import pytest
from src.package.mesh import *


@pytest.mark.parametrize('mesh_file', ['simple_mesh.msh'])
def init_mesh(mesh_file):
    msh = Mesh(mesh_file)
    
    for cell in msh.cells:
        assert type(cell).__name__ == 'Triangle_cell' or type(cell).__name__ == 'Line_cell', 'New type of cell'



