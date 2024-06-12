from src.package.functions import *

class Cell:
    def __init__(self, cell_id, points):
        # Storing a bunch of values
        self._id = cell_id
        self._points = points
        self._midpoint = None
    
    # Compute the midpoint of the cell
    def find_midpoint(self, coords):
        self._midpoint = midpoint(coords)

    # Finding the velocity at the midpoint
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
    def midpoint(self):
        return self._midpoint