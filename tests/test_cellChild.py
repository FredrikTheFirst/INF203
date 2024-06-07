import pytest
from src.package import *


@pytest.mark.parametrize('id', [i for i in range(13)])
def test_id(id):
    a = Line_cell(id, [])
    b = Triangle_cell(id, [])
    assert a.id == 2, 'Problem with Line_cell`s id-attribute'
    assert b.id == id, 'Problem with Triangel_cell`s id-attribute'

