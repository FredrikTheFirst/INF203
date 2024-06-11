from solver_v2 import Simulation

testrun = Simulation("bay.msh")

print("Startup done")
testrun.runsim()
print("Simulation done")
testrun.photos(20)
print("Photos printed")


last_tri = testrun.msh.cells[-1]
tri = testrun.msh.cells[600]

for cft in (tri, last_tri):
    print('')
    print('id')
    print(cft.id)
    print('points')
    print(cft.points)
    print('nuvectors')
    print(cft._nuvectors)
    print('velocity')
    print(cft._v)
    print('avg velocity')
    print(cft._v_avgs)
    print('dot')
    print(cft._dot)