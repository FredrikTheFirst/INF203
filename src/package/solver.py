import matplotlib.pyplot as plt
import numpy as np
import cv2
import logging as log
from src.package.functions import *
from src.package.mesh import *

class Simulation():
    def __init__(self, filename, resfold, boarders, midpoint = np.array([0.35, 0.45])):
        self._filename = filename
        self._x_mid = midpoint
        self._boarders = boarders
        self._msh = Mesh(filename)
        self._oil_fishinggrounds = np.array([])
        self._intv = None
        self._restartFile = None
        self._resfoldname = resfold

        self._msh.cell_midpoint()
        self._msh.triangel_area()
        self._msh.find_neighbours()
        self._msh.find_nuvectors()
        self._msh.find_vel_vec()
        self._msh.find_vel_vec_avg()
        self._msh.calc_dot_prod()

        self._Oillist = np.array([[starting_amount(self._x_mid, cell.midpoint) for cell in self._msh.cells]])

    def genoil(self):
        ucopy = self._Oillist[-1].copy()
        for tri in self._msh.get_triangles():
            u_old = ucopy[tri.id]
            u_old_ngh = ucopy[tri.neighbours_id]

            # u_old_array = np.array([u_old for i in range(3)])

            # dot_list = [g_arr(u_old, u_ngh, pd, nd) for u_ngh, pd, nd in (u_old_ngh, tri._posdot, tri._negdot)]

            # F = -self._dt / tri.area * sum(g_arr(u_old_array, u_old_ngh, tri._posdot, tri._negdot))

            # F = -self._dt / tri.area * sum(u_old * tri._posdot + u_old_ngh * tri._negdot)

            F = -self._dt / tri.area * sum([g_arr(u_old, u_ngh, dot) for u_ngh, dot in zip(u_old_ngh, tri.dot)])
            ucopy[tri.id] += F
        self._Oillist = np.vstack([self._Oillist, ucopy])

        # return np.array(ucopy)

    def runsim(self, frames = 500, t_start=0, t_end=0.5):
        self._frames = frames
        self._t_start = t_start
        self._t_end = t_end
        self._time = t_end-t_start
        self._dt = self._time / frames
        
        for i in range(self._frames):
            self.genoil()

        """
        ulist = [self.u]
        for i in range(self.frames):
            ulist.append(self.genoil(ulist[-1]))
            print(f"Printed u number {i}.")
        self.Oillist = tuple(ulist)
        """

    def fishinggrounds(self):
        included_ids = np.array([], dtype='int32')

        for cell in self._msh.cells:
            include = False
            for coor, limit in zip(cell.midpoint, self._boarders):
                if coor > limit[0] and coor < limit[1]:
                    include = True
            if include:
                included_ids = np.append(included_ids, cell.id)
        self._oil_fishinggrounds = np.array([sum(oil[included_ids]) for oil in self._Oillist])



    def photo(self, i, img_name):
        el = self._Oillist[i]
        
        plt.figure()

        # Create the colormap
        sm = plt.cm.ScalarMappable(cmap='viridis')
        sm.set_array([el])
        umax = max(el)
        umin = min(el)

        # Add colorbar using a separate axis
        cbar_ax = plt.gca().inset_axes([1, 0, 0.05, 1]) # adjust position and size as needed
        plt.colorbar(sm, cax=cbar_ax, label='label3')

        # Need for-loop
        for cell, amount in zip(self._msh.cells, el):
            coords = self._msh.coords[cell.points]
            plt.gca().add_patch(plt.Polygon(coords, color=plt.cm.viridis((amount - umin)/(umax - umin)), alpha=0.9))


        # plt.gca().add_patch(plt.Polygon(triangle1, color=plt.cm.viridis((u[0] - umin)/(umax - umin)), alpha=0.9))
        # plt.gca().add_patch(plt.Polygon(triangle2, color=plt.cm.viridis((u[1] - umin)/(umax - umin)), alpha=0.9))

        # Add labels to axes
        plt.xlabel('label1')
        plt.ylabel('label2')
        plt.xlim(0, 1) # set the x-axis limits
        plt.ylim(0, 1) # set the y-axis limits
        plt.gca().set_aspect('equal')

        # Show plot
        plt.savefig(f"{self._resfoldname}/{img_name}")
        plt.close()

    def photos(self, intv):
        self._intv = intv
        for i in range(0, self._frames, intv):
            self.photo(i, f'frames_in_video/img_{i}.png')
            print(f"Generated photo for step {i}")


    def makevideo(self):
        self._framerate = (self._frames / self._intv) / (self._time * 10)
        # Get the list of image files in the directory
        images = [f"{self._resfoldname}/frames_in_video/img_{i}.png" for i in range(0, self._frames, self._intv)]
        # determine dimension from first image
        frame = cv2.imread(images[0])
        height, width, layers = frame.shape

        ## Define the codec and create a VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') # or 'XVID', 'DIVX', 'mp4v' etc.
        video = cv2.VideoWriter(f"{self._resfoldname}/video.AVI", fourcc, self._framerate, (width, height))

        for image in images:
            video.write(cv2.imread(image))

        cv2.destroyAllWindows()
        video.release()
    
    def make_log(self, logfile='logfile.log'):
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
        with open(self._resfoldname+'/'+filename, 'w') as writer:
            for i in self._Oillist[-1]:
                writer.write(f"{i}\n")
    
    def restorerun(self, restartFile):
        self._restartFile = restartFile
        with open(restartFile, 'r') as file:
            startoil = file.readlines()
            try:
                self._Oillist = np.array([[float(line) for line in startoil]])
            except:
                raise TypeError('There is something wrong with the restartFile')