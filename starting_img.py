import matplotlib.pyplot as plt
import numpy as np
import functions as fc
from mesh_object import *

mesh_file = 'bay.msh'
msh = Mesh(mesh_file)
msh.cell_midpoint()
msh.cell_area()
msh.find_neighbours()



x_mid = np.array([0.5, 0.5])
vfelt = np.array([fc.v(tri._midpoint) for tri in msh._triangles])
#Afelt = np.array([tri._area for tri in msh._triangles])

dt = 0.05

u = np.array([fc.starting_amount(x_mid, cell._midpoint) for cell in msh._cells])

Ftot = []
utot = []
def ufunc(u):
    Fsumlist = u.copy()
    for tri in msh._triangles:
        u_old = u[tri._cell_id]
        tri_v = vfelt[tri._tri_id]
        Flist = []
        for neigh_id in tri._neighbours_id:
            print("First neigh_id:")
            print(neigh_id)
            neigh = msh._cells[int(neigh_id)]
            print("Second neigh:")
            print(neigh)
            u_old_neigh = u[neigh._cell_id]
            print("Old oil of neighbour")
            print(u_old_neigh)
            print('Coords set')
            print(set(tri._points), set(neigh._points))
            matching_points = set(tri._points) & set(neigh._points)
            print("Matching points (indices):")
            print(matching_points)
            matching_coords = np.array([msh._coords[point] for point in matching_points])
            print("Matching coordinates:")
            print(matching_coords)
            nu = fc.nuvector(matching_coords[0], matching_coords[1], tri._midpoint)
            print("nu-vector (element of R2):")
            print(nu)
            F = fc.dOil(dt, tri._area, fc.g(u_old, u_old_neigh, 0.5*(tri_v+fc.v(neigh._midpoint)), nu))
            Ftot.append(F)
            print("Change in oil, F-value, less than 1:")
            print(F)
            print()
            if F > 1:
                print("dOil is more than one:")
                print(F)
            Flist.append(F)
        Fsumlist[tri._cell_id] += sum(Flist)
        utot.append(u_old + sum(Flist))
    return np.array(Fsumlist)

def ulist(n):
    ulist = [u]
    for i in range(n):
        ulist.append(ufunc(ulist[-1]))
    return tuple(ulist)

# u = np.array([0.0, 1.0])

# triangle1 = np.array([[0, 0], [0, 1], [1, 1]])
# triangle2 = np.array([[0, 0], [1, 1], [1, 0]])

# Plot the mesh by adding all triangles with their value

for i, el in enumerate(ulist(8)):
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
    for cell, amount in zip(msh._cells, el):
        coords = msh._coords[cell._points]
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
