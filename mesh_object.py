import meshio
import numpy as np
from functions import A, midpoint


class line_cell:
    def __init__(self, cell_id, points):
        self._cell_id = cell_id
        self._points = points
        self._neighbours = []
    
    def store_neighbours(self, cells):
        my_points = set(self._points)
        for cell in enumerate(cells):
            matches = my_points & set(cell._points)

            if len(matches) == 2:
                self._neighbours.append(cell._cell_id)

class triangle_cell:
    def __init__(self, cell_id, points):
        self._cell_id = cell_id
        self._points = points
        self._neighbours = []

    def find_area(self, coords):
        self._area = A(coords)

    def find_midpoint(self, coords):
        self._midpoint = midpoint(coords)

    def store_neighbours(self, cells):
        my_points = set(self._points)
        for cell in enumerate(cells):
            matches = my_points & set(cell._points)

            if len(matches) == 2:
                self._neighbours.append(cell._cell_id)




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


        self._points = np.array([np.array(point[0:2]) for point in msh.points])

        line_id = 0
        tri_id = 0

        self._lines = []
        self._triangles = []


        for cft in msh.cells:
            # Checking if the cell type is a line or triangle
            is_important = False
            for imp_cell in important_cells:
                if cft.type == imp_cell:
                    is_important = True
            
            # Making the cell objects
            if is_important:
                for cell in cft.data:

                    
                    # Here commes some code that is just for simplicity
                    if cft.type == 'line':
                        cell_obj = factory(cell, line_id, cft.type)
                        self._lines.append(cell_obj)
                        line_id += 1
                    
                    elif cft.type == 'triangle':
                        cell_obj = factory(cell, tri_id, cft.type)
                        self._triangles.append(cell_obj)
                        tri_id += 1
                    
                    self._cells.append(cell_obj)

    
    def cell_area(self):
        for tri in self._triangles:
            tri.find_area(self._points[tri._points])
    
    def cell_midpoint(self):
        for tri in self._triangles:
            tri.find_midpoint(self._points[tri._points])

    def find_neighbours(self):
        for cell in self._cells:
            cell.store_neighbours(self._cells)
