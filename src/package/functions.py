import numpy as np
'''
This module provides a bunch of functions
'''

def v(x):
    '''
    Find the velocity at a given point

    Parameters:
    x (ndarray): A 2D position vector

    Returns:
    ndarray: The velocity at position x
    '''
    return np.array([x[1] - 0.2*x[0], -x[0]])


def g_arr(a, b, dot):
    '''
    The g-function from the task description

    Parameters:
    a (float): The first number, positive
    b (float): The second number, positive
    dot (float): The deciding number

    Returns:
    float: The product of a and dot (if dot is positive), or b and dot (if dot is negative)
    '''
    if dot > 0:
        return a * dot
    else:
        return b * dot


def A(coords):
    '''
    Calculate the area of a triangle

    Parameteres:
    coords (ndarray): A matrix containing the 2D position vector of the corners of a triangle

    Returns:
    float: The area of the triangle
    '''
    a, b, c = np.array(coords[0]), np.array(coords[1]), np.array(coords[2])
    v1 = b - a
    v2 = c - a
    return 0.5 * abs(np.cross(v1, v2))


def midpoint(coords):
    '''
    Calculates the midpoint of a geometric figure

    Parameters:
    coords (ndarray): A matrix containing the 2D position vector of the corners of the figure

    Returns:
    float: The midpoint of the geometric figure
    '''
    return sum(coords) / len(coords)

# The 90 degree clockwise rotation matrix
M = np.array([[0, -1], [1, 0]])

def nuvector(v, mid):
    '''
    Calculating the outward pointing vector for a side of a polynomial with the absolute vale equal to the length of the side 

    Parameters:
    v (ndarray): A matrix containing the 2D position vector for the coorners of the side
    mid (ndarray): The 2D position vector for the midpoint of the polynomial
    M (ndarray): The 90 degree clockwise rotation matrix 

    Returns:
    ndarray: The outward pointing vector for the side
    '''
    v1, v2 = v[0], v[1]
    e = v2 - v1
    nn = M @ e
    pl = v1 - mid
    if nn @ pl > 0:
        return nn
    else:
        return -nn


def starting_amount(x_mid, x):
    '''
    Calculating the starting amount of oil at a point

    Parameters:
    x_mid (ndarray): The 2D position vector for the center of the oil spill
    x (ndarray): The 2D position vector for a point

    Returns
    float: Amount of oil at position x
    '''
    return np.exp(-np.linalg.norm(x - x_mid)**2 / 0.01)