from abc import ABC, abstractmethod
from novel_toy_tools.core.abstract_frame_event import AbstractFrameEvent
from novel_toy_tools.core.abstract_renderer import AbstractRenderer


class AbstractDataProvider():
    def __init__(self, source, renderer:AbstractRenderer):
        super().__init__()
        self.source = source
        pass
        
    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __next__(self) -> AbstractFrameEvent:
        pass