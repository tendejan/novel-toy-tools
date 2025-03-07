from abc import ABC, abstractmethod
from novel_toy_tools.core.abstract_frame_event import AbstractFrameEvent

class AbstractFrameAnalysis(ABC):
    def __init__(self, frame_event:AbstractFrameEvent):
        self.computed_properties:dict = None
        self.frame_event:AbstractFrameEvent = frame_event #TODO this class may be more static than not
        super().__init__()

    @abstractmethod
    def analyse_statistics(self):
        pass

    def get_computed_props(self):
        return self.computed_properties