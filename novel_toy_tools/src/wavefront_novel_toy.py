from novel_toy_tools.core.abstract_novel_toy import AbstractNovelToy
import os
import numpy as np

#TODO remove the secret, constant
from novel_toy_tools.constants import NOVEL_TOY_EXTENSION

class WavefrontNovelToy(AbstractNovelToy):
    def __init__(self, toy_name:str, toy_directory:os.PathLike):
        super().__init__()
        self.toy_file_path = self.find_toy_file(toy_name, toy_directory)
        self.name = toy_name
        #TODO write error for missing major axes here
        self.load_object(self.toy_file_path)

    @staticmethod
    def find_toy_file(toy_name:str, search_directory:os.PathLike):
        for root, dirs, files in os.walk(search_directory):
            #TODO may create a new file format so change the file extension here and perhaps throw an error
            if toy_name + NOVEL_TOY_EXTENSION in files:
                return os.path.join(root, toy_name + NOVEL_TOY_EXTENSION)


    def load_object(self, path_to_object:os.PathLike):
        vertices = []
        normals = []
        faces = []
        with open(path_to_object) as f:
            for line in f:
                if line.startswith('v '):
                    parts = line.split()
                    vertex = list(map(float, parts[1:4]))
                    vertices.append(vertex)
                elif line.startswith('vn '):
                    parts = line.split()
                    normal = list(map(float, parts[1:4]))
                    normals.append(normal)
                #TODO sometimes im gonna need to triangulate quad faces :=(
                elif line.startswith('f '):
                    parts = line.split()
                    face = []
                    for p in parts[1:]:
                        vals = p.split('/')
                        vertex_idx = int(vals[0]) - 1
                        normal_idx = int(vals[2]) - 1
                        face.append((vertex_idx, normal_idx))
                    if len(face) == 4: #great we have a quad now
                        faces.append([face[0], face[1], face[2]])
                        faces.append([face[0], face[2], face[3]])
                    elif len(face) == 3:
                        faces.append(face)
                    else: raise ValueError(f"Unsupported face with dim {len(face)}")
                #TODO write parser for major axis'
                elif line.startswith('axis '):
                    parts = line.split()
                    if parts[1] == "elongation_main":
                        axis_of_elongation_main = np.array(list(map(int, parts[2:])))
                    elif parts[1] == "elongation_secondary":
                        axis_of_elongation_secondary = np.array(list(map(int, parts[2:])))
                    elif parts[1] == "top":
                        axis_of_top = np.array(list(map(int, parts[2:])))
                    elif parts[1] == "forward":
                        axis_of_forward = np.array(list(map(int, parts[2:])))
                        #TODO maybe raise axis not found error here?

        self.vertices = np.array(vertices) 
        self.normals = np.array(normals)
        self.faces = np.array(faces)