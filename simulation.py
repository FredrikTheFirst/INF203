import matplotlib.pyplot as plt
import numpy as np
from functions import *
from mesh_object import *
import cv2

class Simulation():
    def __init__(self, filename, midpoint = np.array([0.35, 0.45])):
        self._filename = filename
        self.x_mid = midpoint
        self.msh = Mesh(filename)
        self.vfelt = np.array([v(cell.midpoint) for cell in self.msh.cells])
        self.u = np.array([starting_amount(self.x_mid, cell.midpoint) for cell in self.msh.cells])

    def runsim(self, frames = 500, time = 0.5):
        self.frames = frames
        self.dt = time/frames
        Oillist = self.u.copy()
        for tri in self.msh.get_triangles():
            u_old = self.u[tri.id]
            tri_v = self.vfelt[tri.id]
            Flist = []
            for neigh_id in tri._neighbours_id:
                neigh = self.msh._cells[int(neigh_id)]
                u_old_neigh = self.u[neigh._cell_id]
                neigh_v = self.vfelt[neigh._cell_id]
                
                matching_points = set(tri._points) & set(neigh._points)
                matching_coords = np.array([self.msh._coords[point] for point in matching_points])

                nu = nuvector(matching_coords, tri._midpoint)
                v = 0.5*(tri_v + neigh_v)
                G = g(u_old, u_old_neigh, v, nu)
                F = dOil(self.dt, tri.area, G)
                Flist.append(F)
            Oillist[tri.id] += sum(Flist)
        #return np.array(Oillist)
        self.Oillist = Oillist

    def photo(self, i):
        el = self.Oillist[i]
        
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
        for cell, amount in zip(self.msh.cells, el):
            coords = self.msh.coords[cell.points]
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
        for i in range(0, self.frames, intv):
            self.photo(i)

    def makevideo(self, framerate = 5):
        
        self.fr = framerate
        # Get the list of image files in the directory
        images = [f"tmp/start_img_{i}.png" for i in range(0,25)]

        # determine dimension from first image
        frame = cv2.imread(images[0])
        height, width, layers = frame.shape

        ## Define the codec and create a VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') # or 'XVID', 'DIVX', 'mp4v' etc.
        video = cv2.VideoWriter("video.AVI", fourcc, self.fr, (width, height)) # 5 frames per second

        for image in images:
            video.write(cv2.imread(image))

        cv2.destroyAllWindows()
        video.release()

