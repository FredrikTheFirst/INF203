import toml
import argparse
import re
from pathlib import Path
from src.package.solver import *
'''
This file is run to make an simulation of an oils pill
'''


def toml_input(pth):
   '''
   Runs a simulation with specifications from a toml file

   Parameters:
   pth (string): The path to a toml file
   '''
   with open(pth, 'r') as file:
      config = toml.load(file)

      settings = config.get('settings')
      geometry = config.get('geometry')
      io = config.get('IO')


      for parameter in (settings, geometry):
         if parameter == None:
            raise NameError('The structure of the toml file is not as expected')
      
      mesh_file = geometry.get('meshName')
      frames = settings.get('nSteps')
      t_start = settings.get('tStart')
      t_end = settings.get('tEnd')
      photo_steps = io.get('writeFrequency')
      boarders = geometry.get('boarders')
      restartFile = io.get('restartFile')
      log_name = io.get('logName')


      for parameter in (mesh_file, frames, t_end, boarders):
         if parameter == None:
            raise NameError('The toml file is missing enteries')

      if t_end < t_start:
         raise ValueError('"t_end" should be larger then "t_start" in the toml file')
      
      if not Path(mesh_file).is_file():
         raise ImportError('Could not find the mesh file')

      # Getting the name of the toml file
      file_name = only_name(pth)

      # Create a folder called results if it dosn`t already exists
      outer_results_folder = 'results'
      if not Path(outer_results_folder).exists():
         Path(outer_results_folder).mkdir()
      # Creating a folder to store the results of the simulation
      resfold = outer_results_folder+'/'+file_name
      if Path(resfold).exists():
         recursive_folder_deletion(Path(resfold))
      Path(resfold).mkdir()

      # Begin simulation
      sim = Simulation(mesh_file, resfold, boarders)
      # If we have been given a start time we throw an error if we can`t find the restart file
      if t_start != None:
         if restartFile == None or not Path(restartFile).is_file():
            raise ImportError('Could not find the restart file')
         else:
            sim.restorerun(restartFile)
      else:
         t_start = 0

      print(f"Starting oil simulation for file {pth}")
      # Running the simulation
      sim.runsim(frames, t_start, t_end)
      print("Generated all oil for the given time interval")
      # Calculating the amount of oil in the fishinggrounds
      sim.fishinggrounds()
      # Getting the last photo from the simulation
      sim.photo(frames-1, 'final_oil_distrubution')
      print("A photo of the final step has been generated")

      # If we have been given the parameter writeFrequency we make photos which we can make a video from
      if photo_steps != None:
         Path(resfold+'/frames_in_video').mkdir()
         sim.photos(photo_steps)
         sim.makevideo()
         print("A video of the simulation has been generated")
      else:
         print("No video was generated, because no writeFrequency parameter was given in the toml-file")

      # User writing in a name for the file containing the final oil disturbution if they want that file
      saveFile = input("What would you like to name the solution-file of your code? (leave blank for no solution-file): ")
      saveFile = only_name(saveFile)
      if len(saveFile) != 0:
         sim.txtprinter(saveFile+'.txt')
         print("A solution file was added to the input-folder")
      else:
         print("No solution file was added to the input folder")
      
      # Making a log of the simulation
      if log_name == None:
         log_name = 'logfile'
      log_name = only_name(log_name)+'.log'
      sim.make_log(log_name)

      print("A log of the simulation has been written")
      print("Simulation done!")

def parse_input():
    '''
    Reading the input from the command line

    Returns:
    string: A path which was defined by the command line input
    '''
    parser = argparse.ArgumentParser(description='Use this program to simulate an oil spill')
    parser.add_argument('-p', '--pth', default='input.toml', help='Prvide a toml file or a folder containing one or multiple toml files')

    args = parser.parse_args()
    pth = args.pth
    return pth

def only_name(string):
   '''
   A function that removes unwanted parts from a string

   Parameters:
   string (string): A string which we want changed

   Returns:
   String: A string without '/', '\\' and '.'
   '''
   string = re.sub("(.)*(/|\\\\)", "", string)
   string = re.sub("(\\..*)*", "", string)
   return string

def checkfile(pth):
   '''
   Verify a path to see if it can be sent on

   Parameteres:
   pth (string): A posible path which leads to a toml file

   Returns:
   string: A path to a toml file
   '''
   # Throw error if the path dosn`t exists
   if not Path(pth).exists():
      raise NameError("Path you have entered doesn't exist")
   # Check if path is an toml file
   if Path(pth).is_file():
      if re.search('.toml$', pth) == None:
         raise TypeError('Was not given a toml file')
      toml_input(pth)
   # Check if path contains one or more tonm file(s) one leve down
   if Path(pth).is_dir():
      p = Path(pth).iterdir()
      p = [str(x) for x in p if x.is_file()]
      tomlfils = [fil for fil in p if re.search('.toml$', fil) != None]
      # Throw error if folder dosn`t contain toml file
      if len(tomlfils) == 0:
         raise TypeError('The given folder contains no toml files')
      for file in tomlfils:
         toml_input(file)

def recursive_folder_deletion(pth):
   '''
   Deletes a folder and all it contents

   Parameters:
   pth (string): The path to a folder
   '''
   if pth.is_file():
      pth.unlink()
   else:
      for child in pth.iterdir():
         recursive_folder_deletion(child)
      pth.rmdir()


if __name__ == '__main__':
   '''
   What happens if file is run
   '''
   pth = parse_input()
   checkfile(pth)


