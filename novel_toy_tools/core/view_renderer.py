from abc import ABC, abstractmethod
import pandas as pd

class ViewRenderer(ABC):
    @abstractmethod
    def render_all_views(self, object_path:str, euler_angles:list, output_path:str) -> pd.DataFrame:
        """render and save views of object to output"""
        pass

    