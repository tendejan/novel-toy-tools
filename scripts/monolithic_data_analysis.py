import polars as pl
import os
from scipy.spatial.transform import Rotation
from novel_toy_tools.utils.is_planar_view import is_planar_view
from novel_toy_tools.interfaces.abstract_frame_event import AbstractFrameEvent
from novel_toy_tools.interfaces.abstract_renderer import AbstractRenderer
from novel_toy_tools.src.wavefront_novel_toy import WavefrontNovelToy
from novel_toy_tools.src.viewer3d_frame_event import Viewer3dFrameEvent
from novel_toy_tools.src.opengl_renderer import OpenGlRenderer
from novel_toy_tools.constants import *

from tqdm import tqdm

import multiprocessing


class FrameEventAnalyser:
    def __init__(self, frame_event:AbstractFrameEvent):
        self.frame_event = frame_event

    def generate_rendition(self, renderer:AbstractRenderer):
        self.frame_event.rendition = renderer.generate_rendition()
    
    def compute_planarity(self, planar_view_funct):
        pass

def generate_null_datasheet(samples_per_toy:dict, schema):
    #TODO this should take a schema and try to generate values to conform to the schema
    rows = []
    for toy in samples_per_toy.keys():
        for frame in range(samples_per_toy[toy]):
            eulers = Rotation.random().as_euler("XYZ", degrees=True)
            filename = f"null_rendition_{toy}_at_x{eulers[0]}_y{eulers[1]}_z{eulers[2]}.png"
            row = [filename, 0, 00000, frame, None, 1, eulers[0], eulers[1], eulers[2], -1, -1, "null", toy] #TODO ok for now Im removing camera type "virtual" but this should be handled
            rows.append(row)
    return pl.DataFrame(rows, schema=schema)

def get_toys(dataframe:pl.DataFrame):
    toy_objects = {}
    toy_names = dataframe["3d object"].unique()
    for toy_name in toy_names:
        toy_objects[toy_name] = WavefrontNovelToy(toy_name)
    return toy_objects

#TODO for rendering we probably want to chunkify based on novel_toy object
def chunkify_dataframe(data_frame:pl.DataFrame, num_chunks):
    chunk_size = len(data_frame) // num_chunks
    chunks = []
    for i in range(num_chunks):
        start = i * chunk_size
        end = (i+1) * chunk_size if i < num_chunks -1 else len(data_frame)
        chunks.append(data_frame[start:end].rows())
    return chunks

def create_frame_events(rows, frame_object_type:AbstractFrameEvent):
    frame_event_objects = []
    for row in rows:
        frame_event_objects.append(frame_object_type(*row))
    return frame_event_objects

def chunkify_objects(frame_objects, num_chunks):
        chunk_size = len(frame_objects) // num_chunks
        chunks = []
        for i in range(num_chunks):
            start = i*chunk_size
            end = (i+1) * chunk_size if i<num_chunks-1 else len(frame_objects)
            chunks.append(frame_objects[start:end])
        return chunks


#TODO take these as args
CSV_INPUT_PATH_EXPERIMENTAL = os.path.normpath(r"/Users/tendejan/Desktop/Tom Endejan Novel Toy 2024/data/experimental/OldDataSheet.csv")
NUM_CORES = os.cpu_count()
if __name__ == "__main__":
    #import the data
    INPUT_DATAFRAME_EXPERIMENTAL = pl.read_csv(CSV_INPUT_PATH_EXPERIMENTAL).drop_nulls(subset=[" x", ' y', ' z'])
    TOY_OBJECTS = get_toys(INPUT_DATAFRAME_EXPERIMENTAL)
    chunks = chunkify_dataframe(INPUT_DATAFRAME_EXPERIMENTAL, NUM_CORES - 1)

    #create the frameobjects parallel
    chunks_with_args = [(chunk, Viewer3dFrameEvent) for chunk in chunks]
    with multiprocessing.Pool(processes=NUM_CORES - 1) as pool:
        frame_objects = pool.starmap(create_frame_events, chunks_with_args)
    frame_event_objects_experimental = [item for sublist in frame_objects for item in sublist ]

    #find counts of each toy for the null data sheet payload
    null_payload = {}
    for toy in TOY_OBJECTS:
        null_payload[toy] = INPUT_DATAFRAME_EXPERIMENTAL.filter(pl.col('3d object') == toy).height
    #create the null distribution
    NULL_INPUT_DATAFRAME = generate_null_datasheet(null_payload, INPUT_DATAFRAME_EXPERIMENTAL.schema)

    #create the null_frame objects parallel
    chunks = chunkify_dataframe(NULL_INPUT_DATAFRAME, NUM_CORES-1)
    chunks_with_args = [(chunk, Viewer3dFrameEvent) for chunk in chunks]
    with multiprocessing.Pool(processes=NUM_CORES-1) as pool:
        null_frame_objects = pool.starmap(create_frame_events, chunks_with_args)
    frame_event_objects_null = [item for sublist in null_frame_objects for item in sublist ]
    #ok now we start the advanced processing
    #we have all the toy objects, now we need to iterate through the frame events and compute the renditions, then compute the statistics

    #frame_event_objects_null
    #frame_event_objects_experimental
    #give them renditions
    
    pbar = tqdm(frame_event_objects_experimental)
    for frame_object in frame_event_objects_experimental:
        #get the rotation
        #TODO would be nicer to just pass the frame event in here probably, that may force the computer to not share novel_toy_oject tho
        #TODO the architecture here is funky, the frame_event should probably just have a rendition image and then an analysis object should decide what to do with it
        #TODO DataManager should probably take the Nove_toy object as an arg as well as datawriter and dataprovider and renderer
        #TODO also its weird to use the TOY_OBJECTS dict to get the wavefront object here, rethink that perhaps
        this_toy = TOY_OBJECTS[frame_object.novel_toy_name]
        #TODO implement a method for grabbing the rotation from the frame_event class
        #TODO you may want to save the rotated toy data in the frame_object file for some sort of weird center of mass analysis or whatever
        this_rotation_xyz = Rotation.from_euler(VIEWER3D_EULER_ORDER, (frame_object.euler_x, frame_object.euler_y, frame_object.euler_z), degrees=True)
        frame_object.rendition = renderer.generate_rendition(this_toy, this_rotation_xyz)
        pbar.update(1)

    def generate_and_link(TOYS, frame_object, renderer):
        this_toy = TOY_OBJECTS[frame_object.novel_toy_name]
        frame_object.get_rendition(renderer)

    chunks = chunkify_objects(frame_event_objects_experimental, NUM_CORES-1)
    renderer = OpenGlRenderer(*VIEWER3D_RENDITION_DIMENTIONS)
    with multiprocessing.Pool(NUM_CORES -1) as pool:
        rendition_objects = list(tqdm(pool.starmap(generate_and_link, chunks), total=len(chunks)))

    print("did it work?")
