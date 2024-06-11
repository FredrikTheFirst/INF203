from mesh_object import *

fil = 'bay.msh'
testrun = Mesh(fil)

testrun.get_triangles()
testrun.cell_midpoint()
testrun.find_neighbours()
testrun.find_nuvectors()
testrun.find_velocity()