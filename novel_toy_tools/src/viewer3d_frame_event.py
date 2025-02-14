from novel_toy_tools.interfaces.abstract_frame_event import AbstractFrameEvent
from novel_toy_tools.interfaces.abstract_renderer import AbstractRenderer
from novel_toy_tools.interfaces.abstract_novel_toy import AbstractNovelToy
from novel_toy_tools.constants import VIEWER3D_EULER_ORDER
from scipy.spatial.transform import Rotation

from novel_toy_tools.src.wavefront_novel_toy import WavefrontNovelToy


class Viewer3dFrameEvent(AbstractFrameEvent):
    #TODO this should take as many args as possible and then default to None for any others,
    #then it can dynamically generate the NONES
    def __init__(self,
                 raw_filename,
                 experiment_date,
                 subject_id,
                 frame_number,
                 age,
                 code,
                 euler_x,
                 euler_y,
                 euler_z,
                 onset,
                 offset,
                 experiment_id,
                 novel_toy_name = None):
        #TODO not sure if I should take the Abstract or the implemented here
        self.novel_toy_ = AbstractNovelToy
        self.subject_id = subject_id
        self.frame_number = frame_number
        self.experiment_id = experiment_id
        self.age = age
        self.experiment_date = experiment_date
        self.code = code
        #TODO investigate defaults for get rotation here
        self.rotation = Rotation.from_euler(VIEWER3D_EULER_ORDER, (euler_y, euler_z, euler_x), degrees=True)
        self.onset = onset
        self.offset = offset
        self.raw_filename = raw_filename
        #TODO may check if rendition is an os.path object here and then load it based on that
        self.rendition = None
        pass

    def get_statistics(self, renderer:AbstractRenderer):

        
        self.area
        self.longest_edge_length
        self.longest_edge_point1
        self.longest_edge_point2
        pass

    #TODO might get rid of this function
    # def get_rotation(self, euler_order:str=VIEWER3D_EULER_ORDER, degrees:bool=True) -> Rotation:
    #     """gets a Rotation from the given euler angles"""
    #     #TODO euler order shoud be dynamically organized for creating the Rotation
    #     return Rotation.from_euler(euler_order, (self.euler_y, self.euler_z, self.euler_x), degrees=degrees)
    
    #TODO this should probably just be the __get__ for self.rendition
    def get_rendition(self, renderer:AbstractRenderer=None):
        if self.rendition:
            return self.rendition #TODO may not want to return anything here
        #TODO write error here if rendition dosent exist and no renderer is injected
        else: #TODO self.novel_toy may take a refrence to a novel_toy object for efficiency
            self.rendition = renderer.generate_rendition(self.novel_toy, self.get_rotation())
            return self.rendition
    
    #TODO maybe make this less cumbersome and just do it at init by generating a novel_toy object
    def link_novel_toy(self, novel_toy:AbstractNovelToy):
        self.novel_toy = novel_toy