from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class AbstractNovelToy(ABC):
    def __init__(self):
        self.name = None
        self.vertices = None
        self.normals = None
        self.faces = None
        self.axis_of_elongation_main = None
        self.axis_of_elongation_secondary = None
        self.axis_of_top = None
        self.axis_of_forward = None
        super().__init__()

    def get_major_axes(self):
        axes = [self.axis_of_elongation_main, self.axis_of_elongation_secondary, self.axis_of_forward, self.axis_of_top]
        returnable = []
        for axis in axes:
            if len(axis) != 0:
                returnable.append(axis)
        return returnable