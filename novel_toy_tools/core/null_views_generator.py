from abc import ABC, abstractmethod

class NullViewsGenerator(ABC):
    @abstractmethod
    def get_angles(self, n):
        """Returns a set of n possible views of an object"""
        pass