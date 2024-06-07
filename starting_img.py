import matplotlib.pyplot as plt
import numpy as np
from functions import *
from mesh_object import *

mesh_file = 'bay.msh'
msh = Mesh(mesh_file)
msh.cell_midpoint()
msh.triangel_area()
msh.find_neighbours()



x_mid = np.array([0.35, 0.45])
vfelt = np.array([v(cell.midpoint) for cell in msh.cells])
#Afelt = np.array([tri.area for tri in msh.triangles])

dt = 0.001

u = np.array([starting_amount(x_mid, cell.midpoint) for cell in msh.cells])

def ufunc(u):
    Oillist = u.copy()
    for tri in msh.get_triangles():
        u_old = u[tri.id]
        tri_v = vfelt[tri.id]
        Flist = []
        for neigh_id in tri.neighbours_id:
            neigh = msh.cells[int(neigh_id)]
            u_old_neigh = u[neigh.id]
            neigh_v = vfelt[neigh.id]
            matching_points = set(tri.points) & set(neigh.points)
            matching_coords = np.array([msh.coords[point] for point in matching_points])
            nu = nuvector(matching_coords, tri.midpoint)
            v = 0.5*(tri_v + neigh_v)
            G = g(u_old, u_old_neigh, v, nu)
            F = dOil(dt, tri.area, G)
            Flist.append(F)
        Oillist[tri.id] += sum(Flist)
    return np.array(Oillist)

def ulist(n):
    ulist = [u]
    for i in range(n):
        ulist.append(ufunc(ulist[-1]))
        print(f"Printed u number {i}.")
    return tuple(ulist)

# u = np.array([0.0, 1.0])

# triangle1 = np.array([[0, 0], [0, 1], [1, 1]])
# triangle2 = np.array([[0, 0], [1, 1], [1, 0]])

# Plot the mesh by adding all triangles with their value

oillist = ulist(500)

for i, el in enumerate([oillist[i] for i in range(0, 500, 20)]):
    plt.figure()


    # Create the colormap
    sm = plt.cm.ScalarMappable(cmap='viridis')
    sm.set_array([el])
    umax = max(el)
    umin = min(el)

    # Add colorbar using a separate axis
    cbar_ax = plt.gca().inset_axes([1, 0, 0.05, 1]) # adjust position and size as needed
    plt.colorbar(sm, cax=cbar_ax, label='label3')

    # Need for-loop
    for cell, amount in zip(msh.cells, el):
        coords = msh.coords[cell.points]
        plt.gca().add_patch(plt.Polygon(coords, color=plt.cm.viridis((amount - umin)/(umax - umin)), alpha=0.9))


    # plt.gca().add_patch(plt.Polygon(triangle1, color=plt.cm.viridis((u[0] - umin)/(umax - umin)), alpha=0.9))
    # plt.gca().add_patch(plt.Polygon(triangle2, color=plt.cm.viridis((u[1] - umin)/(umax - umin)), alpha=0.9))

    # Add labels to axes
    plt.xlabel('label1')
    plt.ylabel('label2')
    plt.xlim(0, 1) # set the x-axis limits
    plt.ylim(0, 1) # set the y-axis limits
    plt.gca().set_aspect('equal')

    # Show plot
    plt.savefig(f"tmp\start_img_{i}.png")
    plt.close()
