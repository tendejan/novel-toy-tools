import os
from novel_toy_tools._depricated.implementations.render_opengl import OpenGLViewRenderer
from novel_toy_tools._depricated.implementations.generate_SO3_scipi import RandomSampleDataProvider
from novel_toy_tools._depricated.interfaces.novel_toy import NovelToy
import pandas as pd
from scipy.spatial.transform import Rotation

OUTPUT_DIR = r"/Users/tendejan/Desktop/Tom Endejan Novel Toy 2024/data/null_distributions"
OBJECT_DIR = r"/Users/tendejan/Desktop/Tom Endejan Novel Toy 2024/data/objects"
NUM_SAMPLES = 500
VIEWER_3D_EULER_ORDER = "YZX"

OBJECTS = []
for file in os.listdir(OBJECT_DIR):
    if file.endswith(".obj"):
        OBJECTS.append(file[:-4])

renderer = OpenGLViewRenderer(600, 800)
#NOTE the colums x y and z have a space before each letter to keep consistent with previous csv's
columns = ['object', ' x', ' y', ' z', 'rendition']
dataframe = pd.DataFrame()
data = []
for object in OBJECTS:
    outdir = os.path.join(OUTPUT_DIR, object)
    os.makedirs(outdir, exist_ok=True)

    this_toy = NovelToy(object, OBJECT_DIR)
    all_rotations = Rotation.random(NUM_SAMPLES)
    for rotation in all_rotations:
        xyz = rotation.as_euler("XYZ", degrees=True)
        x, y, z = xyz[0], xyz[1], xyz[2]
        #TODO add an index here so there is no file save overlap, shouldnt matter too much
        file_name = f"null_rendition_{object}_at_x{int(x)}_y{int(y)}_z{int(z)}"
        outpath = os.path.join(outdir, file_name)
        file_path = renderer.render_single_view(this_toy, rotation, outpath)
        data.append([object, x, y, z, file_path])
path_to_master = os.path.join(OUTPUT_DIR, "null_master_data_sheet.csv")
master_data_sheet = pd.DataFrame.from_records(data, columns=columns)
master_data_sheet.to_csv(path_to_master)
