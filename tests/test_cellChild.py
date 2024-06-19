import pytest
import numpy as np
from src.package.cellChild import *
'''
This file is for testing the methodes and attributes of
the Line_cell class and the Triangle_cell class from the module cellChild
'''

#%% Testing the methodes and attributes of Line_cell and triangle_cell which they have innherited from Cell

# A bunch of coordinates we are using to test the methodes
coords = np.array([[9, 3.25], [7.4, 4.8], [4.4, 1.6], [1, 0], [0, 1], [0, 0], [1.8, 0.5], [1.9, 0.9], [2.1, 25.6]])

@pytest.fixture
def advanced_Line_cell():
    '''
    Defining a list om Line_cell objects

    Returns:
    list: a list of Line_cell objects
    '''
    cells = []
    cells.append(Line_cell(1, [1, 2]))
    cells.append(Line_cell(5, [4, 5]))
    cells.append(Line_cell(4, [6, 7]))
    return cells

@pytest.fixture
def advanced_Triangle_cell():
    '''
    Defining a list om Triangle_cell objects

    Returns:
    list: a list of Triangle_cell objects
    '''
    cells = []
    cells.append(Triangle_cell(0, [0, 1, 2]))
    cells.append(Triangle_cell(2, [3, 4, 5]))
    cells.append(Triangle_cell(3, [6, 7, 8]))
    return cells


@pytest.mark.parametrize('line_ids, triangle_ids', [([1, 5, 4],
                                                     [0, 2, 3])])
def test_cell_id(advanced_Line_cell, advanced_Triangle_cell, line_ids, triangle_ids):
    '''
    Testing if the cells` id is stored correctly

    Parameteres:
    advanced_Line_cell (list): A list containing Line_cell`s 
    advanced_Triangle_cell (list): A list containing Triangle_cell`s
    line_ids (list): A list containing the ids of the Line_cell`s
    triangle_ids (list): A list containing the ids of the Triangle_cell`s
    '''
    for cells, ids in ((advanced_Line_cell, line_ids), (advanced_Triangle_cell, triangle_ids)):
        for id, cell in zip(ids, cells):
            assert cell.id == id

    
@pytest.mark.parametrize('list_line_points, list_triangle_points', [([[1, 2], [4, 5], [6, 7]],
                                                                     [[0, 1, 2], [3, 4, 5], [6, 7, 8]])])
def test_cell_points(advanced_Line_cell, advanced_Triangle_cell, list_line_points, list_triangle_points):
    '''
    Testing if the cells` points are stored correctly

    Parameteres:
    advanced_Line_cell (list): A list containing Line_cell`s 
    advanced_Triangle_cell (list): A list containing Triangle_cell`s
    list_line_points (list): A list containing the points of the Line_cell`s
    list_triangle_points (list): A list containing the points of the Triangle_cell`s
    '''
    for cells, list_points in ((advanced_Line_cell, list_line_points), (advanced_Triangle_cell, list_triangle_points)):
        for points, cell in zip(list_points, cells):
            assert cell.points == points
    

@pytest.mark.parametrize('line_mids, triangle_mids, coords', [(np.array([[5.9, 3.2], [0, 0.5], [1.85, 0.7]]),
                                                               np.array([[104/15, 193/60], [1/3, 1/3], [29/15, 9]]),
                                                               coords)])
def test_cell_midpoint(advanced_Line_cell, advanced_Triangle_cell, line_mids, triangle_mids, coords):
    '''
    Testing if the cells` midpoint are calculated and stored correctly

    Parameteres:
    advanced_Line_cell (list): A list containing Line_cell`s 
    advanced_Triangle_cell (list): A list containing Triangle_cell`s
    line_mids (ndarray): An array containing the midpoint of each Line_cell
    triangle_mids (ndarray): An array containing the midpoint of each Triangle_cell
    coords (ndarray): The array containing the coordinates from the top of the file
    '''
    for cells, mids in ((advanced_Line_cell, line_mids), (advanced_Triangle_cell, triangle_mids)):
        for mid, cell in zip(mids, cells):
            cell.find_midpoint(coords[cell.points])
            for mid_coord, cell_coord in zip(mid, cell.midpoint):
                assert cell_coord == pytest.approx(mid_coord)

@pytest.mark.parametrize('list_line_v, list_triangle_v, coords', [([np.array([2.02, -5.9]), np.array([0.5, -0]), np.array([0.33, -1.85])],
                                                           [np.array([1.83, -6.93333333]), np.array([0.26666667, -0.33333333]), np.array([8.61333333, -1.93333333])],
                                                           coords)])
def test_cell_v(advanced_Line_cell, advanced_Triangle_cell, list_line_v, list_triangle_v, coords):
    '''
    Testing if the cells` v-attribute is calculated and stored correctly
    
    Parameteres:
    advanced_Line_cell (list): A list containing Line_cell`s
    advanced_Triangle_cell (list): A list containing Triangle_cell`s
    list_line_v (lsit): A list containing the v-attribute of each Line_cell
    list_triangle_v (list): A list containing the v-attribute of each Triangle_cell
    coords (ndarray): The array containing the coordinates from the top of the file
    '''
    for cells, list_v in ((advanced_Line_cell, list_line_v), (advanced_Triangle_cell, list_triangle_v)):
        for v, cell in zip(list_v, cells):
            # Need to define midpoints first
            cell.find_midpoint(coords[cell.points])
            cell.find_vel()
            for v_coord, cell_coord in zip(v, cell.v):
                assert cell_coord == pytest.approx(v_coord)

#%% Testing the methodes and attributes unique to triangle_cell
# Line_cell does not have any methodes or attributes not inherited from Cell


@pytest.mark.parametrize('list_area, coords', [([4.884999999999999, 0.5, 1.1949999999999983],
                                                coords)])
def test_triangle_area(advanced_Triangle_cell, list_area, coords):
    '''
    Testing if the triangles` area is calculated and stored correctly
    
    Parameteres:
    advanced_Triangle_cell (list): A list containing Triangle_cell`s
    list_area (list): A list containing the area of each Triangle_cell
    coords (ndarray): The array containing the coordinates from the top of the file
    '''
    for triangle, area in zip(advanced_Triangle_cell, list_area):
        triangle.find_area(coords[triangle.points])
        assert triangle.area == pytest.approx(area)

@pytest.mark.parametrize('list_neighbours', [([np.array([1], dtype='int32'),
                                               np.array([5], dtype='int32'),
                                               np.array([4], dtype='int32')])])
def test_triangle_neighbours_id(advanced_Line_cell, advanced_Triangle_cell, list_neighbours):
    '''
    Testing if the triangles` neighbour`s id are stored correctly
    
    Parameteres:
    advanced_Line_cell (list): A list containing Line_cell`s
    advanced_Triangle_cell (list): A list containing Triangle_cell`s
    list_neighbours (list): A list containing the ids to the neighbours of each Triangle_cell
    coords (ndarray): The array containing the coordinates from the top of the file
    '''
    triangles = advanced_Triangle_cell
    cells = advanced_Line_cell + triangles

    for neighbours, triangle in zip(list_neighbours, triangles):
        triangle.store_neighbours(cells)
        cells.remove(triangle)
        for neigh_id, triangle_neigh_id in zip(neighbours, triangle.neighbours_id):
            assert triangle_neigh_id == neigh_id

@pytest.mark.parametrize('list_neighbours', [([np.array([{1, 2}]),
                                               np.array([{4, 5}]),
                                               np.array([{6, 7}])])])
def test_triangle_neighbours_points(advanced_Line_cell, advanced_Triangle_cell, list_neighbours):
    '''
    Testing if the points shared between the Triangles and it`s neighbours are found and stored correctly
    
    Parameteres:
    advanced_Line_cell (list): A list containing Line_cell`s
    advanced_Triangle_cell (list): A list containing Triangle_cell`s
    list_neighbours (list): A list containing the points shared between each Triangle_cell and it`s neighbours
    coords (ndarray): The array containing the coordinates from the top of the file
    '''
    triangles = advanced_Triangle_cell
    cells = advanced_Line_cell + triangles
    
    for neighbours, triangle in zip(list_neighbours, triangles):
        triangle.store_neighbours(cells)
        cells.remove(triangle)
        for neigh_points, triangle_neigh_points in zip(neighbours, triangle.neighbours_points):
            for neigh_point, triangle_neigh_point in zip(neigh_points, triangle_neigh_points):
                assert triangle_neigh_point == neigh_point

@pytest.mark.parametrize('list_vectors, coords', [([np.array([[-3.2, 3]]),
                                                    np.array([[-1, 0]]),
                                                    np.array([[0.4, -0.1]])],
                                                   coords)])
def test_triangle_nuvectors(advanced_Line_cell, advanced_Triangle_cell, list_vectors, coords):
    '''
    Testing if each triangle`s nuvectors are calculated and stored correctly
    
    Parameteres:
    advanced_Line_cell (list): A list containing Line_cell`s
    advanced_Triangle_cell (list): A list containing Triangle_cell`s
    list_vectors (list): A list containing each Triangle_cell`s nuvectores
    coords (ndarray): The array containing the coordinates from the top of the file
    '''
    triangles = advanced_Triangle_cell
    cells = advanced_Line_cell + triangles
    for nuvecs, triangle in zip(list_vectors, triangles):
        triangle.find_midpoint(coords[triangle.points])
        triangle.store_neighbours(cells)
        cells.remove(triangle)

        triangle.find_nuvecs(coords)

        for nuvec, triangle_nuvec in zip(nuvecs, triangle.nuvectors):
            for nu_coord, tri_nu_coord in zip(nuvec, triangle_nuvec):
                assert tri_nu_coord == pytest.approx(nu_coord)

@pytest.mark.parametrize('list_vectors, coords', [([[[1.165, -3.46666667]],
                                                    [[4.44, -1.13333333]],
                                                    [[4.44, -1.13333333]]],
                                                   coords)])
def test_find_avg_v(advanced_Line_cell, advanced_Triangle_cell, list_vectors, coords):
    '''
    Testing if each triangle`s v_avgs-attribute is calculated and stored correctly
    
    Parameteres:
    advanced_Line_cell (list): A list containing Line_cell`s
    advanced_Triangle_cell (list): A list containing Triangle_cell`s
    list_vectors (list): A list containing each Triangle_cell`s v_avgs-attribute
    coords (ndarray): The array containing the coordinates from the top of the file
    '''
    triangles = advanced_Triangle_cell
    cells = advanced_Line_cell + triangles
    cells_copy = cells.copy()

    for cell in cells:
        cell.find_midpoint(coords[cell.points])
        cell.find_vel()

    for vectors, triangle in zip(list_vectors, triangles):
        triangle.store_neighbours(cells)
        cells_copy.remove(triangle)
        triangle.find_avg_v(cells)

        for vector, tri_v_avgs in zip(vectors, triangle.v_avgs):
            for coord_vector, tri_v_avg in zip(vector, tri_v_avgs):
                assert tri_v_avg == pytest.approx(coord_vector)

@pytest.mark.parametrize('list_dotprods, coords', [([[-14.12800001], [-4.44], [1.8893333330000002]],
                                                  coords)])
def test_dotprods(advanced_Line_cell, advanced_Triangle_cell, list_dotprods, coords):
    '''
    Testing if each triangle`s dotproducts are calculated and stored correctly
    
    Parameteres:
    advanced_Line_cell (list): A list containing Line_cell`s
    advanced_Triangle_cell (list): A list containing Triangle_cell`s
    list_dotprods (list): A list containing each Triangle_cell`s dotproducts
    coords (ndarray): The array containing the coordinates from the top of the file
    '''
    triangles = advanced_Triangle_cell
    cells = advanced_Line_cell + triangles
    cells_copy = cells.copy()

    for cell in cells:
        cell.find_midpoint(coords[cell.points])
        cell.find_vel()

    for dots, triangle in zip(list_dotprods, triangles):
        triangle.store_neighbours(cells)
        cells_copy.remove(triangle)
        triangle.find_avg_v(cells)
        triangle.find_nuvecs(coords)
        triangle.dodotprods()

        for dot, tri_dot in zip(dots, triangle.dot):
            assert tri_dot == pytest.approx(dot)

            





        
    














