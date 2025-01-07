# TODO mark part of this code as partially gpt generated

from novel_toy_tools.core.null_views_generator import NullViewsGenerator
import numpy as np
import quaternion
from typing import List

def fibonacci_sphere_points(num_samples:int) -> np.ndarray:
    """Generate points on a the unit sphere using the Fibonacci spiral method.
    
    Args:
        num_samples (int): number of points to generate

    Returns:
        np.ndarray: array of shape (num_samples, 4) of quaternions on S3
    """

    phi = (1+np.sqrt(5))/2

    indicies = np.arange(num_samples)
    theta = 2*np.pi * indicies / phi
    phi1 = np.arccos(1- 2*(indicies + 0.5) / num_samples)

    # generate the points
    w = np.cos(theta) * np.sin(phi1)
    x = np.sin(theta) * np.sin(phi1)
    y = np.cos(phi1)
    z = np.zeros_like(w)

    # additional rotation in 4d to spread points evenly
    psi = np.pi * indicies / num_samples
    w_new = w * np.cos(psi) - z * np.sin(psi)
    x_new = x
    y_new = y
    z_new = w * np.sin(psi) + z * np.cos(psi)

    points = np.column_stack((w_new, x_new, y_new, z_new))
    points /= np.linalg.norm(points, axis=1)[:, np.newaxis]

    return points

def generate_uniform_rotations(num_samples:int) -> List:
    points = fibonacci_sphere_points(num_samples)

    quaternions = [quaternion.from_float_array([w, x, y, z]) for w, x, y, z in points]

    # normalize again for sanity
    quaternions = [q / np.sqrt(q.norm()) for q in quaternions]

    return quaternions

def check_coverage_metrics(quaternions: List) -> dict:
    n = len(quaternions)
    q_arr = np.array([quaternion.as_float_array(q) for q in quaternions])

    min_dist = float('inf')
    max_dist = 0

    sample_size = min(n, 1000)
    sample_indices = np.random.choice(n, sample_size, replace=False)
    sample_quaternions = q_arr[sample_indices]

    for i in range(sample_size):
        distances = np.abs(np.dot(sample_quaternions[i], q_arr.T))
        distances = distances[distances < 0.999999]

        min_dist = min(min_dist, np.min(distances))
        max_dist = max(max_dist, np.max(distances))

    return {
        'num_rotations': n,
        'min_distance': min_dist,
        'max_distance': max_dist,
        'max to min ratio': max_dist/min_dist if min_dist>0 else float('inf')
    }

class GenerateSO3(NullViewsGenerator):
    def get_angles(self):

        return super().get_angles()