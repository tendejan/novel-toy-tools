from novel_toy_tools.rendition_dataset_pipeline import RenditionDatasetPipeline
from novel_toy_tools.implementations.render_opengl_quaternion import OpenGLViewRenderer as Renderer
from novel_toy_tools.implementations.generate_SO3_scipi import RandomSampleDataProvider as GeneratedDataProvider
from novel_toy_tools.implementations.get_experiment_data import ExperimentalDataFromConsolidated as ExperimentDataProvider

EXPERIMENTAL_DATA = "/data/experimental/OldDataSheet.csv"
OUTPUT_DIR = '/tests/test_renditions'

if __name__ == "__main__": #TODO take args
    renderer = Renderer()
    generated_data = GeneratedDataProvider()
    experiment_data = ExperimentDataProvider(in_file=EXPERIMENTAL_DATA, output_directory=OUTPUT_DIR)

    pipeline = RenditionDatasetPipeline(renderer, generated_data, experiment_data)
    pipeline.generate_dataset(EXPERIMENTAL_DATA, OUTPUT_DIR)