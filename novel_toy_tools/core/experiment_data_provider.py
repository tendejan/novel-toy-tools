from abc import ABC, abstractmethod
import pandas as pd

class ExperimentDataProvider(ABC):
    @abstractmethod
    def get_data(self, in_path):
        """get data from experiment"""
        pass