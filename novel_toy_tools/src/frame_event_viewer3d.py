from novel_toy_tools.core.abstract_frame_event import AbstractFrameEvent
from novel_toy_tools.core.abstract_renderer import AbstractRenderer
from novel_toy_tools.core.abstract_novel_toy import AbstractNovelToy
from novel_toy_tools.constants import VIEWER3D_EULER_ORDER
from scipy.spatial.transform import Rotation

from novel_toy_tools.src.wavefront_novel_toy import WavefrontNovelToy


class FrameEventViewer3d(AbstractFrameEvent):
    #TODO this should take as many args as possible and then default to None for any others,
    #then it can dynamically generate the NONES

    def inject_computed_statistics(self, stats_dict:dict):
        return super().inject_computed_statistics(stats_dict)