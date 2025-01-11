from novel_toy_tools.core.data_provider import DataProvider
from os import PathLike
import pandas as pd
import numpy as np
from novel_toy_tools.core.novel_toy import NovelToy
from scipy.spatial.transform import Rotation


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
            euler = (self.current_value[' y'], self.current_value[' z'], -1 * self.current_value[' x'])
            rotation = Rotation.from_euler("yzx", euler, degrees=True)
            return novel_toy, rotation #TODO this function needs help
        else: pass
    
    def load_data(self, in_file:PathLike):
        return pd.read_csv(in_file)
    
    def link_rendition(self, rendition_path):
        self.dataframe.loc[self.current_index, 'rendition'] = rendition_path
        return
    
    def get_rendition_name(self):
        frame_name = self.current_value[' raw filename']
        rendition_name = "rendition_" + frame_name
        return rendition_name
    
    def get_current_object(self):
        object_name = self.current_value['3d object']
        return object_name
    
    def is_coded(self) -> bool: #TODO check coded value and also check nan in angles
        if self.current_value[' code'] == 1:
            return True
        else: return False
    
if __name__ == "__main__":
    infile = r"/Users/tendejan/Desktop/Tom Endejan Novel Toy 2024/data/experimental/OldDataSheet.csv"
    data_provider = ExperimentalDataFromConsolidated(infile, "/tests")
    for data in data_provider:
        print(data)
