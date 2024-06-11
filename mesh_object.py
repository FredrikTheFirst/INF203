import meshio
import numpy as np
from src.package.functions import *



class Cell:
    def __init__(self, cell_id, points):
        # Storing a bunch of values
        self._id = cell_id
        self._points = points
        self._midpoint = None
        self.oil = 0
    
    # Compute the midpoint of the cell
    def find_midpoint(self, coords):
        self._midpoint = midpoint(coords)

    def find_vel(self):
        self._v = np.array(v(self._midpoint))
    
    # @property makes it such that you can acses the attributes but
    # not change them 
    @property
    def id(self):
        return self._id
    
    @property
    def points(self):
        return self._points
    
    @property
    def neighbours_id(self):
        return self._neighbours_id
    
    @property
    def midpoint(self):
        return self._midpoint


class Line_cell(Cell):
    # The super() makes it so that this class inherites the method
    # from the parent class
    def __init__(self, cell_id, points):
        super().__init__(cell_id, points)
    
    def find_midpoint(self, coords):
        super().find_midpoint(coords)
    
    def find_vel(self):
        super().find_vel()


class Triangle_cell(Cell):
    # The super() makes it so that this class inherites the method
    # from the parent class
    def __init__(self, cell_id, points):
        super().__init__(cell_id, points)
        self._area = None
        # The id's get stored as int
        self._neighbours_id = np.array([], dtype='int32')
        self._neighbours_points = np.array([])
    
    def find_midpoint(self, coords):
        super().find_midpoint(coords)
    
    def find_vel(self):
        super().find_vel()
    
    # Find and store the neighbours of each triangle
    def store_neighbours(self, cells):
        my_points = set(self._points)
        for cell in cells:
            matches = my_points & set(cell.points)

            if len(matches) == 2:
                self._neighbours_id = np.append(self._neighbours_id, cell.id)
                self._neighbours_points = np.append(np.array(self._neighbours_points), matches)

    # Calculate the nu-vectors between every neighbour of every triangle
    def find_nuvecs(self, coords):
        self._nuvectors = np.array([nuvector(np.array([coords[i] for i in pointset]), self._midpoint) for pointset in self._neighbours_points])

    def find_avg_v(self, cells):
        self._v_avgs = np.array([0.5 * (self._v + cells[neighid]._v) for neighid in self._neighbours_id])

    # Computing the area of each triangle
    def find_area(self, coords):
        self._area = A(coords)
    
    def dodotprods(self):
        self._dot = np.array([el[0] @ el[1] for el in zip(self._v_avgs, self._nuvectors)])
    
    # @property makes it so that you can access the attributes but
    # not change them 
    @property
    def area(self):
        return self._area


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
        for cell in self.get_triangles():
            cell.store_neighbours(self._cells)
    
    def find_velocity(self):
        for cell in self.cells:
            cell.find_vel()
    
    def find_avg_velocity(self):
        for tri in self.get_triangles():
            tri.find_avg_v(self._cells)
    
    def find_nuvectors(self):
        for cell in self.get_triangles():
            cell.find_nuvecs(self._coords)
    
    def calc_dot_prod(self):
        for cell in self.get_triangles():
            cell.dodotprods()

    @property
    def cells(self):
        return self._cells
    
    @property
    def coords(self):
        return self._coords
