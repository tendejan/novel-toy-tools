from abc import ABC, abstractmethod
import os
import numpy as np

OBJECTS_DIRECTORY = "/Users/tendejan/Desktop/Tom Endejan Novel Toy 2024/data/objects"

class NovelToy(ABC):
    def __init__(self, object_name, objects_directory:os.PathLike=OBJECTS_DIRECTORY):
        self.path_to_object = self.find_object(object_name, objects_directory)
        self.toy_data = self.load_object(self.path_to_object)
        super().__init__()

    @staticmethod
    def load_object(path_to_object:os.PathLike):
        vertices = []
        normals = []
        faces = []
        major_axis_definitions = {}

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
                elif line.startswith('# axis '):
                    parts = line.split()
        
        return np.array(vertices), np.array(normals), np.array(faces)
    
    @staticmethod
    def find_object(object_name:str, objects_directory:os.PathLike) -> os.PathLike:
        for root, dirs, files in os.walk(objects_directory):
            if object_name + ".obj" in files:
                return os.path.join(root, object_name + ".obj")

    def get_toy_data(self):
        return self.toy_data