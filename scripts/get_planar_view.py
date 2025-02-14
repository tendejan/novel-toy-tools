import pandas as pd
import os
from novel_toy_tools.utils import is_planar_view
from novel_toy_tools.implementations.get_experiment_data import ExperimentalDataFromConsolidated
from novel_toy_tools.implementations.render_opengl import OpenGLViewRenderer

EXPERIMENTAL_DATA_SHEET_PATH = r"/Users/tendejan/Desktop/Tom Endejan Novel Toy 2024/data/experimental/generated/master_data_sheet.csv"
OUT_PATH = r"/Users/tendejan/Desktop/Tom Endejan Novel Toy 2024/data/planar_test"


experimental_dataframe = pd.read_csv(EXPERIMENTAL_DATA_SHEET_PATH)
experimental_dataframe.insert(1, 'is planar view', None)

def get_major_axes(object):
    pass


os.makedirs(OUT_PATH, exist_ok=True)
for row in experimental_dataframe:
    