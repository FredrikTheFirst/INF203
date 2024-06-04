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
    return 1/3 * sum(coords)

M = np.array([[0, -1], [1, 0]])

def nvector(v1, v2, mid):
    e = v2 - v1
    nn = M @ e / np.linalg.norm(e)
    pl = v2 - mid + v1 - mid
    if nn @ pl > 0:
        return nn
    else:
        return -nn

def vvector(v1, v2, mid):
    e = v2 - v1
    nn = M @ e
    pl = v2 - mid + v1 - mid
    if nn @ pl > 0:
        return nn
    else:
        return -nn


'''
def nvectors(coords, mid):
    a, b, c = np.array(coords[0][0:2]), np.array(coords[1][0:2]), np.array(coords[2][0:2])
    e1 = b - a
    e2 = a - c
    e3 = c - b
    M = np.array([[0, -1], [1, 0]])
    n1 = M @ e1 / np.linalg.norm(e1)
    n2 = M @ e2 / np.linalg.norm(e2)
    n3 = M @ e3 / np.linalg.norm(e3)
    return np.array([n1, n2, n3])
'''