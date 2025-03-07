from novel_toy_tools.core.abstract_frame_analysis import AbstractFrameAnalysis
from novel_toy_tools.core.abstract_frame_event import AbstractFrameEvent
from novel_toy_tools.src.image_analysis import ImageProcessor

import numpy as np
import cv2

class FrameAnalysis(AbstractFrameAnalysis):
    #TODO abstract this constructor with objects for image processor and oreintation processor
    def __init__(self,frame_event:AbstractFrameEvent, image_processor:ImageProcessor, orientation_procesor):
        super().__init__()
        self.image_processor = image_processor(frame_event) #TODO idk if this is the right dept inject
        self.orientation_processor = orientation_procesor #TODO abstract this into an object
    
    def analyse_statistics(self, frame_event:AbstractFrameEvent):
        super().analyse_statistics()
        self.image_processor.compute_area_presented()
        self.image_processor.compute_longest_line()
        #TODO abstract this part
        frame = self.frame_event

        self.computed_properties.update(self.image_processor.get_image_statistics())

    
    def get_computed_props(self):
        super().get_computed_props()
        return self.computed_properties