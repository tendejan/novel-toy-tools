from novel_toy_tools.core.novel_toy import NovelToy
from novel_toy_tools.implementations.render_opengl_quaternion import OpenGLViewRenderer
from scipy.spatial.transform import Rotation
import quaternion
import numpy as np
import os
import itertools

hole_block = NovelToy("HoleBlock2QuaterBlocks")
renderer = OpenGLViewRenderer(600, 800)
OUT_FOLDER = "/Users/tendejan/Desktop/Tom Endejan Novel Toy 2024/tests/reverse_engineer"


def squish(list):
    string = ""
    for elem in list:
        string+=elem
    return string

def create_signs(list, size):
    signs = ['p', 'n']
    if len(list[0]) == size:
        return list
    else:
        accum = []
        for elem in list:
            accum.append(elem + signs[0])
            accum.append(elem + signs[1])
        return create_signs(accum, size)
    
all_signs = create_signs(['p', 'n'], 3)

def zip_signs(directions, signs):
    accum = []
    for direction in directions:
        for sign_combo in signs:
            accum.append((direction, sign_combo))
    return accum

all_lowers = list(map(squish, itertools.permutations(["x", "y", "z"])))
all_uppers = list(map(squish, itertools.permutations(["X", "Y", "Z"])))
all_directions = list(itertools.permutations(all_uppers + all_lowers, 2))
all_combos = zip_signs(all_directions, all_signs)


angle_dict = {
    "x" : -106,
    "y" : 1.68,
    "z" : 21.179,
    "X" : -106,
    "Y" : 1.68,
    "Z" : 21.179
}

def arrange_euler(triplet):
    eulers = []
    for elem in triplet:
        eulers.append(angle_dict[elem])
    return eulers

def val_generator():
    pass

def create_perms(order_from, order_to, vals, pos):
    image_perm = f"img{pos}_from_{squish(order_from)}_to_{squish(order_to)}"
    image_path = os.path.join(OUT_FOLDER, image_perm)
    rotation = Rotation.from_euler(order_from, arrange_euler(order_from), degrees=True)
    quat = quaternion.from_euler_angles(rotation.as_euler(order_to, False))
    renderer.render_single_view(hole_block, quat, image_path)

def test_axis():
    rotations = [(0,0,0), (90, 0, 0), (0, 90, 0), (0, 0, 90)]
    axis = ['none',"x", 'y', 'z']

    for rotate, ax in zip(rotations, axis):
        image_perm = f"axis_check_{ax}_"
        image_path = os.path.join(OUT_FOLDER, image_perm)
        abstract_rot = Rotation.from_euler("xyz", rotate, degrees=True)
        quat = quaternion.from_euler_angles(abstract_rot.as_euler('xyz', False))
        renderer.render_single_view(hole_block, quat, image_path)

os.makedirs(OUT_FOLDER, exist_ok=True)
pos = 0
for order_from, order_to in all_directions:
    create_perms(order_from, order_to, None, pos)
    pos += 1

test_axis()

