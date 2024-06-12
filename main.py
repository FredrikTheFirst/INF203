from solver_v2 import *
import os, glob
path = 'config_files'
for filename in glob.glob(os.path.join(path, '*.txt')):
   with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
      # do your stuff