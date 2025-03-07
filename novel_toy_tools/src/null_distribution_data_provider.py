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
        self.toys = list(toy_frame_counts.keys())
        self.frames:list = None

    def __iter__(self):
        self.frames = []
        for toy in self.toy_frame_counts:
            for _ in range(self.toy_frame_counts[toy]): #TODO I know this is wasteful but its also simple
                self.frames.append(toy)
        self.i = 0
        self.height = len(self.frames)
        return self
    
    def __next__(self):
        if self.i >= self.height:
            raise StopIteration
        else:
        
            eulers = Rotation.random().as_euler(VIEWER3D_EULER_ORDER, degrees=True)

            novel_toy_name = self.frames[self.i]
            frame_number = self.i
            experiment_id = "NULL"
            age = "NULL"
            camera_type = "virtual"
            code = 1
            euler_x = eulers[0]
            euler_y = eulers[1]
            euler_z = eulers[2]
            onset = -1
            offset =-1
            row = {
                "3d object": novel_toy_name,
                " subject id": 00000,
                " frame number": frame_number,
                " exp ID": experiment_id,
                " age": age,
                " camera type": camera_type,
                " code": 1,
                " x": euler_x,
                " y": euler_y,
                " z": euler_z,
                " onset":-1,
                " offset":-1,
                " raw filename": f"{novel_toy_name}_x{round(euler_x, 2)}_y{round(euler_y, 2)}_z{round(euler_z, 2)}"
                
            }
            
            self.i += 1
            return row

    def get_toys(self):
        return self.toy_frame_counts.keys()
    
    def height(self):
        return sum(self.toy_frame_counts.values())