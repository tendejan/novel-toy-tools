import cv2
import numpy as np
from PIL import Image
from scipy.spatial.distance import cdist

#TODO maybe implement method chaining on this object
class ImageProcessor:
    """an implementation for computing various image properties and the intermediary steps"""
    def __init__(self, image:Image):
        self.image_statistics = {}
        self.image = np.array(image)
        self.image_gray = self.convert_grayscale(self.image)
        self.image_binary = self.convert_binary(self.image_gray)
        self.im_array_contours, self.image_contour_hierarchy = None, None
        self.area_presented = self.compute_area_presented(self.image_binary)
        self.longest_line = self.compute_longest_line(self.image_binary)
        self.max_distance = None

    def convert_binary(self, gray, threshold=cv2.THRESH_BINARY) -> np.ndarray:
        _, image_binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        self.image_binary = image_binary
        return image_binary

    def convert_grayscale(self, image:np.ndarray) -> np.ndarray:
        self.image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        return self.image_gray

    def compute_area_presented(self, image:np.ndarray):
        whitespace = np.count_nonzero(image)
        self.area_presented = whitespace
        self.image_statistics.update({"area presented": whitespace})
        return whitespace
    
    def compute_longest_line(self, image:np.ndarray):
        contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if not contours:
            return None, 0
        
        points = contours[0].reshape(contours[0].shape[0], 2)

        dist_matrix = cdist(points, points)
        i, j = np.unravel_index(np.argmax(dist_matrix), dist_matrix.shape)

        max_dist = dist_matrix[i,j]
        point1 = points[i]
        point2 = points[j]

        props_dict = {
            "longest line distance": max_dist,
            "line point1 x": point1[0],
            "line point1 y": point1[1],
            "line point2 x": point2[0],
            "line point2 y": point2[1],
        }
        self.image_statistics.update(props_dict)

        return max_dist, (point1, point2)
    
    def get_image_statistics(self):
        return self.image_statistics