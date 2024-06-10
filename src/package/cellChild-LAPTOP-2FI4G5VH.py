import numpy as np
from src.cellParant import Cell



class Line_cell(Cell):
    # The super() makes it so that this class inherites the method
    # from the parent class
    def __init__(self, cell_id, points):
        super().__init__(cell_id, points)
    
    def find_midpoint(self, coords):
        super().find_midpoint(coords)


class Triangle_cell(Cell):
    # The super() makes it so that this class inherites the method
    # from the parent class
    def __init__(self, cell_id, points):
        super().__init__(cell_id, points)
        self._area = None
        # The id's get stored as int
        self._neighbours_id = np.array([], dtype='int32')
    
    def find_midpoint(self, coords):
        super().find_midpoint(coords)
    
    # Find and store the neighbours of each triangel
    def store_neighbours(self, cells):
        my_points = set(self._points)
        for cell in cells:
            matches = my_points & set(cell.points)

            if len(matches) == 2:
                self._neighbours_id = np.append(self._neighbours_id, cell.id)

    # Computing the area of each triangel
    def find_area(self, coords):
        self._area = A(coords)

    # @property makes it such that you can acses the attributes but
    # not change them 
    @property
    def area(self):
        return self._area
