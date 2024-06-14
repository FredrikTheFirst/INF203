import pytest
import numpy as np
from src.package.functions import *

@pytest.mark.parametrize('vector, result', [(np.array([1, 1]), np.array([0.8, -1])),
                                              (np.array([1.6, -2]), np.array([-2.32, -1.6])),
                                              (np.array([-8.64, 43]), np.array([44.728, 8.64]))])
def test_v_function(vector, result):
    vel = v(vector)
    assert vel == pytest.approx(result)
    assert type(vel).__name__ == 'ndarray'

@pytest.mark.parametrize('a, b, dot, result', [([34, 6, -3, -18]),
                                               (3.65, 23.88, 7.9, 28.835),
                                               (56.4, 8.66, -0.123, -1.06518)])
def test_g_arr_function(a, b, dot, result):
    ret = g_arr(a, b, dot)
    assert ret == pytest.approx(result)
    assert type(ret) == float or type(ret) == int
"""
@pytest.mark.parametrize('coords, result', [(np.array([[1, 0], [0, 0], [0, 1]]), 0.5),
                                            (np.array([[1, 0], [0, 0], [0, 1]]), 0.5),
                                            ()])
def test_A_function(coords, result)
"""