
from mesh_object import mesh
import functions as fc
import numpy as np

file_name = 'bay.msh'
msh = mesh(file_name)
msh.cell_midpoint()

vfelt = np.array([fc.v(tri._midpoint) for tri in msh._triangles])



#%% Making strating conditions

