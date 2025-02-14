from abc import ABC, abstractmethod

class AbstractNovelToy(ABC):
    def __init__(self):
        self._name = None
        self._vertices = None
        self._normals = None
        self._faces = None
        self._axis_of_elongation_main = None
        self._axis_of_elongation_secondary = None
        self._axis_of_top = None
        self._axis_of_forward = None
        super().__init__()

    # Name property
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    # Vertices property
    @property
    def vertices(self):
        return self._vertices

    @vertices.setter
    def vertices(self, value):
        self._vertices = value

    # Normals property
    @property
    def normals(self):
        return self._normals

    @normals.setter
    def normals(self, value):
        self._normals = value

    # Faces property
    @property
    def faces(self):
        return self._faces

    @faces.setter
    def faces(self, value):
        self._faces = value

    # Axis of elongation (main) property
    @property
    def axis_of_elongation_main(self):
        return self._axis_of_elongation_main

    @axis_of_elongation_main.setter
    def axis_of_elongation_main(self, value):
        self._axis_of_elongation_main = value

    # Axis of elongation (secondary) property
    @property
    def axis_of_elongation_secondary(self):
        return self._axis_of_elongation_secondary

    @axis_of_elongation_secondary.setter
    def axis_of_elongation_secondary(self, value):
        self._axis_of_elongation_secondary = value

    # Axis of top property
    @property
    def axis_of_top(self):
        return self._axis_of_top

    @axis_of_top.setter
    def axis_of_top(self, value):
        self._axis_of_top = value

    # Axis of forward property
    @property
    def axis_of_forward(self):
        return self._axis_of_forward

    @axis_of_forward.setter
    def axis_of_forward(self, value):
        self._axis_of_forward = value

    # Major axes property (read-only, no setter)
    @property
    def major_axes(self):
        return {
            "elongation_main": self._axis_of_elongation_main,
            "elongation_secondary": self._axis_of_elongation_secondary,
            "top": self._axis_of_top,
            "forward": self._axis_of_forward
        }