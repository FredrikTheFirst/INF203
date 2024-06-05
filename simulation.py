
from mesh_object import mesh
from functions import v
import numpy as np

file_name = 'bay.msh'
msh = mesh(file_name)
msh.cell_midpoint()

vfelt = np.array([v(i) for i in ])



#%% Making strating conditions

