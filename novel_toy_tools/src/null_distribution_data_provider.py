from novel_toy_tools.core.abstract_data_provider import AbstractDataProvider
#TODO this dept may be changed to an abstract class
from novel_toy_tools.core.abstract_renderer import AbstractRenderer
from novel_toy_tools.constants import VIEWER3D_EULER_ORDER
from scipy.spatial.transform import Rotation
from novel_toy_tools.src.frame_event_viewer3d import FrameEventViewer3d

class NullDistributionDataProvider(AbstractDataProvider):
    """A DataManager class for generating FrameEvents randomly"""
    def __init__(self, toy_frame_counts:dict):
        self.toy_frame_counts = toy_frame_counts
        self.toys = toy_frame_counts.keys()
        self.current_toy_index = 0
        self.repitition = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current_toy_index >= len(self.toys):
            raise StopIteration
        
        #TODO this is so messy, clean it up seriously
        if self.repitition < self.toy_frame_counts[self.toys[self.current_toy_index]]:
            #TODO change this perhaps
            eulers = Rotation.random().as_euler(VIEWER3D_EULER_ORDER, degrees=True)
            frame_event = FrameEventViewer3d()

            frame_event.novel_toy_name = self.toys[self.current_toy_index]
            frame_event.frame_number = self.repitition
            frame_event.experiment_id = "NULL"
            frame_event.age = "NULL"
            frame_event.camera_type = "virtual"
            frame_event.code = 1
            frame_event.euler_x = eulers[0]
            frame_event.euler_y = eulers[1]
            frame_event.euler_z = eulers[2]
            frame_event.onset = -1
            frame_event.offset =-1
            
            self.repitition += 1
            return frame_event
        else:
            self.repitition = 0
            self.current_toy_index += 1
            return 
