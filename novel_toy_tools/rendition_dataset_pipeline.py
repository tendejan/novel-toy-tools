from core.null_views_generator import NullViewsGenerator
from core.view_renderer import ViewRenderer
from core.experiment_data_provider import ExperimentDataProvider

class RenditionDatasetPipeline:
    def __init__(self, null_views_generator:NullViewsGenerator, experiment_data_provider:ExperimentDataProvider, view_renderer:ViewRenderer ):
        self.null_views_generator = null_views_generator
        self.experiment_data_provider = experiment_data_provider
        self.view_renderer = view_renderer

    def generate_dataset(self, outpath): #TODO ok so we could split the csv into its constituent parts but I think it makes more sense here to keep the entries consistent
        self.null_angles = self.null_views_generator.get_angles() #TODO it might make more sense to do every object in one pass
        self.experiment_data = self.experiment_data_provider.get_data()
        #TODO render the null and experimental datasets here
        self.view_renderer.render_views()
        self.view_renderer.render_views()
        #TODO create pandas dataframe here with the object, original image path (null), rendered image path
        #TODO create a pandas dataframe with object, original image path, rendered image path

    #TODO maybe use euler angles or use quaternions