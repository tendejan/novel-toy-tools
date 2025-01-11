from novel_toy_tools.core.view_renderer import ViewRenderer
from novel_toy_tools.core.data_provider import DataProvider

class RenditionDatasetPipeline:
    def __init__(self, view_renderer:ViewRenderer, generated_data_provider:DataProvider, experiment_data_provider:DataProvider):
        self.view_renderer = view_renderer
        self.generated_data_provider = generated_data_provider
        self.experiment_data_provider = experiment_data_provider

    def generate_dataset(self, in_path, out_path):
        self.view_renderer.render_all_views(self.generated_data_provider)
        self.view_renderer.render_all_views(self.experiment_data_provider)