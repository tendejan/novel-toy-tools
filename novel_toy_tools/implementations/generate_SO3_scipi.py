from novel_toy_tools.core.data_provider import DataProvider
from scipy.spatial.transform import Rotation

#TODO conform to interface

class RandomSampleDataProvider(DataProvider):
    def __init__(self):
        self.dataframe = self.load_data()

    def __iter__(self):
        return super().__iter__()
    
    def __next__(self):
        return super().__next__()
    
    def link_rendition(self, rendition_path):
        return super().link_rendition(rendition_path)
    
    def get_rendition_name(self):
        return super().get_rendition_name()
    
    def load_data(self):
        return
    
    def generate_so3_samples(self, n):
        rotations = Rotation.random(n)
        return rotations
    