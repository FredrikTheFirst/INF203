
#VI SKAL IKKE BRUKE DETTE:D

import matplotlib.pyplot as plt
import numpy as np
from functions import *
from mesh_object import *

mesh_file = 'bay.msh'
msh = Mesh(mesh_file)
msh.cell_midpoint()
msh.cell_area()
msh.find_neighbours()



x_mid = np.array([0.35, 0.45])
vfelt = np.array([v(cell._midpoint) for cell in msh._cells])
#Afelt = np.array([tri._area for tri in msh._triangles])

dt = 0.001

u = np.array([starting_amount(x_mid, cell._midpoint) for cell in msh._cells])

def ufunc(u):
    Oillist = u.copy()
    for tri in msh._triangles:
        u_old = u[tri._cell_id]
        tri_v = vfelt[tri._cell_id]
        neighvlist = np.array([vfelt[i] for i in tri._neighbours_id])
        neighoil = np.array([Oillist[i] for i in tri._neighbours_id])
        matching_coords_list = np.array([[msh._coords[point] for point in set(tri._points) & set(msh._cells[i]._points)] for i in tri._neighbours_id])
        nu = np.array([nuvector(matching_coords, x_mid) for matching_coords in matching_coords_list])
        v = 0.5*(tri_v + neighvlist)
        G = np.array([g(u_old, neighoil, vi, nui) for vi, nui in zip(v, nu)])
        F = dOil(dt, tri._area, G, nu)
        Oillist[tri._cell_id] += F
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
