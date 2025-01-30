from abc import ABC, abstractmethod
from os import PathLike

class Pipeline(ABC):
    def __init__(self, data_provider):
        super().__init__()

    def set_output_path(self, path:PathLike):
        self.output_path = path
        return
    
    def set_input_path(self, path:PathLike):
        self.input_path = path
        return

    @abstractmethod
    def run(self):
        raise NotImplementedError