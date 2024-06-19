# Group32PettersenHaugen
####

### Description:

This project contains a package which is used to simulate an oil spill.
To use this package to simulate an oil spill you can run the main.py file with the command line.



### Modules:

1) cellChild.py
2) cellParent.py
3) functions.py
4) mesh.py
5) solver.py

Executing program:

To use this package to simulate an oil spill you can run the main.py file with the command line.
For it to main.py to run you need an toml file with the right structure

Structure toml file:

[settings]
<br>
nSteps = 501 # `Required`. Number of time steps
<br>
tStart = 0.1 # Start time
<br>
tEnd = 0.6 # `Required` End time

[geometry]
<br>
meshName = "bay.msh" # `Required` Name of mesh fil
<br>
boarders = [[0.0, 0.45], [0.0, 0.2]] # `Required` Boarders of the fishinggrounds

[IO]
<br>
logName = "log" # Name of logfile that are 
<br>
writeFrequency = 10 # The frequency of vido of simulation
<br>
restartFile = "input/solution.txt"

Tests

