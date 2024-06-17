import pytest
from src.package.cellChild import *


#%% Testing the methodes and attributes of Line_cell and Triangel_cell which they have innherited from Cell

coords = np.array([[9, 3.25], [7.4, 4.8], [4.4, 1.6], [1, 0], [0, 1], [0, 0], [1.8, 0.5], [1.9, 0.9], [2.1, 25.6]])

@pytest.fixture
def advanced_Line_cell():
    cells = []
    cells.append(Line_cell(1, [1, 2]))
    cells.append(Line_cell(5, [4, 5]))
    cells.append(Line_cell(4, [6, 7]))
    return cells

@pytest.fixture
def advanced_Triangel_cell():
    cells = []
    cells.append(Triangle_cell(0, [0, 1, 2]))
    cells.append(Triangle_cell(2, [3, 4, 5]))
    cells.append(Triangle_cell(3, [6, 7, 8]))
    return cells

@pytest.mark.parametrize('line_ids, triangel_ids', [([1, 5, 4],
                                                     [0, 2, 3])])
def test_cell_id(advanced_Line_cell, advanced_Triangel_cell, line_ids, triangel_ids):
    for cells, ids in ((advanced_Line_cell, line_ids), (advanced_Triangel_cell, triangel_ids)):
        for id, cell in zip(ids, cells):
            assert cell.id == id

    
@pytest.mark.parametrize('list_line_points, list_triangel_points', [([[1, 2], [4, 5], [6, 7]],
                                                                     [[0, 1, 2], [3, 4, 5], [6, 7, 8]])])
def test_cell_points(advanced_Line_cell, advanced_Triangel_cell, list_line_points, list_triangel_points):
    for cells, list_points in ((advanced_Line_cell, list_line_points), (advanced_Triangel_cell, list_triangel_points)):
        for points, cell in zip(list_points, cells):
            assert cell.points == points
    

@pytest.mark.parametrize('line_mids, triangel_mids, coords', [([[5.9, 3.2], [0, 0.5], [1.85, 0.7]],
                                                               [[104/15, 193/60], [1/3, 1/3], [29/15, 9]],
                                                               coords)])
def test_cell_midpoint(advanced_Line_cell, advanced_Triangel_cell, line_mids, triangel_mids, coords):
    for cells, mids in ((advanced_Line_cell, line_mids), (advanced_Triangel_cell, triangel_mids)):
        for mid, cell in zip(mids, cells):
            # Make sure the midpoint`s` are None if find_midpoint() is not called
            assert cell.midpoint == None
            cell.find_midpoint(coords[cell.points])
            for mid_coord, cell_coord in zip(mid, cell.midpoint):
                assert cell_coord == pytest.approx(mid_coord)

@pytest.mark.parametrize('list_line_v, list_triangel_v, coords', [([np.array([2.02, -5.9]), np.array([0.5, -0]), np.array([0.33, -1.85])],
                                                           [np.array([1.83, -6.93333333]), np.array([0.26666667, -0.33333333]), np.array([8.61333333, -1.93333333])],
                                                           coords)])
def test_cell_v(advanced_Line_cell, advanced_Triangel_cell, list_line_v, list_triangel_v, coords):
    for cells, list_v in ((advanced_Line_cell, list_line_v), (advanced_Triangel_cell, list_triangel_v)):
        for v, cell in zip(list_v, cells):
            # Make sure the v`s are None if find_vel() is not called
            assert cell.v == None
            # Need to define midpoints first
            cell.find_midpoint(coords[cell.points])
            cell.find_vel()
            for v_coord, cell_coord in zip(v, cell.v):
                assert cell_coord == pytest.approx(v_coord)

#%% Testing the methodes and attributes unique to Triangel_cell
# Line_cell does not have any unique methodes or attributes


@pytest.mark.parametrize('list_area, coords', [([4.884999999999999, 0.5, 1.1949999999999983],
                                                coords)])
def test_triangel_area(advanced_Triangel_cell, list_area, coords):
    for triangel, area in zip(advanced_Triangel_cell, list_area):
        # Make sure the area`s are None if find_area() is not called
        assert triangel.area == None
        triangel.find_area(coords[triangel.points])
        assert triangel.area == pytest.approx(area)

@pytest.mark.parametrize('list_neighbours', [([np.array([1], dtype='int32'),
                                               np.array([5], dtype='int32'),
                                               np.array([4], dtype='int32')])])
def test_triangel_neighbours_id(advanced_Triangel_cell, advanced_Line_cell, list_neighbours):
    triangles = advanced_Triangel_cell
    cells = advanced_Line_cell + triangles

    for triangel in triangles:
        # Making sure the neighbours_id`s arrays are empty if store._neighbours() is not called
        assert len(triangel.neighbours_id) == 0
    
    for neighbours, triangel in zip(list_neighbours, triangles):
        triangel.store_neighbours(cells)
        cells.remove(triangel)
        for neigh_id, triangel_neigh_id in zip(neighbours, triangel.neighbours_id):
            assert triangel_neigh_id == neigh_id

@pytest.mark.parametrize('list_neighbours', [([np.array([{1, 2}]),
                                               np.array([{4, 5}]),
                                               np.array([{6, 7}])])])
def test_triangel_neighbours_points(advanced_Line_cell, advanced_Triangel_cell, list_neighbours):
    triangles = advanced_Triangel_cell
    cells = advanced_Line_cell + triangles

    for triangel in triangles:
        # Making sure the neighbours_points`s arrays are empty if store._neighbours() is not called
        assert len(triangel.neighbours_points) == 0
    
    for neighbours, triangel in zip(list_neighbours, triangles):
        triangel.store_neighbours(cells)
        cells.remove(triangel)
        for triangel_neigh_points in neighbours:
            pass
            # for neigh_point, triangel_neigh_point in zip(neigh_points, triangel_neigh_points):
                # assert triangel_neigh_point == neigh_point

@pytest.mark.parametrize('list_vectors, coords', [([np.array([[-3.2, 3]]),
                                                    np.array([[-1, 0]]),
                                                    np.array([[0.4, -0.1]])],
                                                   coords)])
def test_triangel_nuvectors(advanced_Line_cell, advanced_Triangel_cell, list_vectors, coords):
    triangles = advanced_Triangel_cell
    cells = advanced_Line_cell + triangles
    for nuvecs, triangel in zip(list_vectors, triangles):
        triangel.find_midpoint(coords[triangel.points])
        triangel.store_neighbours(cells)
        cells.remove(triangel)

        triangel.find_nuvecs(coords)

        for nuvec, triangel_nuvec in zip(nuvecs, triangel.nuvectors):
            for nu_coord, tri_nu_coord in zip(nuvec, triangel_nuvec):
                assert tri_nu_coord == pytest.approx(nu_coord)

@pytest.mark.parametrize('list_vectors, coords', [([[[1.165, -3.46666667]],
                                                    [[4.44, -1.13333333]],
                                                    [[4.44, -1.13333333]]],
                                                   coords)])
def test_find_avg_v(advanced_Line_cell, advanced_Triangel_cell, list_vectors, coords):
    triangles = advanced_Triangel_cell
    cells = advanced_Line_cell + triangles
    cells_copy = cells.copy()

    for cell in cells:
        cell.find_midpoint(coords[cell.points])
        cell.find_vel()

    for vectors, triangel in zip(list_vectors, triangles):
        triangel.store_neighbours(cells)
        cells_copy.remove(triangel)
        triangel.find_avg_v(cells)

        for vector, tri_v_avgs in zip(vectors, triangel.v_avgs):
            for coord_vector, tri_v_avg in zip(vector, tri_v_avgs):
                assert tri_v_avg == pytest.approx(coord_vector)

@pytest.mark.parametrize('list_dotprods, coords', [([[-14.12800001], [-4.44], [1.8893333330000002]],
                                                  coords)])
def test_dotprods(advanced_Line_cell, advanced_Triangel_cell, list_dotprods, coords):
    triangles = advanced_Triangel_cell
    cells = advanced_Line_cell + triangles
    cells_copy = cells.copy()

    for cell in cells:
        cell.find_midpoint(coords[cell.points])
        cell.find_vel()

    for dots, triangel in zip(list_dotprods, triangles):
        triangel.store_neighbours(cells)
        cells_copy.remove(triangel)
        triangel.find_avg_v(cells)
        triangel.find_nuvecs(coords)
        triangel.dodotprods()

        for dot, tri_dot in zip(dots, triangel.dot):
            assert tri_dot == pytest.approx(dot)

            





        
    














