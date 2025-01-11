from novel_toy_tools.core.novel_toy import NovelToy
from novel_toy_tools.implementations.render_opengl import OpenGLViewRenderer
from scipy.spatial.transform import Rotation
import numpy as np
import os
import itertools

"""for determining euler order of the 3d viewer app"""



def squish(list):
    string = ""
    for elem in list:
        string+=elem
    return string


def arrange_euler(triplet):
    eulers = []
    for elem in triplet:
        eulers.append(angle_dict[elem])
    return eulers

def create_perms(renderer, order_from, pos):
    image_perm = f"img{pos}_from_{squish(order_from)}"
    image_path = os.path.join(OUT_FOLDER, image_perm)
    rotation = Rotation.from_euler(order_from, arrange_euler(order_from), degrees=True)
    renderer.render_single_view(hole_block, rotation, image_path) 

def test_axis(renderer):
    rotations = [(0,0,0), (90, 0, 0), (0, 90, 0), (0, 0, 90)]
    axis = ['none',"x", 'y', 'z']

    for rotate, ax in zip(rotations, axis):
        image_perm = f"axis_check_{ax}_"
        image_path = os.path.join(OUT_FOLDER, image_perm)
        abstract_rot = Rotation.from_euler("xyz", rotate, degrees=True)
        renderer.render_single_view(hole_block, abstract_rot, image_path)

def main():
    hole_block = NovelToy("HoleBlock2QuaterBlocks")
    renderer = OpenGLViewRenderer(600, 800)
    all_uppers = list(map(squish, itertools.permutations(["X", "Y", "Z"])))
    angle_dict = {
        "X" : 90,
        "Y" : 80,
        "Z" : 70
    }


os.makedirs(OUT_FOLDER, exist_ok=True)
pos = 0
for order_from in all_uppers:
    create_perms(order_from, pos)
    pos += 1

test_axis()

if __name__ == "__main__":
    #TODO implement cli
    pass