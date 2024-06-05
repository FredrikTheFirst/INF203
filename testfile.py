from mesh_object import line_cell, triangle_cell, cell_factory, mesh

file_name = 'bay.msh'
test = mesh(file_name)



for tri in test._triangles:
    print(type(tri._points))
    print(tri._points)
    print(tri._cell_id)
