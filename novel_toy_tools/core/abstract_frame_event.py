from abc import ABC, abstractmethod
from dataclasses import dataclass
from novel_toy_tools.core.abstract_rotation import AbstractRotation
from novel_toy_tools.core.abstract_novel_toy import AbstractNovelToy
from novel_toy_tools.core.abstract_rendition import AbstractRendition

#TODO add rendition rotation and other abstract properties here
@dataclass
class AbstractFrameEvent(ABC):
    statistics:dict = None
    novel_toy:AbstractNovelToy = None
    rotation:AbstractRotation = None
    rendition:AbstractRendition = None

    #TODO this may want to be an abstract method
    def inject_computed_statistics(self, stats_dict:dict):
        self.statistics.update(stats_dict)
