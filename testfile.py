from mesh_object import Mesh
import numpy as np

file_name = 'bay.msh'
test = Mesh(file_name)


for tri in test._triangles:
    print(type(tri._points))
    print(tri._points)
    print(tri._cell_id)
    crds = np.array([test._coords[i] for i in tri._points.tolist()])
    print(crds)
    tri.find_area(crds)
    print(tri._area)
    print()