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

OBJECT_DIRECTORY = os.path.normpath(r"")
INPUT_CSV = os.path.normpath(r"")
OUTPUT_DIRECTORY = os.path.normpath(r"")

#change this order to whatever order your program uses
EULER_ORDER = "YZX"

#CSV header definitions, change these if needbe
PRIMARY_KEY = "KID_IDFrameKey"
EULER_X = "EulerAngleX"
EULER_Y = "EulerAngleY"
EULER_Z = "EulerAngleZ"
OBJECT_NAME = 'Object'

#we probably only want the one renderer, pass in dimensions to the renderer object if you want something other than 800x600
RENDERER = ObjectRenderer(camera_distance=-35)

def generate_rendition(object_cache:dict, output_dir:os.PathLike, dataframe_row:pl.Series, renderer:ObjectRenderer=RENDERER):
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
    output_path = os.path.join(output_dir, f"rendition_{primary_key}.png")
    rendition.save(output_path)
    return primary_key

def main(input_csv:os.PathLike, output_directory:os.PathLike, object_directory:os.PathLike):
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

if __name__ == "__main__":
    parser = ArgumentParser(prog="generate renditions",
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
    main(
        input_csv=args.input_csv or INPUT_CSV,
        output_directory=args.output_directory or OUTPUT_DIRECTORY,
        object_directory=args.object_directory or OBJECT_DIRECTORY
    )