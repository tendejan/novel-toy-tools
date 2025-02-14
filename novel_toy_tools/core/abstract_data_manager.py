from abc import ABC, abstractmethod
from os import PathLike
from novel_toy_tools.core.abstract_frame_event import AbstractFrameEvent
from novel_toy_tools.core.abstract_data_provider import AbstractDataProvider
from novel_toy_tools.core.abstract_data_writer import AbstractDataWriter
from novel_toy_tools.core.abstract_renderer import AbstractRenderer


class AbstractDataManager(ABC):#TODO decide if analysis package and renderer goes here
    def __init__(self, data_provider:AbstractDataProvider, data_writer:AbstractDataWriter, analysis_package, renderer:AbstractRenderer):
        super().__init__()
        self.data_provider = data_provider
        self.data_writer = data_writer
        self.analysis_package = None #TODO analysis may want to be dynamically adjusted for brevity
        self.renderer = renderer #TODO renderer may not belong here
        self.toy_objects_cache = None #rethink the name here

#TODO should have an objects dict so we dont have to load each Novel_toy each time


    @abstractmethod
    def process_data(self):
        pass