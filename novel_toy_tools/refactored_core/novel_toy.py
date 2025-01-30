from abc import ABC, abstractmethod
from os import PathLike

#TODO major axis reading from obj file should be in inherited class

class NovelToy(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def load_mesh(self, path:PathLike):
        raise NotImplementedError

    @abstractmethod
    def get_mesh(self):
        raise NotImplementedError

    @abstractmethod
    def get_main_axis(self):
        raise NotImplementedError