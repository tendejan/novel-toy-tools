from novel_toy_tools.interfaces.abstract_data_writer import AbstractDataWriter
from novel_toy_tools.interfaces.abstract_frame_event import AbstractFrameEvent
import os
import PIL

from novel_toy_tools.constants import VIEWER3D_OUTPUT_COLUMNS

import pandas as pd

class NullDataWriter(AbstractDataWriter):
    def __init__(self, csv_path:os.PathLike, rendition_directory:os.PathLike ):
        self.csv_path = csv_path
        self.rendition_directory = rendition_directory

        df = pd.DataFrame(columns=VIEWER3D_OUTPUT_COLUMNS)
        super().__init__()

    def save_frame_event(self, frame_event:AbstractFrameEvent, rendition_format:str="png"):
        """Method for dynamically saving the intrinsic and computed frame data"""
        #TODO make this async threaded so we dont have to wait
        self.save_image_data(frame_event, rendition_format)
        self.save_non_image_data(frame_event)
        return super().save_frame_event(frame_event)
    
    def save_image_data(self, frame_event:AbstractFrameEvent, rendition_format:str="png"):
        #save the rendition first
        #check object directory exists
        object_dir = os.path.join(self.rendition_directory, frame_event.novel_toy_name)
        os.makedirs(object_dir, exist_ok=True)

        #generate a dynamic name and path for saving the image to
        frame_event.rendition_name = f"null_rendition_{frame_event.novel_toy_name}_at_x{self.euler_x}_y{self.euler_y}_z{self.euler_z}.{rendition_format}"
        frame_event.rendition_path = os.path.join(object_dir, self.rendition_name)
        frame_event.rendition.save(self.rendition_path)

    def save_non_image_data(self, frame_event:AbstractFrameEvent):
        pass