import toml
import argparse
from src.package.solver import *
import re
from pathlib import Path


def toml_input(pth):
   with open(pth, 'r') as file:
      config = toml.load(file)

      settings = config.get('settings', {})
      geometry = config.get('geometry', {})
      io = config.get('IO', {})

      for parameter in (settings, geometry, io):
         if parameter == {}:
            raise NameError('The structure of the toml file is not as expected')
      
      mesh_file = geometry.get('meshName')
      frames = settings.get('nSteps')
      t_start = settings.get('tStart')
      t_end = settings.get('tEnd')
      photo_steps = io.get('writeFrequency')
      boarders = geometry.get('boarders')
      restartFile = io.get('restartFile')
      log_name = io.get('logName')


      for parameter in (mesh_file, t_end, boarders):
         if parameter == None:
            raise NameError('The toml file is missing enteries')

      x = re.sub("config_files/", "", pth)
      file_name = re.sub(".toml", "", x)

      sim = Simulation(mesh_file, file_name)
      sim.restorerun(restartFile)
      sim.runsim(frames, t_start, t_end)
      print("Generated all oil for the given time interval")
      sim.fishinggrounds()
      sim.photo(sim._frames-1)
      print("A photo of the final step has been generated")
      sim.photos(photo_steps)

      if photo_steps:
         sim.makevideo()
         print("A video of the simulation has been generated")
      else:
         print("No video was generated, because no writeFrequency parameter was given in the input toml-file")

      saveFile = input("What would you like to name the solution-file of your code? (leave blank for no solution-file): ")
      if len(saveFile) != 0:
         sim.txtprinter()
         print("A solution file was added to the input-folder")
      else:
         print("No solution file was added to the input folder")
      
      sim.make_log()
      print("A log of the simulation has been written")
      print("Simulation done!")


pth = input("Enter the path of your config file here, or the path of your folder of toml-files (leave blank for the example file): ")
if len(pth) == 0:
   pth = 'config_files/example_config_file.toml'

if os.path.exists(pth) == False:
   print("Path you have entered doesn't exist")
if os.path.isfile(pth) == True:
   toml_input(pth)
if os.path.isdir(pth) == True:
   p = Path(pth).glob('**/*')
   tomlfils = [fil for fil in p if type(fil) == toml]
   for file in tomlfils:
      toml_input(file)























'''from solver_v2 import *
path = 'config_files'
import os 

dir_list = os.listdir(path) 
   
for file in dir_list:
    with open(f"{path}\{file}", 'r') as conf:
      content = conf.readlines()
      items = []
      for line in content:
         print(line)
         if '=' in line:
            items.append(line.strip("\n"))

for ting in items:
   eval(ting)'''