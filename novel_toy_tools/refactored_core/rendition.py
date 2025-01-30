from abc import ABC, abstractmethod
from os import PathLike

class Rendition(ABC):
    def __init__(self):
        self.image
        self.path:PathLike
        super().__init__()

    @abstractmethod
    def get_statistics(self):
        raise NotImplementedError