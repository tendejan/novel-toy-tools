from novel_toy_tools.core.abstract_frame_analysis import AbstractFrameAnalysis
from novel_toy_tools.core.abstract_frame_event import AbstractFrameEvent

import numpy as np
import cv2

class FrameAnalysis(AbstractFrameAnalysis):
    def __init__(self, frame_event:AbstractFrameEvent, avoid_holes:bool=False):
        super().__init__(frame_event)
        self.rendition = frame_event.rendition #TODO may need more about implementation here, investigate an abstract rendition
        self.AVOID_HOLES = False
        self.image_binarized = None
        self.image_contours, self.contour_hierarchy = None, None

    def analyse_rendition(self):
        return super().analyse_rendition()
    
    def analyse_statistics(self):
        return super().analyse_statistics()
    
    def get_computed_props(self):
        return super().get_computed_props()