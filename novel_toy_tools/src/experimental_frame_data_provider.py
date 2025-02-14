from novel_toy_tools.core.abstract_frame_data_provider import FrameDataProvider
#TODO derivitive NovelToy should be in this class
#TODO write a better docstring

class ExperimentalFrameData(FrameDataProvider):
    def __init__(self):
        #TODO take dir path and deal with combining csv's
        #TODO add iteraor init logic
        super().__init__()

    def __iter__(self):
        return super().__iter__()
    
    def __next__(self):
        #TODO function should return pandas row
        return super().__next__()
    
    def get_rendition_name(self):
        return super().get_rendition_name()