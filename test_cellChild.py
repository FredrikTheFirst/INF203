import pytest
from src.package.cellChild import Triangle_cell, Line_cell


@pytest.mark.parametrize('id', [1, 6, 29])
def test_id(id):
    a = Line_cell(id, [])
    b = Triangle_cell(id, [])
    assert a.id == id, 'Store id'
    assert b.id == id, 'Store id'

