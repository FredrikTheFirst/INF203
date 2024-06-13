from src.package.solver import Simulation

testrun = Simulation("bay.msh")

print("Startup done")

testrun.runsim()
print("Simulation done")
testrun.photos(499)
"""
print("Photos printed")
testrun.make_log('noe_123')
"""
print('made log')

