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
    a, b, c = np.array(coords[0]), np.array(coords[1]), np.array(coords[2])
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
    pl = v1 - mid + v2 - mid
    if nn @ pl > 0:
        return nn
    else:
        return -nn


def morevectors(coords, func):
    coordlist = coords.tolist()
    vectorset = []
    for i, item in enumerate(coordlist):
        pair = [item]
        coordlist.pop(i)
        for vector in coordlist:
            pair.append(vector)
            vectorset.append(pair)
            pair = [item]
    nlist = []
    for item in vectorset:
        nlist.append(func(np.array(item[0]), np.array(item[1]), midpoint(coords)))
    return nlist