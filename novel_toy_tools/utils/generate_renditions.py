from argparse import ArgumentParser
from novel_toy_tools.src.wavefront_novel_toy import WavefrontNovelToy
from novel_toy_tools.src.opengl_renderer import ObjectRenderer
from novel_toy_tools.utils import arrange_eulers
from scipy.spatial.transform import Rotation
import polars as pl
from multiprocessing import Pool
import os
from tqdm import tqdm
from functools import partial

NUM_CORES = os.cpu_count() - 1

OBJECT_DIRECTORY = os.path.normpath(r"/Users/tendejan/Desktop/Alfredo Higher Order Image Properties/null_datasets_2025-09-05/PrefViews 3D objects")
INPUT_CSV = os.path.normpath(r"/Users/tendejan/Desktop/Alfredo Higher Order Image Properties/null_datasets_2025-09-05/test/rotation_data.csv")
OUTPUT_DIRECTORY = os.path.normpath(r"/Users/tendejan/Desktop/Alfredo Higher Order Image Properties/null_datasets_2025-09-05/test/renditions")

#change this order to whatever order your program uses
EULER_ORDER = "YZX"

#CSV header definitions, change these if needbe
PRIMARY_KEY = "KID_IDFrameKey"
EULER_X = "Euler_X"
EULER_Y = "Euler_Y"
EULER_Z = "Euler_Z"
OBJECT_NAME = 'Object'

#we probably only want the one renderer, pass in dimensions to the renderer object if you want something other than 800x600
# RENDERER will be created lazily when needed to avoid OpenGL initialization issues on import
RENDERER = None

def generate_rendition(object_cache:dict, output_dir:os.PathLike, dataframe_row:pl.Series, renderer:ObjectRenderer=None):
    # Create renderer if not provided
    if renderer is None:
        global RENDERER
        if RENDERER is None:
            RENDERER = ObjectRenderer(camera_distance=-35)
        renderer = RENDERER
    
    primary_key = dataframe_row[PRIMARY_KEY]

    #arrange the eulers and generate the rotation object for consumption
    x, y, z = dataframe_row[EULER_X], dataframe_row[EULER_Y], dataframe_row[EULER_Z]
    eulers = arrange_eulers(EULER_ORDER, x, y, z)
    rotation = Rotation.from_euler(EULER_ORDER, eulers, degrees=True)

    #get the toy object
    object_name = dataframe_row[OBJECT_NAME]
    toy = object_cache[object_name]

    #generate rendition and save out
    rendition = renderer.generate_rendition(toy, rotation)
    output_path = os.path.join(output_dir, f"rendition_{primary_key}.jpg")
    rendition.save(output_path)
    return primary_key

def generate_renditions(input_csv:os.PathLike=None, output_directory:os.PathLike=None, object_directory:os.PathLike=None):
    # Use default values if not provided
    if input_csv is None:
        input_csv = INPUT_CSV
    if output_directory is None:
        output_directory = OUTPUT_DIRECTORY
    if object_directory is None:
        object_directory = OBJECT_DIRECTORY
    
    #read the csv
    dataframe = pl.read_csv(input_csv, ignore_errors=True)
    #filter out all rows that do not contain orientations
    dataframe = dataframe.filter(
        pl.col(EULER_X).is_not_null(),
        pl.col(EULER_Y).is_not_null(),
        pl.col(EULER_Z).is_not_null(),
    )
    #find and cache all unique objects in these data
    wavefront_objects = dataframe.select(pl.col(OBJECT_NAME)).unique().to_series().to_list()
    toy_cache = {}
    for toy in wavefront_objects:
        toy_cache[toy] = WavefrontNovelToy(toy, object_directory)

    #create the out directory
    os.makedirs(output_directory, exist_ok=True)

    partial_funct = partial(generate_rendition, toy_cache, output_directory)
    #generate the rotations in parallel
    print(f"Saving renditions to {output_directory}")
    with Pool(NUM_CORES) as pool:
        results = list(tqdm(
            pool.imap_unordered(partial_funct, dataframe.iter_rows(named=True)),
            total=dataframe.height,
            desc="Generating Renditions"
        ))

def cli_main():
    """Console script entry point"""
    parser = ArgumentParser(prog="generate-renditions",
                            description="reads an input csv containing euler angles and object names and generates"
                            "renditions of those objects by their rotations")
    parser.add_argument(
        "-i", "--input_csv", help="path to the csv containing the rotations and objects"
    )
    parser.add_argument(
        "-o", "--output_directory", help="directory to store all renditions"
    )
    parser.add_argument(
        "-obj", "--object_directory", help="the directory storing all the wavefront .obj files for reading into the program"
    )

    args = parser.parse_args()
    generate_renditions(
        input_csv=args.input_csv,
        output_directory=args.output_directory,
        object_directory=args.object_directory
    )

if __name__ == "__main__":
    cli_main()