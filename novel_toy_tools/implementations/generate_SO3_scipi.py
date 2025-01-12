from novel_toy_tools.core.data_provider import DataProvider
from scipy.spatial.transform import Rotation

#TODO conform to interface

class RandomSampleDataProvider(DataProvider):
    def __init__(self, num_samples, objects):
        return self

    def __iter__(self):
        self.current_index = 0
        self.next_index = 1
        return self
    
    def __next__(self):
        return super().__next__()
    
    def link_rendition(self, rendition_path):
        return super().link_rendition(rendition_path)
    
    def get_rendition_name(self):
        return super().get_rendition_name()
    
    def load_data(self, num_samples):
        return
    
    def get_dataframe_from_samples():
        pass

    def generate_so3_samples(self, n):
        rotations = Rotation.random(n)
        return rotations
    