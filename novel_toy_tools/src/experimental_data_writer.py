from novel_toy_tools.core.abstract_data_writer import AbstractDataWriter
from os import PathLike

class ExperimentalDataWriter(AbstractDataWriter):
    def __init__(self, renditions_path:PathLike, statistics_path:PathLike):
        super().__init__()

    def write(self, frame_events):
        return super().write(frame_events)
    
    def update(self, frame_events):
        return super().update(frame_events)