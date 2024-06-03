import meshio


class line_cell:
    def __init__(self):
        pass

class triangle_cell:
    def __init__(self):
        pass


class cell_factory:
    def __init__(self) -> None:
        self._cell_types = {}
    
    def register(self, key, name):
        self._cell_types[key] = name

class mesh():
    def __init__(self, mesh_file):
        # Register the different types of cell (line and triangle)
        factory = cell_factory()
        factory.register('line', line_cell)
        factory.register('triangle', triangle_cell)





mesh_file = 'bay.msh'  # Going to test the classes mesh, triangle_cell and line_cell with "bay.mesh" 

msh = mesh(mesh_file)