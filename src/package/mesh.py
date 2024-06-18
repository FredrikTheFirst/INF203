import meshio
import numpy as np
from src.package.cellChild import *
'''
This module reads in a .msh and establishes the cells
'''

class Cell_factory:
    '''
    A factory class to help define cell objects
    '''
    def __init__(self):
        '''
        Stores an empty dictionary as an attribute
        '''
        self._cell_types = {}
    
    def register(self, key, name):
        '''
        Filling in the _cell_types (dictionary) attribute

        Parameteres:
        key (float): A string which can be used to get the variable name
        name (type): The class name with which we can make an object
        '''
        self._cell_types[key] = name

    def __call__(self, cell, cell_id, celltype):
        '''
        Calling a class from the attribute _cell_types and creating an object

        Paremeters:
        cell (list): A list of the points of the cells
        cell_id (int): The id of the cell
        celltype (string): Which type of cell this is. Used to get the class name from the dictionary

        Returns:
        obj: A cell of a certian type with some of the parameters as attributes
        '''
        denne_cellen = self._cell_types[celltype](cell_id, cell)
        return denne_cellen


class Mesh():
    '''
    The object which is going to contain cells and coordinates in an organized fashion
    as well as defining properties of the cells
    '''
    def __init__(self, mesh_file):
        '''
        Read a .msh file and store its information

        Paramteres
        mesh_file (string): Name of the .msh file
        '''

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

    def get_triangles(self):
        '''
        Makes a list of just the triangle cells

        Return:
        list: The mesh`s triangle cells
        '''
        return [cell for cell in self._cells if type(cell).__name__ == 'Triangle_cell']

    def triangel_area(self):
        '''
        Calling the cell method that finds the area of each triangle
        '''
        for cell in self.get_triangles():
            cell.find_area(self._coords[cell.points])
    
    def cell_midpoint(self):
        '''
        Calling the cell method that finds the midpoint of each cell
        '''
        for cell in self._cells:
            cell.find_midpoint(self._coords[cell.points])

    def find_neighbours(self):
        '''
        Calling the cell method that finds and stores the neighbours of each triangle
        '''
        cells = self._cells.copy()
        for tri in self.get_triangles():
            cells.remove(tri)
            tri.store_neighbours(cells)
    
    def find_nuvectors(self):
        '''
        Calling the cell method that finds the outward pointing vector for a side of the each triangle
        with the absolute vale equal to the length of the side. This vector is called the nuvector
        '''
        for cell in self.get_triangles():
            cell.find_nuvecs(self._coords)
    
    def find_vel_vec(self):
        '''
        Calling the cell method that finds the velocity for each cell
        '''
        for cell in self.cells:
            cell.find_vel()

    def find_vel_vec_avg(self):
        '''
        Calling the cell method that finds the average between the triangle`s velocity
        and each of it`s neighbour`s velocities
        '''
        for tri in self.get_triangles():
            tri.find_avg_v(self._cells)
            
    def calc_dot_prod(self):
        '''
        Calling the methodes that finds the dotproducts between each side`s nuvector and the average of the velocites between the triangle
        and the neighbour which it shares the side with.
        '''
        for tri in self.get_triangles():
            tri.dodotprods()
    
    @property
    def cells(self):
        return self._cells
    
    @property
    def coords(self):
        return self._coords
