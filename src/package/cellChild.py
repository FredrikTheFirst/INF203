import numpy as np
from src.package.cellParant import *

# Just a comment
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
        self._nuvectors = np.array([])
        self._v_avgs = np.array([])
        self._dot = []

    
    def find_midpoint(self, coords):
        super().find_midpoint(coords)
    
    def find_vel(self):
        super().find_vel()
    
    # Find and store the neighbours of each triangle
    def store_neighbours(self, cells):
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

    # Computing the area of each triangle
    def find_area(self, coords):
        self._area = A(coords)
    
    # Calculate the nu-vectors between every neighbour of every triangle
    def find_nuvecs(self, coords):
        self._nuvectors = np.array([nuvector(np.array([coords[i] for i in pointset]), self._midpoint) for pointset in self._neighbours_points])
    
    # Calculating the average of the velocities between the triangle and its neighbours
    def find_avg_v(self, cells):
        self._v_avgs = np.array([0.5 * (self._v + cells[neighid].v) for neighid in self._neighbours_id])

    # Calculating the dot product
    def dodotprods(self):
        self._dot = [el[0] @ el[1] for el in zip(self._v_avgs, self._nuvectors)]
        

    # @property makes it such that you can acses the attributes but
    # not change them 
    @property
    def area(self):
        return self._area
    
    @property
    def neighbours_id(self):
        return self._neighbours_id
    """
    @neighbours_id.setter
    def neighbours_id(self, id):
        if isinstance(id, int):
            return self._neighbours_id
    """

    @property
    def neighbours_points(self):
        return self._neighbours_points
    
    @property
    def nuvectors(self):
        return self._nuvectors
    
    @property
    def v_avgs(self):
        return self._v_avgs
    
    
    @property
    def dot(self):
        return self._dot
    