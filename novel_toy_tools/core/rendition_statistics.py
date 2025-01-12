from abc import ABC, abstractmethod
from os import PathLike

class RenditionStatistics(ABC):
    """an abstract class for the various computations on novel toy renditions"""
    def __init__(self, path_to_image:PathLike):
        self.load_image(path_to_image)
        return super().__init__()
    
    @abstractmethod
    def load_image(self, path_to_image:PathLike):
        raise NotImplementedError

    @abstractmethod
    def compute_area_presented(self):
        raise NotImplementedError

    @abstractmethod
    def compute_longest_edge(self):
        raise NotImplementedError

    @abstractmethod
    def compute_planar_view(self):
        raise NotImplementedError

    @abstractmethod
    def get_rendition_statistics(self) -> dict:
        raise NotImplementedError