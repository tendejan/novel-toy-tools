from abc import ABC, abstractmethod

class AbstractRendition(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_rendition_statistics(self):
        pass