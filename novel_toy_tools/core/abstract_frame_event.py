from abc import ABC, abstractmethod

#TODO may not need the renderer dep
from novel_toy_tools.core.abstract_renderer import AbstractRenderer

#TODO add rendition rotation and other abstract properties here
class AbstractFrameEvent(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_statistics(self, renderer:AbstractRenderer):
        pass