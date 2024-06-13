from src.package.solver import Simulation
import numpy as np

testrun = Simulation("bay.msh")

print("Startup done")

testrun.runsim(frames=100)
print("Simulation done")
"""
testrun.photos(50)
print("Photos printed")
"""
testrun.fishinggrounds()
print(testrun._oil_fishinggrounds)
print(np.shape(testrun._oil_fishinggrounds))
testrun.make_log('noe_123')
print('made log')

