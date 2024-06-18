import matplotlib.pyplot as plt
import numpy as np
import cv2
import logging as log
from src.package.functions import *
from src.package.mesh import *
'''
This module is used to run a simulation of the 
'''

class Simulation():
    '''
    This object runs an oil simulation as well as storing paramteres of the simulation
    '''
    def __init__(self, filename, resfold, boarders, midpoint = np.array([0.35, 0.45])):
        '''
        This method is storeing the parameters as attributes as well as defining other attributes

        Paramterers
        filename (string): The name of the .msh file that containes the geometry of the simulation
        resfold (string): The name and relative path of the folder which the results of the simulation is going to be stored in
        boarders (list): A list containing the the boarders of the fishing grounds
        midpoint (ndarray): An array which descripes the episenter of the oil spill
        '''
        self._filename = filename
        self._x_mid = midpoint
        self._boarders = boarders
        self._msh = Mesh(filename)
        self._resfoldname = resfold

        # Establishing attributes which are empty/None to be used later
        self._oil_fishinggrounds = np.array([])
        self._intv = None
        self._restartFile = None
        self._frames = None
        self._t_start = None
        self._t_end = None
        self._time = None
        self._dt = None

        # Calling the methodes of the self._msh object
        self._msh.cell_midpoint()
        self._msh.triangel_area()
        self._msh.find_neighbours()
        self._msh.find_nuvectors()
        self._msh.find_vel_vec()
        self._msh.find_vel_vec_avg()
        self._msh.calc_dot_prod()

        # Calculating the starting amount of oil in each cell
        self._Oillist = np.array([[starting_amount(self._x_mid, cell.midpoint) for cell in self._msh.cells]])

    def genoil(self):
        '''
        Generating the amount of oil in each cell for a iteration of the simulation
        '''

        # Copy an array of the oil from the last iteration
        ucopy = self._Oillist[-1].copy()
        for tri in self._msh.get_triangles():
            # Amount of oil in the triangle from the previous iteration
            u_old = ucopy[tri.id]
            # Amount of oil in the neighbouring cells from the previous iteration
            u_old_ngh = ucopy[tri.neighbours_id]
            # The total change of oil in the triangle
            F = -self._dt / tri.area * sum([g_arr(u_old, u_ngh, dot) for u_ngh, dot in zip(u_old_ngh, tri.dot)])
            ucopy[tri.id] += F
        # Storing the amount of oil in each cell from this iteration
        self._Oillist = np.vstack([self._Oillist, ucopy])

    def runsim(self, frames = 500, t_start=0, t_end=0.5):
        '''
        Establishing some attributes based on the given parameters as well as calling the method
        which generates the next iteration

        Parameters:
        frames (int): The amount of steps in which are going to be simulated
        t_start (float): The start time of the simulation
        t_end (float): The end time of the simulation
        '''
        self._frames = frames
        self._t_start = t_start
        self._t_end = t_end
        self._time = t_end-t_start
        self._dt = self._time / frames
        
        for i in range(self._frames):
            self.genoil()

    def fishinggrounds(self):
        '''
        Calculating the amount of oil in the fishing grounds for each iteration of the simulation
        '''

        # Storing the ids of the cells in the fishinggrounds
        included_ids = np.array([], dtype='int32')
        for cell in self._msh.cells:
            include = True
            for coor, limit in zip(cell.midpoint, self._boarders):
                if coor < limit[0] or coor > limit[1]:
                    include = False
            if include:
                included_ids = np.append(included_ids, cell.id)
        # Storing the amount of oil in the fishing grounds for each iteration of the simulation
        self._oil_fishinggrounds = np.array([sum(oil[included_ids]) for oil in self._Oillist])



    def photo(self, i, img_name):
        '''
        Generate an image from an iteration of the simulation

        Parameteres:
        i (int): The iteration at which the data in the image is from
        img_name (string): The name and path of the image
        '''

        oil = self._Oillist[i]
        
        plt.figure()

        # Create the colormap
        sm = plt.cm.ScalarMappable(cmap='viridis')
        sm.set_array([oil])
        umax = max(oil)
        umin = min(oil)

        # Add colorbar using a separate axis
        cbar_ax = plt.gca().inset_axes([1, 0, 0.05, 1]) # adjust position and size as needed
        plt.colorbar(sm, cax=cbar_ax, label='Amount of oil')

        # Coloring the cell
        for cell, amount in zip(self._msh.cells, oil):
            coords = self._msh.coords[cell.points]
            plt.gca().add_patch(plt.Polygon(coords, color=plt.cm.viridis((amount - umin)/(umax - umin)), alpha=0.9))

        # Add labels to axes
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.xlim(0, 1) # set the x-axis limits
        plt.ylim(0, 1) # set the y-axis limits
        plt.gca().set_aspect('equal')

        # Show and save plot
        plt.savefig(f"{self._resfoldname}/{img_name}")
        plt.close()

    def photos(self, intv):
        '''
        Calling the photo generating method with an timestep interval

        Parameteres
        intv (int): interval between photos generated
        '''
        self._intv = intv
        for i in range(0, self._frames, intv):
            self.photo(i, f'frames_in_video/img_{i}.png')
            print(f"Generated photo for timestep {i}")


    def makevideo(self):
        '''
        Generating a video of the oil distrubution over time
        '''
        # Defining the framerate
        self._framerate = (self._frames / self._intv) / (self._time * 10)
        # Get the list of image files in the directory
        images = [f"{self._resfoldname}/frames_in_video/img_{i}.png" for i in range(0, self._frames, self._intv)]
        # determine dimension from first image
        frame = cv2.imread(images[0])
        height, width, layers = frame.shape

        # Define the codec and create a VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') # or 'XVID', 'DIVX', 'mp4v' etc.
        video = cv2.VideoWriter(f"{self._resfoldname}/oil_distrubution.mp4", fourcc, self._framerate, (width, height))

        for image in images:
            video.write(cv2.imread(image))

        cv2.destroyAllWindows()
        video.release()
    
    def make_log(self, logfile='logfile.log'):
        '''
        Writing a log for the simulation

        Parameters:
        logfile (string): The name of the logfile
        '''
        logger = log.getLogger(__name__)
        logplace = f"{self._resfoldname}/{logfile}"
        handler = log.FileHandler(str(logplace), mode='w')
        formatter = log.Formatter('%(asctime)s - %(levelname)s:\n%(message)s')

        information = f'''
nSteps: {self._frames}
tStart: {self._t_start}
tEnd: {self._t_end}
meshName: {self._filename}
boarders: {self._boarders}'''
        
        if self._intv != None:
            information += f'''
writeFrequency = {self._intv}'''
        
        if self._restartFile != None:
            information += f'''
restartFile = {self._restartFile}'''

        information += '''

Oil in fishingrounds at time:
'''
        for i in range(self._frames+1):
            step = self._t_start + i * self._dt
            information += f'''
t = {step:#.5g}:     {self._oil_fishinggrounds[i]:#.5g}'''

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(log.INFO)
        logger.info(information)

    def txtprinter(self, filename):
        '''
        Printing out the final oil distrubution

        Parameteres:
        filename (string): The name of the file which the distrubution is goinig to be printed to
        '''
        with open(self._resfoldname+'/'+filename, 'w') as writer:
            for i in self._Oillist[-1]:
                writer.write(f"{i}\n")
    
    def restorerun(self, restartFile):
        '''
        Storing the starting amount of oil for each cell from a text file

        Parameteres:
        restartFile (string): The name of the file which the oil distrubution is gathered from
        '''
        self._restartFile = restartFile
        with open(restartFile, 'r') as file:
            startoil = file.readlines()
            try:
                self._Oillist = np.array([[float(line) for line in startoil]])
                assert len(self._msh.cells) == len(self._Oillist[0])
            except:
                raise TypeError('There is something wrong with the restartFile')