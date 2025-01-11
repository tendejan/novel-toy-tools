from abc import ABC, abstractmethod
from pandas import DataFrame
from os import PathLike

class DataProvider(ABC):

    @abstractmethod
    def __init__(self):
        self.dataframe:DataFrame
        self.output_directory:PathLike
        pass

    @abstractmethod
    def __iter__(self):
        return self
    
    @abstractmethod
    def __next__(self):
        pass

    @abstractmethod
    def link_rendition(self, rendition_path:PathLike):
        """links the generated rendition with the current item in the iterator"""
        pass

    @abstractmethod
    def get_rendition_name(self) -> str:
        pass

    @abstractmethod #TODO at the moment this batch loads all the data, may want to implement an iterator for it
    def load_data(self):
        pass