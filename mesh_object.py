import meshio
import numpy as np


class line_cell:
    def __init__(self, cell_id, coords):
        self._cell_id = cell_id
        self._coords = coords

class triangle_cell:
    def __init__(self, cell_id, coords):
        self._cell_id = cell_id
        self._coords = coords


class cell_factory:
    def __init__(self) -> None:
        self._cell_types = {}
    
    def register(self, key, name):
        self._cell_types[key] = name

    def __call__(self, cell, cell_id, celltype):
        denne_cellen = self._cell_types[celltype](cell_id, cell)
        return denne_cellen


class mesh():
    def __init__(self, mesh_file):
        # Register the different types of cell (line and triangle)
        factory = cell_factory()

        important_cells = ['line', 'triangle']
        for imp_cell in important_cells:
            factory.register(imp_cell, eval(imp_cell+'_cell'))
        

        msh = meshio.read(mesh_file)

        self._cells = []
        self._points = msh.points

        cell_id = 0

        
        for cft in msh.cells:
            # Checking if the cell type is a line or triangle
            is_important = False
            for imp_cell in important_cells:
                if cft.type == imp_cell:
                    is_important = True
            
            # Making the cell objects
            if is_important:
                for cell in cft.data:
                    coords = self._points[cell]
                    self._cells.append(factory(coords, cell_id, cft.type))
                    cell_id += 1
        



            



mesh_file = 'bay.msh'  # Going to test the classes mesh, triangle_cell and line_cell with "bay.mesh" 

msh = mesh(mesh_file)