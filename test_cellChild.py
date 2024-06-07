import pytest
from src.package import Triangle_cell, Line_cell


@pytest.mark.parametrize('id_list', [i for i in range(13)])
def test_id(id_list):
    for id in id_list:
        a = Line_cell(id, [])
        b = Triangle_cell(id, [])
        assert a.id == id
        assert b.id == id

