from novel_toy_tools.interfaces.abstract_data_manager import AbstractDataManager
from novel_toy_tools.interfaces.abstract_data_provider import AbstractDataProvider
from novel_toy_tools.interfaces.abstract_data_writer import AbstractDataWriter
from novel_toy_tools.interfaces.abstract_renderer import AbstractRenderer

from novel_toy_tools.src.null_distribution_data_provider import NullDistributionDataProvider
from novel_toy_tools.src.null_data_writer import NullDataWriter
from opengl_renderer import OpenGlRenderer
import multiprocessing

from my_secrets import *
from novel_toy_tools.constants import *

#TODO this may be an uneeded file
#debug
import os

"""Data Manager for creating a null distribution"""
#TODO this may be converted to entirely abstract dependancys

class NullDataManager(AbstractDataManager):
    def __init__(self, data_provider:AbstractDataProvider, data_writer:AbstractDataWriter, renderer:AbstractRenderer):
        super().__init__(data_provider, data_writer, renderer)

    def process_data(self):
        return super().process_data()

    

if __name__ == "__main__":
    toy_payload = {toy: 5 for toy in NOVEL_TOYS}
    OUT_CSV = "/data/refactored/null.csv"
    OUT_DIR = '/data/refactored'

    data_provider = NullDistributionDataProvider(toy_payload)
    data_writer = NullDataWriter(OUT_CSV, OUT_DIR)
    renderer = OpenGlRenderer(*VIEWER3D_RENDITION_DIMENTIONS)
    manager = NullDataManager(data_provider, data_writer, renderer)

    manager.process_data()
    

    