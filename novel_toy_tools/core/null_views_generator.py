from abc import ABC, abstractmethod

class NullViewsGenerator(ABC):
    @abstractmethod
    def get_angles(self):
        """Returns a set of all possible views of an object"""
        pass