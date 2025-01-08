from scipy.spatial.transform import Rotation
from novel_toy_tools.core.null_views_generator import NullViewsGenerator
import quaternion

class RotationDistributionScipy(NullViewsGenerator):
    def __init__(self):
        super().__init__()


    def get_angles(self, n):
        return super().get_angles(n)
    
    def generate_so3_samples(self, n):
        rotations = Rotation.random(n)
        quaternions = [quaternion.from_float_array(quat) for quat in rotations.as_quat()]
        return quaternions
    