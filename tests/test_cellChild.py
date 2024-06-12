import pytest
from src.package.cellChild import *


@pytest.mark.parametrize('id', [1, 6, 29])
def test_id(id):
    a = Line_cell(id, [])
    b = Triangle_cell(id, [])
    assert a.id == id, 'Problem with Line_cell`s id-attribute'
    assert b.id == id, 'Problem with Triangel_cell`s id-attribute'



