import matplotlib.pyplot as plt
import numpy as np
import functions as fc
from mesh_object import *

mesh_file = 'bay.msh'
msh = mesh(mesh_file)
msh.cell_midpoint()
msh.cell_area()
msh.find_neighbours()



x_mid = np.array([0.5, 0.5])
vfelt = np.array([fc.v(tri._midpoint) for tri in msh._triangles])
Afelt = np.array([tri._area for tri in msh._triangles])
#nufelt = np.array([fc.morevectors(np.array(), fc.nuvector) for neighbour in tri._neighbours] for tri in msh._triangles])

dt = 0.5

u = np.array([fc.starting_amount(x_mid, tri._midpoint) for tri in msh._triangles])
ungh = np.array([[fc.starting_amount(x_mid, mid) for mid in tri._neighbours] for tri in msh._triangles])
Fsumlist = []
for tri in msh._triangles:
    u_old = u[tri._cell_id]
    tri_v = vfelt[tri._cell_id]
    Flist = []
    for neigh in tri._neighbours:
        neigh = msh._triangles[neigh]
        print(tri._points)
        print(neigh._points)
        matching_points = set(tri._points) & set(neigh._points)
        print(matching_points)
        matching_coords = np.array(msh._points[matching_points])
        nu = fc.nuvector(matching_coords[0], matching_coords[1], tri._midpoint)
        u_old_neigh = u[neigh._cell_id]
        F = fc.dOil(dt, tri._area, g((u_old, u_old_neigh, tri_v, nu)))
        Flist.append(F)
    sum(Flist)
    Fsumlist.append(Flist)

u2 = np.array([sum(e) for e in zip(u, Fsumlist)])



#u2 = u + sum([fc.dOil(dt, Afelt, fc.g(u, u_ngh, vfelt, nu)) for u_ngh, nu in zip(ungh, nufelt)])

# u = np.array([0.0, 1.0])

# triangle1 = np.array([[0, 0], [0, 1], [1, 1]])
# triangle2 = np.array([[0, 0], [1, 1], [1, 0]])

# Plot the mesh by adding all triangles with their value
plt.figure()


# Create the colormap
sm = plt.cm.ScalarMappable(cmap='viridis')
sm.set_array([u])
umax = max(u)
umin = min(u)

# Add colorbar using a separate axis
cbar_ax = plt.gca().inset_axes([1, 0, 0.05, 1]) # adjust position and size as needed
plt.colorbar(sm, cax=cbar_ax, label='label3')

# Need for-loop
for tri, amount in zip(msh._triangles, u):
    coords = msh._points[tri._points]
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
plt.savefig("start_img.png")
plt.close()
