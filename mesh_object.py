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

    def __call__(self, cft):
        pass


class mesh():
    def __init__(self, mesh_file):
        # Register the different types of cell (line and triangle)
        factory = cell_factory()

        important_cells = ['line', 'triangle']

        for imp_cell in important_cells:
            factory.register(imp_cell, exec(imp_cell+'_cell'))
        

        self._cells = []

        msh = meshio.read(mesh_file)
        for cft in msh.cells:
            # Checking if the cell type is a line or triangle
            is_important = False
            for imp_cell in important_cells:
                if cft.type == imp_cell:
                    is_important = True
            
            # Dont know how to call all cells of a type.
            # Need another for loop
            if is_important:
                self._cells.append(factory(cft))


                





            



mesh_file = 'bay.msh'  # Going to test the classes mesh, triangle_cell and line_cell with "bay.mesh" 

msh = mesh(mesh_file)