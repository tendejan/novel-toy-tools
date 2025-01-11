from novel_toy_tools.implementations.get_experiment_data import ExperimentalDataFromConsolidated
from novel_toy_tools.implementations.render_opengl import OpenGLViewRenderer
import os

EXPERIMENTAL_DATA = "/Users/tendejan/Desktop/Tom Endejan Novel Toy 2024/data/experimental/OldDataSheet.csv"
OUTPUT_DIR = "/Users/tendejan/Desktop/Tom Endejan Novel Toy 2024/data/experimental/generated"

renderer = OpenGLViewRenderer(600, 800)
experimental_data = ExperimentalDataFromConsolidated(in_file=EXPERIMENTAL_DATA, output_directory=OUTPUT_DIR)

os.makedirs(OUTPUT_DIR, exist_ok=True)
for data_point in experimental_data:
    if data_point:
        current_object = experimental_data.get_current_object()
        out_dir = os.path.join(OUTPUT_DIR, current_object)
        #check that the dir exists
        os.makedirs(out_dir, exist_ok=True)
        outpath = os.path.join(out_dir, experimental_data.get_rendition_name())
        view_path = renderer.render_single_view(*data_point, outpath)
        print("saving " + experimental_data.get_rendition_name())
        experimental_data.link_rendition(view_path)
master_data_sheet_path = os.path.join(OUTPUT_DIR, 'master_data_sheet.csv')
experimental_data.dataframe.to_csv(master_data_sheet_path)
