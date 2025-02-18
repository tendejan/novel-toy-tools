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

