from abc import ABC, abstractmethod
from novel_toy_tools.core.abstract_frame_event import AbstractFrameEvent
from typing import List

class AbstractDataWriter(ABC):
    #TODO decide how to infer props
    def __init__(self):
        super().__init__()

    @abstractmethod
    def write(self, frame_events:List[AbstractFrameEvent]):
        pass

    @abstractmethod
    def update(self, frame_events:List[AbstractFrameEvent]):
        pass