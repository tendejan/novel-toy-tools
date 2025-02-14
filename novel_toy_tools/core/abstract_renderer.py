from abc import ABC, abstractmethod
from novel_toy_tools.core.abstract_rendition import AbstractRendition
from novel_toy_tools.core.abstract_novel_toy import AbstractNovelToy
from novel_toy_tools.core.abstract_rotation import AbstractRotation

class AbstractRenderer(ABC):
    def __init__(self):
        super().__init__()

    #TODO this may need to be a static method
    @abstractmethod #TODO type the Rotation object better here, rn its just a scipy
    def generate_rendition(self, novel_toy:AbstractNovelToy, rotation:AbstractRotation) -> AbstractRendition:
        pass