import toml
import argparse
from src.package.solver import *
import re


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
      restartFile = io.get('restartFile')
      dt = t_end - t_start

      for parameter in (mesh_file, t_end):
         if parameter == None:
            raise NameError('The toml file is missing enteries')

      x = re.replace("config_files/", "", pth)
      file_name = re.replace(".toml", "", pth)

      sim = Simulation(mesh_file, file_name)
      sim.restorerun(restartFile)
      sim.runsim(frames, dt)
      sim.photos(photo_steps)
      #sim.txtprinter()
         

pth = 'config_files/example_config_file.toml'

toml_input(pth)
























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