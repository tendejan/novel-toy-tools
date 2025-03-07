from novel_toy_tools.core.abstract_data_writer import AbstractDataWriter
from novel_toy_tools.core.abstract_frame_event import AbstractFrameEvent
from os import PathLike
import os
import polars as pl
from typing import List

class ExperimentalDataWriter(AbstractDataWriter):
    def __init__(self, renditions_path:PathLike, statistics_path:PathLike):
        super().__init__()
        self.renditions_path = renditions_path
        self.statistics_path = statistics_path
        self.i = 0

    def write(self, frame_events:List[AbstractFrameEvent]):
        super().write(frame_events)
        out_data = []
        for frame_event in frame_events:
            rend_name = self.generate_rendition_name(frame_event) + str(self.i) #TODO write a check here to see if file already exists, then warn instead of appending self.i
            rendition_path = os.path.join(self.renditions_path, rend_name)
            frame_event.rendition.save(rendition_path + ".png")
            frame_event.inject_computed_statistics({'rendition name': rend_name})
            out_data.append(frame_event.statistics)
            self.i += 1
        dataframe = pl.from_dicts(out_data)
        dataframe.write_csv(self.statistics_path)

    def update(self, frame_event):
        return super().update(frame_event)
    
    @staticmethod
    def generate_rendition_name(frame_event:AbstractFrameEvent):
        rendition_name = ""
        if frame_event.statistics[' raw filename']:
            rendition_name = "rendition_" + frame_event.statistics[' raw filename']
        return rendition_name