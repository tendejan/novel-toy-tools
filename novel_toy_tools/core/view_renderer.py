from abc import ABC, abstractmethod
import pandas as pd
from novel_toy_tools.core.data_provider import DataProvider
from os import PathLike
from novel_toy_tools.core.novel_toy import NovelToy

class ViewRenderer(ABC):
    def __init__(self): #TODO shader as arg
        super().__init__()

    def render_all_views(self, data_provider:DataProvider, output_path:str):
        """render and save views from a DataProvider object to output"""
        for novel_toy, rotation in data_provider:
            rendition_path = self.render_single_view(novel_toy, rotation, data_provider.get_rendition_name())
            data_provider.link_rendition(rendition_path)

    @abstractmethod
    def render_single_view(object:NovelToy, rotation, output_path:str) -> PathLike:
        """render and save a single view of the object to output"""
        pass
    