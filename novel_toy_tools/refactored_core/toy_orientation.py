from abc import ABC, abstractmethod
from novel_toy_tools.core.novel_toy import NovelToy
from scipy.spatial.transform import Rotation ## TODO may want to move away from this dependancy but its great for now

class ToyOrientation(ABC):

    def __init__(self, novel_toy:NovelToy, orientation:Rotation):
        self.novel_toy = novel_toy
        self.orientation = orientation
        super().__init__()

    @abstractmethod
    def get_rendition(self):
        raise NotImplementedError

    @abstractmethod
    def get_novel_toy(self):
        raise NotImplementedError

    @abstractmethod
    def get_orientation(self):
        raise NotImplementedError
        
    @abstractmethod
    def set_rendition(self):
        raise NotImplementedError