import meshio
import numpy as np
from src.package.cellChild import *


class Cell_factory:
    def __init__(self):
        self._cell_types = {}
    
    def register(self, key, name):
        self._cell_types[key] = name

    def __call__(self, cell, cell_id, celltype):
        denne_cellen = self._cell_types[celltype](cell_id, cell)
        return denne_cellen


class Mesh():
    def __init__(self, mesh_file):
        # Register the different types of cell (line and triangle)
        factory = Cell_factory()

        # We only care about line- and triangle cells
        important_cells = ['line', 'triangle']
        # Register only the types of cell in "important_cells"
        for imp_cell in important_cells:
            factory.register(imp_cell, eval(imp_cell.capitalize()+'_cell'))
        
        # Reading the mesh_file
        msh = meshio.read(mesh_file)

        self._cells = []

        # Gets rid of the always zero z-coordinate while reading
        # the coordinates for each point
        self._coords = np.array([np.array(point[0:2]) for point in msh.points])

        cell_id = 0
        # Go throug the cells from the given mesh_file
        for cft in msh.cells:
            # Checking if the cell type is one of the types in important_cells
            is_important = False
            if cft.type in important_cells:
                is_important = True
            
            # Making the cell objects
            if is_important:
                for cell in cft.data:
                    cell_obj = factory(cell, cell_id, cft.type)
                    self._cells.append(cell_obj)
                    cell_id += 1

    # A method to get a list of only the triangel cells
    def get_triangles(self):
        return [cell for cell in self._cells if type(cell).__name__ == 'Triangle_cell']
    
    # Computing the area of each triangel cell
    def triangel_area(self):
        for cell in self.get_triangles():
            cell.find_area(self._coords[cell.points])
    
    # Computing the midpoint of all cells
    def cell_midpoint(self):
        for cell in self._cells:
            cell.find_midpoint(self._coords[cell.points])

    # Register the neighbours of all cells
    def find_neighbours(self):
        cells = self._cells.copy()
        for id, tri in enumerate(self.get_triangles()):
            tri.store_neighbours(cells)
            cells.remove(tri)
    
    # Finding the scaled normalvector of the sides of triangels
    def find_nuvectors(self):
        for cell in self.get_triangles():
            cell.find_nuvecs(self._coords)
    
    # Finding the vector of each cell given a vector field
    def find_vel_vec(self):
        for cell in self.cells:
            cell.find_vel()

    # Find the average of the velocity vectors of neighbouring cells
    def find_vel_vec_avg(self):
        for tri in self.get_triangles():
            tri.find_avg_v(self._cells)
    
    # Something smart
    def calc_dot_prod(self):
        for cell in self.get_triangles():
            cell.dodotprods()
    
    @property
    def cells(self):
        return self._cells
    
    @property
    def coords(self):
        return self._coords