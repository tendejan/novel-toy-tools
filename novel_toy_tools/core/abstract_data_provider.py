from abc import ABC, abstractmethod
from novel_toy_tools.core.abstract_frame_event import AbstractFrameEvent
from novel_toy_tools.core.abstract_renderer import AbstractRenderer
from typing import List

class AbstractDataProvider():
    #TODO source may need to change here
    def __init__(self, source):
        super().__init__()
        self.source = source
        pass
        
    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __next__(self) -> AbstractFrameEvent:
        pass

    #TODO this has been useful for batch computing but investigate if this is really where we want it
    @abstractmethod
    def get_toys(self) -> List[str]:
        pass

    @abstractmethod
    def height(self):
        pass