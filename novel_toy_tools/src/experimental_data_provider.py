from novel_toy_tools.core.abstract_data_provider import AbstractDataProvider
from novel_toy_tools.src.frame_event_viewer3d import FrameEventViewer3d
from typing import List
import polars as pl
from os import PathLike

class ExperimentalDataProviderFromConsolidated(AbstractDataProvider):
    def __init__(self, source:PathLike):
        #TODO more fanc reading here
        self.data_frame = pl.read_csv(source, has_header=True).filter(pl.col(" code")==1)
        self.data_frame_iterator = self.data_frame.iter_rows(named=True)
        super().__init__(source)

    def __iter__(self):
        return self.data_frame_iterator
    
    def __next__(self):
        return self.data_frame_iterator.__next__()
        

    def get_toys(self) -> List[str]: #TODO consider passing column names as a schema
        return self.data_frame.unique(subset=['3d object']).get_column('3d object').to_numpy().tolist()
        
    def height(self):
        return self.data_frame.height