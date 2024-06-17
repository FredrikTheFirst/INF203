import toml
import argparse
from src.package.solver import *
import re
from pathlib import Path


def toml_input(pth):
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
      
      if t_start == None:
         t_start = 0
      
      x = re.sub("(.)*(/|\\\\)", "", pth)
      file_name = re.sub(".toml", "", x)

      outer_results_folder = 'results'
      if not Path(outer_results_folder).exists():
         Path(outer_results_folder).mkdir()
      
      resfold = outer_results_folder+'/'+file_name
      if Path(resfold).exists():
         recursive_folder_deletion(Path(resfold))
      Path(resfold).mkdir()

      sim = Simulation(mesh_file, resfold, boarders)
      if restartFile != None:
         sim.restorerun(restartFile)
      print(f"Starting oil simulation for file {x}")
      sim.runsim(frames, t_start, t_end)
      print("Generated all oil for the given time interval")
      sim.fishinggrounds()
      sim.photo(sim._frames-1, 'final_oil_distrubution')
      print("A photo of the final step has been generated")

      if photo_steps != None:
         Path(resfold+'/frames_in_video').mkdir()
         sim.photos(photo_steps)
         sim.makevideo()
         print("A video of the simulation has been generated")
      else:
         print("No video was generated, because no writeFrequency parameter was given in the toml-file")

      saveFile = input("What would you like to name the solution-file of your code? (leave blank for no solution-file): ")
      if len(saveFile) != 0:
         sim.txtprinter(saveFile)
         print("A solution file was added to the input-folder")
      else:
         print("No solution file was added to the input folder")
      
      if log_name == None:
         log_name = 'logfile'
      sim.make_log(log_name)

      print("A log of the simulation has been written")
      print("Simulation done!")

def parse_input():
    parser = argparse.ArgumentParser(description='Use this program to simulate an oil spill')
    parser.add_argument('-p', '--pth', default='“input.toml', help='Prvide a toml file or a folder containing one or multiple toml files')

    args = parser.parse_args()
    pth = args.pth
    return pth

def checkfile(pth):
   if not Path(pth).exists():
      raise NameError("Path you have entered doesn't exist")
   if Path(pth).is_file():
      if re.search('.toml$', pth) == None:
         raise TypeError('Was not given a toml file')
      toml_input(pth)
   if Path(pth).is_dir() == True:
      p = Path(pth).iterdir()
      p = [str(x) for x in p if x.is_file()]
      tomlfils = [fil for fil in p if re.search('.toml$', fil) != None]
      if len(tomlfils) == 0:
         raise TypeError('The given folder contains no toml files')
      print(tomlfils)
      for file in tomlfils:
         toml_input(file)

def recursive_folder_deletion(pth):
   if pth.is_file():
      pth.unlink()
   else:
      for child in pth.iterdir():
         recursive_folder_deletion(child)
      pth.rmdir()


if __name__ == '__main__':
   pth = parse_input()
   checkfile(pth)


