from abc import ABC, abstractmethod
#TODO Abstract NovelToy should be in this class


class FrameDataProvider(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __next__(self):
        pass

    @abstractmethod
    def get_rendition_name(self):
        pass