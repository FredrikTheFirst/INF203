import toml
import argparse
from src.package.solver import *


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
      dt = t_end - t_start

      for parameter in (mesh_file, t_end):
         if parameter == None:
            raise NameError('The toml file is missing enteries')

      sim = Simulation(mesh_file)
      sim.restorerun('input/solution.txt')
      sim.runsim(frames, t_start, t_end)
      sim.fishinggrounds()
      sim.photos(photo_steps)
      sim.make_log()
      #sim.txtprinter()
         

# pth = 'config_files\example_config_file.toml'

# toml_input(pth)

def parse_input():
    parser = argparse.ArgumentParser(description='Use this program to simulate an oil spill')
    parser.add_argument('-f', '--file', default='“input.toml', help='Prvide a toml file or a folder containing a toml file')

    args = parser.parse_args()
    file = args.file
    return file

file = parse_input()
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