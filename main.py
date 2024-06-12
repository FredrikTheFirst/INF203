import toml
import argparse
from solver_v3 import *

with open('config_files\example_config_file.toml', 'r') as file:
   config = toml.load(file)
   settings = config.get('settings', {})
   geometry = config.get('geometry', {})
   io = config.get('IO', {})

   mesh_file = geometry.get('meshName')
   frames = settings.get('nSteps')
   t_start = settings.get('tStart')
   t_end = settings.get('tEnd')
   photo_steps = io.get('writeFrequency')
   dt = t_end - t_start


   sim = Simulation(mesh_file)
   sim.runsim(frames, dt)
   sim.photos(photo_steps)
























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