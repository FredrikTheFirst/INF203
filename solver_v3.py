import matplotlib.pyplot as plt
import numpy as np
from src.package.functions import *
from src.package.mesh import *
import cv2

class Simulation():
    def __init__(self, filename, midpoint = np.array([0.35, 0.45])):
        self._filename = filename
        self._x_mid = midpoint
        self._msh = Mesh(filename)

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
            u_old_ngh = ucopy[tri._neighbours_id]
            F = sum([-self._dt / tri.area * g_arr(u_old, u_ngh, dot) for u_ngh, dot in zip(u_old_ngh, tri.dot)])
            ucopy[tri.id] += F
        self._Oillist = np.vstack([self._Oillist, ucopy])

        # return np.array(ucopy)

    def runsim(self, frames = 500, time = 0.5):
        self._frames = frames
        self._time = time
        self._dt = time / frames
        
        for i in range(self._frames):
            self.genoil()
            print(f"Printed u number {i}.")

        """
        ulist = [self.u]
        for i in range(self.frames):
            ulist.append(self.genoil(ulist[-1]))
            print(f"Printed u number {i}.")
        self.Oillist = tuple(ulist)
        """

    def photo(self, i):
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
        plt.savefig(f"tmp\start_img_{i}.png")
        plt.close()

    def photos(self, intv):
        for i in range(0, self._frames, intv):
            self.photo(i)

    def makevideo(self, framerate = 5):
        
        self._fr = framerate
        # Get the list of image files in the directory
        images = [f"tmp/start_img_{i}.png" for i in range(0,25)]

        # determine dimension from first image
        frame = cv2.imread(images[0])
        height, width, layers = frame.shape

        ## Define the codec and create a VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') # or 'XVID', 'DIVX', 'mp4v' etc.
        video = cv2.VideoWriter("video.AVI", fourcc, self._fr, (width, height)) # 5 frames per second

        for image in images:
            video.write(cv2.imread(image))

        cv2.destroyAllWindows()
        video.release()

