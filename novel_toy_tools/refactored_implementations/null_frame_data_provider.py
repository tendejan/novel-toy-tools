from novel_toy_tools.refactored_core.frame_data_provider import FrameDataProvider
from novel_toy_tools.refactored_core.renderer import Renderer
from scipy.spatial.transform import Rotation

#TODO this class may want to also generate the rendion statistics
#TODO add documentation about this
#TODO derivitive NovelToy should be in this class
EULER_ORDER = "XYZ"

class NullFrameDataProvider(FrameDataProvider):
    def __init__(self, renderer:Renderer):
        #TODO add inital values and bounds for iterator
        self.renderer = Renderer
        super().__init__()

    def __iter__(self):
        return super().__iter__()
    
    def __next__(self):
        #TODO write out of bounds to raise StopIteration
        rotation = Rotation.random()
        self.euler_x, self.euler_y, self.euler_z = rotation.as_euler(EULER_ORDER, degrees=True)
        #TODO may want to seperate the computation parts from this class to be parallelizable
        #TODO generate the rendition, do work on the rendition, add work to self.data
        #TODO this function should return a pandas row of all the data in question
        return super().__next__()
    
    def get_rendition_name(self):
        return super().get_rendition_name()