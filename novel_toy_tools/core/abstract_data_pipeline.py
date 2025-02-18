from abc import abstractmethod, ABC
from novel_toy_tools.core.abstract_data_manager import AbstractDataManager
from typing import List


class AbstractDataPipeline(ABC):
    def __init__(self, data_managers:List[AbstractDataManager]):
        super().__init__()


    @abstractmethod
    def process_frames(self):
        pass