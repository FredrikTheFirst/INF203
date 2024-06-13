import pytest
from src.package.cellChild import *


@pytest.mark.parametrize('id', [0, 6, 29])
def test_id(id):
    a = Line_cell(id, [])
    b = Triangle_cell(id, [])
    assert a.id == id, 'Problem with Line_cell`s id-attribute'
    assert b.id == id, 'Problem with Triangel_cell`s id-attribute'

@pytest.mark.parametrize('points', [[4, 6, 1], [13, 54, 23], [43, 12, 23]])
def test_points(points):
    a = Line_cell(None, points)
    b = Triangle_cell(None, points)
    assert a.points == points, 'Problem with Line_cell`s points-attribute'
    assert b.points == points, 'Problem with Triangel_cell`s points-attribute'

# @pytest.mark.parametrize('coords, mid', [[np.array([1, 0], [0, 1], [0, 0]), n], ])








