import numpy as np
from src.package.cellParent import *
'''
This module provides the cell objects used in meshes
'''


class Line_cell(Cell):
    '''
    A child class which inherites properties of the parent class Cell
    A class for cells that happens to be lines
    '''
    def __init__(self, cell_id, points):
        '''
        Calling the parent method
        '''
        super().__init__(cell_id, points)
    
    def find_midpoint(self, coords):
        '''
        Calling the parent method
        '''
        super().find_midpoint(coords)
    
    def find_vel(self):
        '''
        Calling the parent method
        '''
        super().find_vel()


class Triangle_cell(Cell):
    '''
    A child class which inherites properties of the parent class Cell
    A class for cells that happens to be triangles
    '''
    def __init__(self, cell_id, points):
        '''
        Calling the parent method and defining aditional empty/None attributes to be used later
        '''
        super().__init__(cell_id, points)
        self._area = None
        self._neighbours_id = np.array([], dtype='int32')
        self._neighbours_points = np.array([])
        self._nuvectors = np.array([])
        self._v_avgs = np.array([])
        self._dot = []

    
    def find_midpoint(self, coords):
        '''
        Calling the parent method
        '''
        super().find_midpoint(coords)
    
    def find_vel(self):
        '''
        Calling the parent method
        '''
        super().find_vel()
    
    def store_neighbours(self, cells):
        '''
        Finds and stores the id`s and shared points of neighbours as attributes

        Parameteres:
        cells (list): A list of the cells that might neighbour the triangle
        '''
        my_points = set(self._points)

        # If a triangle already has 3 neigbhours we dont look for others
        if len(self._neighbours_id) != 3:
            for cell in cells:
                matches = my_points & set(cell.points)

                if len(matches) == 2:
                    self._neighbours_id = np.append(self._neighbours_id, cell.id)
                    self._neighbours_points = np.append(np.array(self._neighbours_points), matches)
                    
                    # If the neigbours is a triangle we store the cell`s id in the neigbhours list 
                    if type(cell).__name__ == 'Triangle_cell':
                        cell._neighbours_id = np.append(cell._neighbours_id, self._id)
                        cell._neighbours_points = np.append(np.array(cell._neighbours_points), matches)
                        
                    # If a triangle already has 3 neigbhours we break from the loop
                    if len(self._neighbours_id) == 3:
                        break

    def find_area(self, coords):
        '''
        Computing the area of the Triangle and storing it as an attribute

        Parameters:
        coords (ndarray): A matrix containing the 2D position vector of the corners of the triangle
        '''
        self._area = A(coords)
    
    def find_nuvecs(self, coords):
        '''
        Calculating the outward pointing vectors for the sides of the triangle with the
        absolute vale equal to the length of the side. Then storing the vectors in an array.
        These vectors are called the nuvectors

        Parameters:
        coords (ndarray): A matrix containing the 2D position vector of the corners of the triangle
        '''
        self._nuvectors = np.array([nuvector(np.array([coords[i] for i in pointset]), self._midpoint) for pointset in self._neighbours_points])
    
    def find_avg_v(self, cells):
        '''
        Calculating the average between the triangle`s velocity and each of it`s neighbour`s velocities.
        Then storing the averages in an array

        Parameters:
        cells (list): A list containing all the cells
        '''
        self._v_avgs = np.array([0.5 * (self._v + cells[neighid].v) for neighid in self._neighbours_id])

    def dodotprods(self):
        '''
        Calculating the dotproducts between each side`s nuvector and the average of the velocites between the triangle
        and the neighbour which it shares the side with.
        '''
        self._dot = [el[0] @ el[1] for el in zip(self._v_avgs, self._nuvectors)]
     
    @property
    def area(self):
        '''
        Getter to provid the variable area
        '''
        return self._area
    
    @property
    def neighbours_id(self):
        '''
        Getter to provid the variable neighbours_id
        '''
        return self._neighbours_id

    @property
    def neighbours_points(self):
        '''
        Getter to provid the variable neighbous_points
        '''
        return self._neighbours_points
    
    @property
    def nuvectors(self):
        '''
        Getter to provid the variable nuvectors
        '''
        return self._nuvectors
    
    @property
    def v_avgs(self):
        '''
        Getter to provid the variable v_avgs
        '''
        return self._v_avgs
    
    @property
    def dot(self):
        '''
        Getter to provid the variable dot
        '''
        return self._dot
    