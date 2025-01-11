# TODO mark part of this code as partially gpt generated
import numpy as np
from typing import List

#TODO conform to interface
class fibbonacciSpiralDataProvider(GeneratedDataProvider):
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
        z = 1 - 2*(indicies + 0.5) / num_samples
        radius = np.sqrt(1 -  z ** 2)

        x = radius * np.cos(theta)
        y = radius * np.sin(theta)

        w = np.zeros_like(x)
        points = np.column_stack((w, x, y, z))
        points /= np.linalg.norm(points, axis=1)[:, np.newaxis]

        return points

    def generate_uniform_rotations(num_samples:int) -> List:
        points = fibonacci_sphere_points(num_samples)

        quaternions = [quaternion.from_float_array(p) for p in points]

        # normalize again for sanity

        quaternions = [q.normalized() for q in quaternions]

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
            distances = np.linalg.norm(q_arr - sample_quaternions[i], axis=1)
            distances = distances[distances > 1e-6]

            min_dist = min(min_dist, np.min(distances))
            max_dist = max(max_dist, np.max(distances))

        return {
            'num_rotations': n,
            'min_distance': min_dist,
            'max_distance': max_dist,
            'max to min ratio': max_dist/min_dist if min_dist>0 else float('inf')
        }