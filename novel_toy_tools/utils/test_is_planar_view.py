from novel_toy_tools.utils.orientation import *
import pytest
from itertools import permutations, product
import numpy as np

from novel_toy_tools.src import render_opengl
from novel_toy_tools.src import get_experiment_data
from novel_toy_tools.src import generate_SO3_scipi

#ok so we're gonna want to generate a test example where we read from 3dViewer data, compute their planarity and then visually check


#test with multiple different view angles
#test with multiple axes defined of each type
#test with known planar rotations
#test with random planar rotations

class TestPlanarity:
    zero_vector = np.array([0,0,0])
    i_vector = np.array([1,0,0])
    j_vector = np.array([0,1,0])
    k_vector = np.array([0,0,1])
    identity_rotation = Rotation.from_euler("xyz", (0,0,0), True)
    pos_right_rotation_x = Rotation.from_euler("xyz", (90,0,0), True)
    neg_right_rotation_x = Rotation.from_euler("xyz", (-90, 0, 0), True)
    pos_right_rotation_y = Rotation.from_euler("xyz", (0, 90,0), True)
    neg_right_rotation_y = Rotation.from_euler("xyz", (0, -90, 0), True)
    pos_right_rotation_z = Rotation.from_euler("xyz", (0, 0, 90), True)
    neg_right_rotation_z = Rotation.from_euler("xyz", (0, 0, -90), True)
    pos_quarter_rotation_x = Rotation.from_euler("xyz", (25, 0, 0), True)
    neg_quarter_rotation_x = Rotation.from_euler("xyz", (-25, 0, 0), True)

    def test_no_rotation(self):
        assert is_planar_view(self.identity_rotation, [self.i_vector, self.j_vector], 2, True, VIEWER_3D_PERSPECTIVE_VECTOR ) == True

    def test_right_rotations(self):
        angles = generate_right_rotations()
        #TODO add composite rotations and check if they modulo 90, assert true if so, assert false if not so
        try:
            for eulers in angles:
                for axes in generate_main_axes():
                    assert is_planar_view(Rotation.from_euler("xyz", eulers, degrees=True), axes, 2, True) == True
        except ValueError:
            assert not np.any(axes)
                
    def test_three_quarters(self):
        #TODO programmatically iterate these tests
        assert is_planar_view(self.neg_quarter_rotation_x, [self.i_vector, self.j_vector], 2, True) == False
        assert is_planar_view(self.pos_quarter_rotation_x, [self.i_vector, self.j_vector], 2, True) == False

    #TODO this is not working correctly
    def test_colinear_planarity(self):
        colinear_axes = []
        colinear_axes.append(list(product(self.i_vector, repeat=3)))
        colinear_axes.append(list(product(self.j_vector, repeat=3)))
        colinear_axes.append(list(product(self.k_vector, repeat=3)))
        colinear_axes.append(list(product(self.i_vector, repeat=2)))
        colinear_axes.append(list(product(self.j_vector, repeat=2)))
        colinear_axes.append(list(product(self.k_vector, repeat=2)))
        for axes in colinear_axes:
            assert has_colinear_planarity(axes) == True

    #TODO this
    def test_threshold(self):
        pass



def generate_right_rotations():
    rights = [0, 90, -90, 180, -180, 270, -270]
    return list(product(rights, repeat=3))

def generate_quarter_rotations():
    quarters = []

def generate_main_axes():
    vectors = (TestPlanarity.i_vector, TestPlanarity.j_vector, TestPlanarity.k_vector, TestPlanarity.zero_vector)
    return product(vectors, repeat=3)

testObj = TestPlanarity()
testObj.test_colinear_planarity()