import matplotlib.pyplot as plt
import numpy as np
from functions import *
from mesh_object import *

class Simulation():
    def __init__(self, filename):
        self._filename = filename
        self.x_mid = np.array([0.35, 0.45])
        self.vfelt = np.array([v(cell.midpoint) for cell in msh.cells])
        self.u = np.array([starting_amount(self.x_mid, cell.midpoint) for cell in msh.cells])

    def runsim(self, dt):
        self.dt = dt
        Oillist = self.u.copy()
        for tri in msh.get_triangles():
            u_old = self.u[tri.id]
            tri_v = self.vfelt[tri.id]
            Flist = []
            for neigh_id in tri._neighbours_id:
                neigh = msh._cells[int(neigh_id)]
                u_old_neigh = u[neigh._cell_id]
                neigh_v = self.vfelt[neigh._cell_id]
                
                matching_points = set(tri._points) & set(neigh._points)
                matching_coords = np.array([msh._coords[point] for point in matching_points])

                nu = nuvector(matching_coords, tri._midpoint)
                v = 0.5*(tri_v + neigh_v)
                G = g(u_old, u_old_neigh, v, nu)
                F = dOil(dt, tri.area, G)
                Flist.append(F)
            Oillist[tri.id] += sum(Flist)
        #return np.array(Oillist)
        self.Oillist = Oillist

    def photo(self):
        pass

    def photos(self):
        pass

    def makevideo(self):
        pass

