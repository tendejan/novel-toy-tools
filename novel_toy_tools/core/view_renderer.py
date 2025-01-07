from abc import ABC, abstractmethod
import pandas as pd

class ViewRenderer(ABC):
    @abstractmethod
    def render_all_views(self, object_path:str, euler_angles:list, output_path:str) -> pd.DataFrame:
        """render and save views of object to output"""
        pass
    def render_single_view(self, object_path:str, angel, output_path:str):
        """render and save a single view of the object to output"""
        pass

    