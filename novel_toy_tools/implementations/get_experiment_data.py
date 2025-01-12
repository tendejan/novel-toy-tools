from novel_toy_tools.core.data_provider import DataProvider
from os import PathLike
import pandas as pd
import numpy as np
from novel_toy_tools.core.novel_toy import NovelToy
from scipy.spatial.transform import Rotation

#see https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.from_euler.html
VIEWER_3D_EULER_ORDER = "YZX" #where capital corisponds to intrinsic rotations

class ExperimentalDataFromConsolidated(DataProvider):
    def __init__(self, in_file, output_directory):
        self.dataframe = self.load_data(in_file)
        self.dataframe['rendition'] = None

    def __iter__(self):
        self.current_index = 0
        self.next_index = 1
        return self

    def __next__(self):
        if self.dataframe.size == 0 or self.next_index  > len(self.dataframe):
            self.current_value = None
            raise StopIteration
        self.current_value = self.dataframe.iloc[self.current_index]
        self.current_index = self.next_index
        self.next_index += 1

        if self.is_coded():
            novel_toy = NovelToy(self.current_value['3d object'])
            #NOTE dataframe columns x, y, and z have a space in front of them to keep consistent with previous work
            # the order that euler values are read in will need to change if VIEWER_3D_EULER_ORDER is changed
            euler = (self.current_value[' y'], self.current_value[' z'], self.current_value[' x'])
            rotation = Rotation.from_euler(VIEWER_3D_EULER_ORDER, euler, degrees=True)
            return novel_toy, rotation
        else: pass
    
    def load_data(self, in_file:PathLike):
        return pd.read_csv(in_file)
    
    def link_rendition(self, rendition_path):
        self.dataframe.loc[self.current_index, 'rendition'] = rendition_path
        return
    
    def get_rendition_name(self):
        #NOTE column raw filename has a space in front to keep consistent with previous work
        frame_name = self.current_value[' raw filename']
        rendition_name = "rendition_" + frame_name
        return rendition_name
    
    def get_current_object(self):
        object_name = self.current_value['3d object']
        return object_name
    
    def is_coded(self) -> bool: #TODO check coded value and also check nan in angles
        #NOTE column code has a space to keep consistent with previous work
        if self.current_value[' code'] == 1:
            return True
        else: return False
    
if __name__ == "__main__":
    pass
