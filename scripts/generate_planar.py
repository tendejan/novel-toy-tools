import polars as pl
from novel_toy_tools.src.wavefront_novel_toy import WavefrontNovelToy
from novel_toy_tools.src.opengl_renderer import OpenGlRenderer
from novel_toy_tools.src.frame_event_viewer3d import FrameEventViewer3d
from novel_toy_tools.utils import is_planar_view, arrange_eulers
from novel_toy_tools.src.experimental_data_provider import ExperimentalDataProviderFromConsolidated
from scipy.spatial.transform import Rotation

from novel_toy_tools.constants import VIEWER3D_EULER_ORDER
from novel_toy_tools import my_secrets
import os

OUT_DIR = os.path.normpath(r"/Users/tendejan/Desktop/Tom Endejan Novel Toy 2024/data/experimental")
OUT_FILE = os.path.normpath(r"null_planarity.csv")
OUT_PATH = os.path.join(OUT_DIR, OUT_FILE)
INFILE = os.path.normpath(r"/Users/tendejan/Desktop/Tom Endejan Novel Toy 2024/data/alfredo_planar_computed/null_views_planar_food.csv")

def main():
    data_provider = ExperimentalDataProviderFromConsolidated(INFILE)
    toys_cache = {}
    for toy in data_provider.get_toys():
        toys_cache[toy] = WavefrontNovelToy(toy, my_secrets.OBJECTS_DIRECTORY)
    
    schema = {"toy": pl.String, " raw filename": pl.String, "is planar": pl.Boolean, "x": pl.Float64, "y": pl.Float64, "z":pl.Float64}
    out = pl.DataFrame(schema=schema)
    for row in data_provider:
        frame_event = FrameEventViewer3d(row)

        eulers = arrange_eulers(VIEWER3D_EULER_ORDER, row[' x'], row[' y'], row[' z'])
        frame_event.rotation = Rotation.from_euler(VIEWER3D_EULER_ORDER, eulers, degrees=True)

        frame_event.novel_toy = toys_cache[row['3d object']]


        is_planar = is_planar_view(frame_event.rotation, frame_event.novel_toy.get_major_axes(), 10, degrees=True)
        data = pl.DataFrame({"toy":frame_event.novel_toy.name, " raw filename": frame_event.statistics[' raw filename'], "is planar": is_planar, "x": row[' x'], "y":row[' y'], "z":row[' z']})
        out = out.vstack(data)
    
    out.write_csv("null_planarity.csv")

main()