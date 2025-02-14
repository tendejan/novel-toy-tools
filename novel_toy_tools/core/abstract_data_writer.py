from abc import ABC, abstractmethod
from novel_toy_tools.core.abstract_frame_event import AbstractFrameEvent

class AbstractDataWriter(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def save_frame_event(self, frame_event:AbstractFrameEvent):
        pass