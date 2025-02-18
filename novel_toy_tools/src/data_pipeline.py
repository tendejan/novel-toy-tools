from novel_toy_tools.core.abstract_data_pipeline import AbstractDataPipeline
from novel_toy_tools.core.abstract_data_manager import AbstractDataManager
from novel_toy_tools.src.opengl_renderer import OpenGlRenderer
from novel_toy_tools.src.null_distribution_data_provider import NullDistributionDataProvider
from novel_toy_tools.src.experimental_data_provider 
from novel_toy_tools.constants import *
from typing import List

class ExperimentalNullDataPipeline(AbstractDataPipeline):
    def __init__(self, data_managers:List[AbstractDataManager]):
        super().__init__(data_managers)


    def process_frames(self):
        for data_manager in self.data_managers:
            for frame in data_manager:
                pass



if __name__ == "__main__":
    renderer = OpenGlRenderer(*VIEWER3D_RENDITION_DIMENTIONS)
