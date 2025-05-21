from novel_toy_tools.core.abstract_data_manager import AbstractDataManager
from novel_toy_tools.src.csv_data_writer import ExperimentalDataWriter
from novel_toy_tools.src.opengl_renderer import ObjectRenderer
from novel_toy_tools.src.wavefront_novel_toy import WavefrontNovelToy
from novel_toy_tools.src.frame_event_viewer3d import FrameEventViewer3d #TODO im pretty sure I should just get rid of this and use the abstract clas

from novel_toy_tools.src.experimental_data_provider import ExperimentalDataProviderFromConsolidated
from novel_toy_tools.src.null_distribution_data_provider import NullDistributionDataProvider

#TODO refactor these for DI
from novel_toy_tools.src.image_analysis import ImageProcessor

from scipy.spatial.transform import Rotation
from novel_toy_tools.my_secrets import *
from novel_toy_tools.constants import *
from novel_toy_tools.utils import arrange_eulers


from tqdm import tqdm

OBJECT_DICT = {'AirplaneNovel': 1332,
 'Camera': 1033,
 'ShovelNovel': 936,
 'Cup': 822,
 'CribNovel': 1873,
 'Crib': 646,
 'CupNovel': 1424,
 'CameraNovel': 1051,
 'Shoe': 884,
 'HighChairNovel': 982,
 'Train': 1554,
 'ShoeNovel': 1238,
 'TrainNovel': 1127,
 'Airplane': 852,
 'HighChair': 1242,
 'Shovel': 1401}

class ConcreteDataManager(AbstractDataManager):
    def __init__(self, data_provider, data_writer, analysis_package, renderer):
        super().__init__(data_provider, data_writer, analysis_package, renderer)
        self.frame_events = []

    def load_frame_events(self): #TODO this should be made parallelizabl and split into seperate functions
        for row in tqdm(self.data_provider, desc="loading frame events", total=self.data_provider.height()):
            #init frame event
            frame_event = FrameEventViewer3d(row)

            #get rotation
            eulers = arrange_eulers(VIEWER3D_EULER_ORDER, row[' x'], row[' y'], row[' z'])
            frame_event.rotation = Rotation.from_euler(VIEWER3D_EULER_ORDER, eulers, degrees=True)

            #get novel_toy as refrence to shared object
            frame_event.novel_toy = self.toy_objects_cache[row['3d object']]

            #TODO this may be the slowest part of the computation, may want do do this in passes
            #get rendition
            frame_event.rendition = renderer.generate_rendition(frame_event.novel_toy, frame_event.rotation)

            #ok now compute the rendition props and inject them into the frame event
            # image_processor = ImageProcessor(frame_event.rendition)
            # frame_event.inject_computed_statistics(image_processor.get_image_statistics())

            self.frame_events.append(frame_event)
            



    def process_data(self): #TODO maybe rename this to be more specifically about getting the shared data
        #create the novel toy objects
        self.toy_objects_cache = {}
        for toy_name in self.data_provider.get_toys():
            self.toy_objects_cache[toy_name] = WavefrontNovelToy(toy_name, r"/Users/tendejan/Desktop/Alfredo Higher Order Image Properties/PVMDA 7-0 Frame Data Merged Computed/PrefViews 3D objects")
        
        self.load_frame_events()
        
        self.data_writer.write(self.frame_events)



if __name__ == "__main__":
    #init depts
    # data_provider = ExperimentalDataProviderFromConsolidated(EXPERIMENTAL_CSV_FROM_CONSOLIDATED)
    data_provider = NullDistributionDataProvider(OBJECT_DICT)
    data_writer = ExperimentalDataWriter(r"/Users/tendejan/Desktop/Alfredo Higher Order Image Properties/PVMDA 7-0 Frame Data Merged Computed/stochastic/renditions", r"/Users/tendejan/Desktop/Alfredo Higher Order Image Properties/PVMDA 7-0 Frame Data Merged Computed/stochastic/rendition_data.csv")
    # analysis_package = FrameAnalysis() #TODO refactor and then inject this
    renderer = ObjectRenderer(*VIEWER3D_RENDITION_DIMENTIONS, -35)

    #inject #TODO fix the analysis package injection
    data_manager = ConcreteDataManager(data_provider, data_writer, None, renderer)

    #proceed
    data_manager.process_data()