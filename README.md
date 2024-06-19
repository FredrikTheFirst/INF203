# Oil spill simulation
#### By Group32

### Description:

This project contains a package which is used to simulate oil spills. 
The package is created to see how much oil enters into fishinggrounds, and is specifically designed to simulate how much oil has entered into the fishinggrounds by bay City. The geometry of lake by bay City is given by the mesh "bay.msh". If the file main.py is used to run the simulation the results will be stored in a folder which itself is stored in the folder results (If results doesn't exist the folder will be genereted).



### Modules:

1) cellChild.py
2) cellParent.py
3) functions.py
4) mesh.py
5) solver.py

### Executing program:

You can run a simulation by running the file main.py in the command line, with the command line argument -p or --pth. This argument excpects a toml file or a folder containing one or more toml files. Examples below.
```sh
python main.py -p file.toml
```
```sh
python main.py -p folder_with_toml_files
```
If no -p or --pth argument is given the main.py code will use the file input.toml



### Structure toml file:
The toml file(s) is expected to have the structure below. Remember that if 'tStart' is not provided the simulation will not use the values from 'restartFile'.


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
logName = "log" # Name of the logfile that is prodused
<br>
writeFrequency = 10 # The frequency of output video.
<br>
restartFile = "input/solution.txt" # Name of restart File

### Tests

The folder tests contains four test file which tests if the package works correctly

1) test_cellChild.py
2) test_functions.py
3) test_mesh.py
4) test_solver

For these tests to function the files below need to be in the folder 'tests_files'

- simple.msh
- simple_mesh.msh
- simple_mesh_2.msh
- restart_file.txt
- restart_file_21.txt
- restart_file_22.txt
- restart_file_23.txt
