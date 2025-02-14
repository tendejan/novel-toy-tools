from abc import abstractmethod, ABC
from novel_toy_tools.core.abstract_data_manager import AbstractDataManager
from novel_toy_tools.core.abstract_renderer import AbstractRenderer


class AbstractAnalysisPipeline(ABC):
    def __init__(self):
        super().__init__()


    @abstractmethod
    def process_frames(self):
        pass