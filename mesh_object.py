import meshio
import numpy as np
from functions import A, midpoint


class line_cell:
    def __init__(self, cell_id, points):
        self._cell_id = cell_id
        self._points = points
        self._neighbours = []
    
    def store_neighbours(self, neig_id):
        self._neighbours.append(neig_id)

class triangle_cell:
    def __init__(self, cell_id, points):
        self._cell_id = cell_id
        self._points = points
        self._neighbours = []

    def find_area(self, coords):
        self._area = A(coords)

    def find_midpoint(self, coords):
        self._midpoint = midpoint(coords)

    def store_neighbours(self, neig_id):
        self._neighbours.append(neig_id)



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
                    coords = self._points[cell]
                    cell_obj = factory(self._points[cell], cell_id, cft.type)
                    self._cells.append(cell_obj)

                    # Here commes some code that is just for simplisety
                    if cft.type == 'line':
                        self._lines.append(cell_obj)
                    
                    elif cft.type == 'triangle':
                        self._triangles.append(cell_obj)
                    


                    cell_id += 1
    
    def cell_area(self):
        for tri in self._triangles:
            tri.find_area(self._points[tri])
    
    def cell_midpoint(self):
        for tri in self._triangles:
            tri.find_midpoint(self._points[tri])

    # NOT done
    def find_neighbours(self):
        for prim_cell in self._cells:
            for neig_cell in self._cells:
                match_point = 0
                for i, prim_coord in enumerate(prim_cell._coords):
                    for j, neig_coord in enumerate(neig_cell._coords):
                        if i <= j and prim_coord.all() == neig_coord.all():
                            match_point += 1
                if match_point == 2:
                    prim_cell.store_neighbours(neig_cell._cell_id)
                    break

                        
        



            



mesh_file = 'simple_mesh.msh'  # Going to test the classes mesh, triangle_cell and line_cell with "simple_mesh.msh" 

msh = mesh(mesh_file)