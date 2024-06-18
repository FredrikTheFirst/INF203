from src.package.functions import *
'''
This module provides the parent class for the cells in a mesh
'''

class Cell:
    '''
    An object which is meant to exist among other similar objects
    '''
    def __init__(self, cell_id, points):
        '''
        Stores the parameters as attributes and define other attributes as None

        Parameters:
        cell_id (int): The id of the cell
        points (list): A list of the cell`s points 
        '''
        self._id = cell_id
        self._points = points
        self._midpoint = None
        self._v = None
    
    def find_midpoint(self, coords):
        '''
        Finding the midpoint of the cell and storing it as an attribute

        Parameters:
        coords (ndarray): A matrix containing the coordinates of the corneres of the cell
        '''
        self._midpoint = midpoint(coords)

    def find_vel(self):
        '''
        Finding the velocity at the cell`s midpoint and storing it as an attribute
        '''
        self._v = np.array(v(self._midpoint))
    
    # @property makes it such that you can acses the attributes but
    # not change them 
    @property
    def id(self):
        '''
        Getter to prvid the variable id
        '''
        return self._id
    
    @property
    def points(self):
        return self._points
    
    @property
    def midpoint(self):
        return self._midpoint
    
    @property
    def v(self):
        return self._v