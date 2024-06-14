import pytest
from src.package.mesh import *
from src.package.cellChild import *

@pytest.mark.parametrize('coords, mid', [(np.array([[1, 0], [0, 1]]), np.array([0.5, 0.5])),
                                         (np.array([[8.7, 0.6], [16.32, 78.4]]), np.array([12.51, 39.5])),
                                         (np.array([[0.3789, 542], [25, 0.76]]), np.array([12.68945, 271.38]))])
def test_cell_midpoint_Line(coords, mid):
    a = Line_cell(None, [])
    assert a.midpoint == None, 'Problem with the initiation of a Triangel_Cell`s midpoint-attribute'
    a.find_midpoint(coords)
    assert a.midpoint == pytest.approx(mid), 'Problem with Triangel_cell`s midpoint-attribute'


@pytest.mark.parametrize('mesh_file', [('simple_mesh.msh')])
def test_mesh_initiation(mesh_file):
    #mesh_file = 'simple_mesh.msh'
    msh = Mesh(mesh_file)

    for cell in msh.cells:
        assert type(cell).__name__ == 'Triangle_cell' or type(cell).__name__ == 'Line_cell', 'New type of cell'




