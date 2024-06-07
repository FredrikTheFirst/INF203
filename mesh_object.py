import meshio
import numpy as np
from abc import ABC, abstractmethod
from functions import midpoint, A



class Cell(ABC):
    def __init__(self, cell_id, points) -> None:
        self._id = cell_id
        self._points = points
        self._neighbours_id = np.array([], dtype='int32')
    
    def find_midpoint(self, coords):
        self._midpoint = midpoint(coords)
    
    def store_neighbours(self, cells):
        my_points = set(self._points)
        for cell in cells:
            matches = my_points & set(cell._points)

            if len(matches) == 2:
                self._neighbours_id = np.append(self._neighbours_id, cell._cell_id)


class Line_cell(Cell):
    def __init__(self, cell_id, points):
        super().__init__(cell_id, points)
    
    def find_midpoint(self, coords):
        super().find_midpoint(coords)
    
    def store_neighbours(self, cells):
        super().store_neighbours(cells)

class Triangle_cell(Cell):
    def __init__(self, cell_id, points):
        super().__init__(cell_id, points)
    
    def find_midpoint(self, coords):
        super().find_midpoint(coords)
    
    def store_neighbours(self, cells):
        super().store_neighbours(cells)

    def find_area(self, coords):
        self._area = A(coords)


class Cell_factory:
    def __init__(self) -> None:
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

        important_cells = ['line', 'triangle']
        for imp_cell in important_cells:
            factory.register(imp_cell, eval(imp_cell.capitalize()+'_cell'))
        

        msh = meshio.read(mesh_file)

        self._cells = []
        cell_id = 0

        self._coords = np.array([np.array(point[0:2]) for point in msh.points])

        for cft in msh.cells:
            # Checking if the cell type is a line or triangle
            is_important = False
            for imp_cell in important_cells:
                if cft.type == imp_cell:
                    is_important = True
            
            # Making the cell objects
            if is_important:
                for cell in cft.data:

                    cell_obj = factory(cell, cell_id, cft.type)
                    self._cells.append(cell_obj)
                    cell_id += 1

    def get_triangles(self):
        return [cell for cell in self._cells if type(cell).__name__ == 'Triangle_cell']

    def triangel_area(self):
        for cell in self.get_triangles():
            cell.find_area(self._coords[cell._points])
    
    def cell_midpoint(self):
        for cell in self._cells:
            cell.find_midpoint(self._coords[cell._points])

    def find_neighbours(self):
        for cell in self._cells:
            cell.store_neighbours(self._cells)

if __name__ == '__main__':
    msh = Mesh('simple_mesh.msh')
    msh.find_neighbours()
    msh.triangel_area()
    msh.cell_midpoint()

    
    for cell in msh._cells:
        print('')
        print('>', cell._cell_id)
        print(cell._midpoint)
        print(cell._neighbours_id)
        print(type(cell).__name__)
    
    
    print('Kun trekanter')
    for cell in msh._cells:
        if type(cell).__name__ == 'Triangle_cell':
            print('>', cell._cell_id)
            print(cell._area)
        
    a = msh.get_triangles()
    print(a)

