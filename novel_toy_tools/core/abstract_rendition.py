from abc import ABC, abstractmethod
from dataclasses import dataclass

#TODO dept: think about removing this dept
from PIL import Image

#TODO rethink if we need this class
@dataclass
class AbstractRendition(ABC):
    image:Image = None

    #TODO probs only need this for debug
    def show(self):
        self.image.show()

    @abstractmethod
    def save(self):
        pass