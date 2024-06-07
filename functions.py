import numpy as np


#finner hastighet i et punkt (midtpunkt)
def v(x):
    return np.array([x[1] - 0.2*x[0], -x[0]])


#g-funksjonen
def g(a, b, v, u):
    dot = np.array(v) @ np.array(u)
    if dot > 0:
        return a * dot
    else:
        return b * dot


#finner areal
def A(coords):
    a, b, c = np.array(coords[0]), np.array(coords[1]), np.array(coords[2])
    v1 = b - a
    v2 = c - a
    return 0.5 * abs(np.cross(v1, v2))


#finner midtpunkt
def midpoint(coords):
    return sum(coords) / len(coords)


#90 graders rotasjonsmatrise
M = np.array([[0, -1], [1, 0]])

#n-vector funksjon, tar to koordinater og et triangelmidtpunkt, lager en ortonormal vektor på linja
def nvector(v1, v2, mid):
    e = v2 - v1
    nn = M @ e / np.linalg.norm(e)
    pl = v2 - mid + v1 - mid
    if nn @ pl > 0:
        return nn
    else:
        return -nn


#n-vector funksjon, tar to koordinater og et triangelmidtpunkt, lager en ortogonal vektor på linja med samme lengde som linja
def nuvector(v1, v2, mid):
    e = v2 - v1
    nn = M @ e
    pl = v1 - mid + v2 - mid
    if nn @ pl > 0:
        return nn
    else:
        return -nn

#tar koordinater til hjørnene på en trekant og gir tilbake en liste med normalvektorer på hver av kantene (ubrukelig?)
def morevectors(coords, func):
    c = np.array([e - coords[i-1] for i, e in enumerate(coords)])
    nlist = [func(np.array([0, 0]), c[i], midpoint(c)) for i in range(len(coords))]
    return np.array(nlist)

#danner startolja til hver celle
def starting_amount(x_mid, x):
    return np.exp(-np.linalg.norm(x - x_mid)**2 / 0.01)

#regner ut endringen av olje i en celle
def dOil(dt, A, g):
    return -dt/A * g
