import pytest
from src.package.mesh import *
'''
This file is for testing the methodes and its attributes of the Mesh class from the module mesh
'''

@pytest.fixture
def advanced_mesh():
    '''
    Defining a list of Mesh objects

    Returns:
    list: a list of Mesh objects
    '''
    mesh = []
    mesh.append(Mesh('tests_files/simple.msh'))
    mesh.append(Mesh('tests_files/simple_mesh.msh'))
    mesh.append(Mesh('tests_files/simple_mesh_2.msh'))
    return mesh

@pytest.mark.parametrize('lengths', [([488, 8, 22])])
def test_mesh_cells_length(advanced_mesh, lengths):
    '''
    Testing if each mesh has the correct amount of cells

    Parameteres:
    advanced_mesh (list): A list containing the different meshes
    lengths (list): A list containing the correct amount of cells in each mesh
    '''
    for mesh, length in zip(advanced_mesh, lengths):
        assert len(mesh.cells) == length
        
@pytest.mark.parametrize('lengths', [([244, 5, 12])])
def test_mesh_coords_length(advanced_mesh, lengths):
    '''
    Testing if each mesh has the correct amount of points

    Parameteres:
    advanced_mesh (list): A list containing the different meshes
    lengths (list): A list containing the correct amount of points in each mesh
    '''
    for mesh, length in zip(advanced_mesh, lengths):
        assert len(mesh.coords) == length
        
@pytest.mark.parametrize('lengths', [([419, 4, 14])])
def test_mesh_triangles_length(advanced_mesh, lengths):
    '''
    Testing if each mesh has the correct amount of triangle cells

    Parameteres:
    advanced_mesh (list): A list containing the different meshes
    lengths (list): A list containing the correct amount of triangle cells in each mesh
    '''
    for mesh, length in zip(advanced_mesh, lengths):
        assert len(mesh.get_triangles()) == length


@pytest.mark.parametrize('ids, list_midpoints', [([0, 4, -1],
                                             np.array([[[-1, -0.44444444], [-1, 1.0859369e-15], [0.42458427, -0.11909357]],
                                              [[0.5, 1], [0.5, 0.83333333], [0.5, 0.16666667]],
                                              [[0.25, 1], [0.75, 0], [0.78333333, 0.48055556]]]))])
def test_mesh_midpoints(advanced_mesh, ids, list_midpoints):
    '''
    Testing if each mesh has been able to calculate the correct midpoint for some cells

    Parameteres:
    advanced_mesh (list): A list containing the different meshes
    ids (list): A list containing the id of some cells
    list_midpoints (ndarray): An array containing the correct midpoint for each cell in each mesh
    '''
    for midpoints, mesh in zip(list_midpoints, advanced_mesh):
        mesh.cell_midpoint()
        for midpoint, id in zip(midpoints, ids):
            for coor_midpoint, coor_cell_midpoint in zip(midpoint, mesh.cells[id].midpoint):
                assert coor_cell_midpoint == pytest.approx(coor_midpoint)


@pytest.mark.parametrize('ids, list_vels', [([0, 4, -1],
                                             np.array([[[-0.24444444, 1], [0.2, 1], [-0.20401043, -0.42458427]],
                                              [[0.9, -0.5], [0.73333333, -0.5], [0.06666667, -0.5]],
                                              [[0.95, -0.25], [-0.15, -0.75], [0.32388889, -0.78333333]]]))])
def test_mesh_velocities(advanced_mesh, ids, list_vels):
    '''
    Testing if each mesh has been able to calculate the correct velocities (v-attribute) for some cells

    Parameteres:
    advanced_mesh (list): A list containing the different meshes
    ids (list): A list containing the id of some cells
    list_vels (ndarray): An array containing the correct velocity for each cell in each mesh
    '''
    for vels, mesh in zip(list_vels, advanced_mesh):
        mesh.cell_midpoint()
        mesh.find_vel_vec()
        for vel, id in zip(vels, ids):
            for coor_vel, coor_cell_vel in zip(vel, mesh.cells[id].v):
                assert coor_cell_vel == pytest.approx(coor_vel)


@pytest.mark.parametrize('ids, list_areas', [([-4, -3, -1],
                                             [[0.003022201500451224, 0.0027551532226679667, 0.0024263458238418718],
                                              [0.25, 0.25, 0.25],
                                              [0.05611979166663384, 0.058593750000013226, 0.05846354166667034]])])
def test_mesh_areas(advanced_mesh, ids, list_areas):
    '''
    Testing if each mesh has been able to calculate the correct area for some triangles

    Parameteres:
    advanced_mesh (list): A list containing the different meshes
    ids (list): A list containing the id of some triangles
    list_areas (list): A list containing the correct area for each triangle in each mesh
    '''
    for areas, mesh in zip(list_areas, advanced_mesh):
        mesh.triangel_area()
        for area, id in zip(areas, ids):
            assert mesh.cells[id].area == pytest.approx(area)


@pytest.mark.parametrize('ids, list_neigh_ids', [([-4, -3, -1],
                                             np.array([[[275, 405, 483], [304, 363, 381], [383, 407, 486]],
                                              [[0, 5, 6], [4, 3, 7], [5, 6, 2]],
                                              [[17, 20, 21], [10, 12, 20], [11, 14, 18]]]))])
def test_mesh_neighbours_id(advanced_mesh, ids, list_neigh_ids):
    '''
    Testing if each mesh has been able to store the neighbours` id correctly for triangles

    Parameteres:
    advanced_mesh (list): A list containing the different meshes
    ids (list): A list containing the id of some triangles
    list_areas (ndarray): An array containing the correct neighbours_id array for each triangle in each mesh
    '''
    for neighs_ids, mesh in zip(list_neigh_ids, advanced_mesh):
        mesh.find_neighbours()
        for neigh_ids, id in zip(neighs_ids, ids):
            for neigh_id, triangle_neigh_id in zip(neigh_ids, mesh.cells[id].neighbours_id):
                assert triangle_neigh_id == neigh_id


@pytest.mark.parametrize('ids, list_neigh_points', [([-4, -3, -1],
                                             np.array([[[{29, 191}, {226, 29}, {226, 191}],
                                               [{188, 92}, {219, 188}, {219, 92}],
                                               [{225, 94}, {94, 215}, {225, 215}]],
                                              [[{0, 1}, {0, 4}, {1, 4}],
                                               [{0, 4}, {0, 3}, {3, 4}],
                                               [{3, 4}, {2, 4}, {2, 3}]],
                                              [[{8, 9}, {9, 10}, {8, 10}],
                                               [{9, 7}, {11, 7}, {9, 11}],
                                               [{10, 5}, {8, 5}, {8, 10}]]]))])
def test_mesh_neighbours_points(advanced_mesh, ids, list_neigh_points):
    '''
    Testing if each mesh has been able to store the shared points between the triangles and it`s neighbours correctly

    Parameteres:
    advanced_mesh (list): A list containing the different meshes
    ids (list): A list containing the id of some triangles
    list_areas (ndarray): An array containing the correct shared points for each triangle in each mesh
    '''
    for neighs_points, mesh in zip(list_neigh_points, advanced_mesh):
        mesh.find_neighbours()
        for neigh_points, id in zip(neighs_points, ids):
            for neigh_point, triangle_neigh_point in zip(neigh_points, mesh.cells[id].neighbours_points):
                for set_neigh_point, set_triangle_neigh_point in zip(neigh_point, triangle_neigh_point):
                    assert set_triangle_neigh_point == set_neigh_point


@pytest.mark.parametrize('ids, nuvectors_lv4', [([-4, -3, -1],
                                             np.array([[[[0.08446074, -0.0224894], [-0.06012343, -0.05555556], [-0.02433731, 0.07804495]],
                                               [[-0.07797692, -0.00362369], [0.04246173, 0.07263912], [0.03551519, -0.06901542]],
                                               [[-0.05890839, 0.04355665], [-0.01001779, -0.07496981], [0.06892617, 0.03141315]]],
                                              [[[0, 1], [-0.5, -0.5], [0.5, -0.5]],
                                               [[0.5, 0.5], [-1, -0], [0.5, -0.5]],
                                               [[-0.5, 0.5], [0.5, 0.5], [0, -1]]],
                                              [[[-0.08125, -0.33125], [-0.27291667, 0.26875], [0.35416667, 0.0625]],
                                               [[-0.125, -0.375], [-0.21875, 0.28125], [0.34375, 0.09375]],
                                               [[0.14791667, 0.35625], [0.20625, -0.29375], [-0.35416667, -0.0625]]]]))])
def test_mesh_nuvectors(advanced_mesh, ids, nuvectors_lv4):
    '''
    Testing if each mesh has been able to calculate and store the nuvectors of the triangles correctly

    Parameteres:
    advanced_mesh (list): A list containing the different meshes
    ids (list): A list containing the id of some triangles
    nuvectors_lv4 (ndarray): An array containing the nuvectors for each triangle in each mesh
    '''
    for nuvectors_lv3, mesh in zip(nuvectors_lv4, advanced_mesh):
        mesh.find_neighbours()
        mesh.cell_midpoint()
        mesh.find_nuvectors()
        for nuvectors_lv2, id in zip(nuvectors_lv3, ids):
            for nuvector, triangle_nuvectors in zip(nuvectors_lv2, mesh.cells[id].nuvectors):
                for coor_nuvector, coor_triangle_nuvectors in zip(nuvector, triangle_nuvectors):
                    assert coor_triangle_nuvectors == pytest.approx(coor_nuvector)


@pytest.mark.parametrize('ids, average_lv4', [([-4, -3, -1],
                                             np.array([[[[-0.64295477, -0.90564461], [-0.63700208, -0.85560008], [-0.60303504, -0.86973628]],
                                               [[-0.34548996, -0.19640243], [-0.32831435, -0.23234214], [-0.37400337, -0.23512687]],
                                               [[-0.18191023, -0.40645021], [-0.22915151, -0.42550802], [-0.19840747, -0.44607485]]],
                                              [[[0.81666667, -0.5], [0.6, -0.33333333], [0.53333333, -0.66666667]],
                                               [[0.6, -0.33333333], [0.48333333, -0.08333333], [0.26666667, -0.33333333]],
                                               [[0.26666667, -0.33333333], [0.2, -0.66666667], [-0.01666667, -0.5]]],
                                              [[[0.22069444, -0.55104167], [0.40888889, -0.50416667], [0.32388889, -0.67916667]],
                                               [[0.37708333, -0.171875], [0.60416667, -0.15625], [0.49069444, -0.32604167]],
                                               [[0.43180556, -0.83229167], [0.20402778, -0.84270833], [0.32388889, -0.67916667]]]]))])
def test_mesh_average_velocities(advanced_mesh, ids, average_lv4):
    '''
    Testing if each mesh has been able to calculate and store the average of the velocity (v-attribute)
    between the triangles each oftheir neighbours correctly

    Parameteres:
    advanced_mesh (list): A list containing the different meshes
    ids (list): A list containing the id of some triangles
    average_lv4 (ndarray): An array containing the average velocity between the triangles and each of their
    neighbours for each triangle in each mesh
    '''
    for average_lv3, mesh in zip(average_lv4, advanced_mesh):
        mesh.find_neighbours()
        mesh.cell_midpoint()
        mesh.find_vel_vec()
        mesh.find_vel_vec_avg()
        for average_lv2, id in zip(average_lv3, ids):
            for average, triangle_average in zip(average_lv2, mesh.cells[id].v_avgs):
                for coor_average, coor_triangle_average in zip(average, triangle_average):
                    assert coor_triangle_average == pytest.approx(coor_average)


@pytest.mark.parametrize('ids, dot_prod_lv4', [([-4, -3, -1],
                                             np.array([[[-0.03393703504028231, 0.08583208662780564, -0.053202274312507174],
                                               [0.0276519458669857, -0.03081792182423136, 0.0029445781373194143],
                                               [-0.006987573305847651, 0.03419584524891575, -0.027688085173069917]],
                                              [[-0.5, -0.1333333333333334, 0.6000000000000001],
                                               [0.1333333333333334, -0.48333333333333334, 0.3],
                                               [-0.3, -0.2333333333333334, 0.5]],
                                              [[0.16460112847261654, -0.24708738425922766, 0.072262731481178],
                                               [0.017317708333848575, -0.17610677083347065, 0.1381098090271906],
                                               [-0.23263266782487388, 0.2896263020835187, -0.072262731481178]]]))])
def test_mesh_dot_products(advanced_mesh, ids, dot_prod_lv4):
    '''
    Testing if each mesh has been able to calculate and store dotproducts of each triangle correctly

    Parameteres:
    advanced_mesh (list): A list containing the different meshes
    ids (list): A list containing the id of some triangles
    dot_prod_lv4 (ndarray): An array containing the average velocity between the triangles and each of their
    neighbours for each triangle in each mesh
    '''
    for dot_prod_lv3, mesh in zip(dot_prod_lv4, advanced_mesh):
        mesh.find_neighbours()
        mesh.cell_midpoint()
        mesh.find_vel_vec()
        mesh.find_vel_vec_avg()
        for dot_prod_lv2, id in zip(dot_prod_lv3, ids):
            for dot_prod, triangle_dot_prods in zip(dot_prod_lv2, mesh.cells[id].dot):
                assert triangle_dot_prods == pytest.approx(dot_prod)