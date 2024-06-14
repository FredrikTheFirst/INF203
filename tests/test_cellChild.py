import pytest
from src.package.cellChild import *
from src.package.functions import *


#%% Testing cell_Child.py

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
            # Make sure the midpoints are None if find_midpoint() is not called
            assert cell.midpoint == None
            cell.find_midpoint(coords[cell.points])
            for mid_coord, cell_coord in zip(mid, cell.midpoint):
                assert cell_coord == pytest.approx(mid_coord)


@pytest.mark.parametrize('coords, mid', [(np.array([[1, 0], [0, 1]]), np.array([0.5, 0.5])),
                                         (np.array([[8.7, 0.6], [16.32, 78.4]]), np.array([12.51, 39.5])),
                                         (np.array([[0.3789, 542], [25, 0.76]]), np.array([12.68945, 271.38]))])
def test_cell_midpoint_Line(coords, mid):
    a = Line_cell(None, [])
    assert a.midpoint == None, 'Problem with the initiation of a Triangel_Cell`s midpoint-attribute'
    a.find_midpoint(coords)
    assert a.midpoint == pytest.approx(mid), 'Problem with Triangel_cell`s midpoint-attribute'










