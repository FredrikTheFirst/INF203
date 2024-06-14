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

@pytest.mark.parametrize('coords, result', [(np.array([[1, 0], [0, 0], [0, 1]]), 0.5),
                                            (np.array([[0.356, 5.34], [1.65, 0.24], [9.8, 9.9]]), 27.03252),
                                            (np.array([[7.65, 3.33], [53.8, 8], [99, 5.5]]), 163.2295)])
def test_A_function(coords, result):
    area = A(coords)
    assert area == pytest.approx(result)

@pytest.mark.parametrize('coords, result', [(np.array([[1.34, 6.5], [87, 56]]), [44.17, 31.25]),
                                            (np.array([[45, 7.7], [23.45, 8.7], [34.5, 23]]), [2059/60, 197/15]),
                                            (np.array([[3.5, 4.5], [9.34, 56], [5.7, 5.8]]), [6.18, 22.1])])
def test_midpoint_function(coords, result):
    mid_point = midpoint(coords, result)
    for mid_coor, res_coor in zip(mid_point, result):
        assert mid_coor == pytest.approx(res_coor)

@pytest.mark.parametrize('vec, mid, result', [(np.array([[1, 0], [0, 1]]), [0.5, 0.5], np.array([1, 1])),
                                              (np.array([[3.67, 1.45], [0.78, 19.3]]), [1.5, 0.23], np.array([17.85, 2.89])),
                                              (np.array([[7.9, 0], [67.8, 2.56]]), [5.7, 0.5], np.array([2.56, -59.9]))])
def test_nuvector_function(vec, mid, result):
    v = nuvector(vec, mid)
    for v_coor, res_coor in zip(v, result):
        assert v_coor == pytest.approx(res_coor)

@pytest.mark.parametrize('x_mid, x, result', [(np.array([0.32, 1.4]), np.array([0.32, 1.4]), 1),
                                              (np.array([0.47, 1.8]), np.array([0.5, 1.7]), 0.3362164937067328),
                                              (np.array([5.2, 0.93]), np.array([5, 0.75]), 0.0007173117601093084)])
def test_starting_amount_function(x_mid, x, result):
    amount = starting_amount(x_mid, x)
    assert amount == pytest.approx(result)
