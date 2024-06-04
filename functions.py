import numpy as np

def v(x):
    return [x[1] - 0.2*x[0], -x[0]]

def g(a, b, v, u):
    dot = np.array(v) @ np.array(u)
    if dot > 0:
        return a * dot
    else:
        return b * dot
    
def A(coords):
    a, b, c = np.array(coords[0][0:2]), np.array(coords[1][0:2]), np.array(coords[2][0:2])
    v1 = b - a
    v2 = c - a
    return 0.5 * abs(np.cross(v1, v2))

def midpoint(coords):
    return sum([point for point in coords])
