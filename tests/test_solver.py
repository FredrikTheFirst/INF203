import pytest
from src.package.solver import *
'''
This file is for testing the methodes and attributes of the Simulation class from the module solver
'''

@pytest.fixture
def advanced_sim():
    '''
    Defining a list om Simulation objects

    Returns:
    list: a list of Simulation objects
    '''
    sim = []
    sim.append(Simulation('tests_files/simple.msh', 'results/tests/simple', [[0.0, 0.45], [0.0, 0.2]]))
    sim.append(Simulation('tests_files/simple_mesh.msh', 'results/tests/simple_mesh', [[0.2, 0.4], [0.2, 0.4]]))
    sim.append(Simulation('tests_files/simple_mesh_2.msh', 'results/tests/simple_mesh_2', [[0.0, 1], [0.5, 0.75]]))
    return sim

@pytest.mark.parametrize('boarders', [([[[0.0, 0.45], [0.0, 0.2]], [[0.2, 0.4], [0.2, 0.4]], [[0.0, 1], [0.5, 0.75]]])])
def test_store_border(advanced_sim, boarders):
    '''
    Testing if the simulation stores the boarders of the fishinggrounds correctly

    Parameteres:
    advanced_sim (list): A list containing different simululation objects
    resfoldname (list): A list containing the coorect boarders
    '''
    for sim, boarder in zip(advanced_sim, boarders):
        for coord_sim_boarder, coord_boarder in zip(sim._boarders, boarder):
            for lim_sim_boarder, lim_boarder in zip(coord_sim_boarder, coord_boarder):
                assert  lim_sim_boarder == pytest.approx(lim_boarder)

@pytest.mark.parametrize('resfoldname', [(['results/tests/simple', 'results/tests/simple_mesh', 'results/tests/simple_mesh_2'])])
def test_store_resfoldname(advanced_sim, resfoldname):
    '''
    Testing if the simulation stores the result folder correctly

    Parameteres:
    advanced_sim (list): A list containing different simululation objects
    resfoldname (list): A list containing the coorect foldernames
    '''
    for sim, foldname in zip(advanced_sim, resfoldname):
        assert sim._resfoldname ==  foldname

@pytest.mark.parametrize('file', [('restart_file.txt')])
def test_restorerun_WrongFile_length(advanced_sim, file):
    '''
    Testing that if the restorerun method of the Simulation class is giving a restartFile with
    the wrong amount cells than it throws a TypeError

    Parameteres:
    advanced_sim (list): A list containing different simululation objects
    file (string): The name and path of a restart file
    '''
    for sim in advanced_sim:
        with pytest.raises(TypeError) as exeinfo:
            sim.restorerun(file)
        assert str(exeinfo.value) == 'There is something wrong with the restartFile'

@pytest.mark.parametrize('files', [('restart_file_21.txt', 'restart_file_22.txt', 'restart_file_23.txt')])
def test_restorerun_WrongFile_type(advanced_sim, files):
    '''
    Testing that if the restorerun method of the Simulation class is giving a restartFile without numbers
    than it throws a TypeError

    Parameteres:
    advanced_sim (list): A list containing different simululation objects
    file (string): The name and path of a restart file
    '''
    for sim, file in zip(advanced_sim, files):
        with pytest.raises(TypeError) as exeinfo:
            sim.restorerun(file)
        assert str(exeinfo.value) == 'There is something wrong with the restartFile'