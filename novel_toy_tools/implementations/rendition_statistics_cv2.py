from novel_toy_tools.core.rendition_statistics import RenditionStatistics
import cv2
import pandas as pd
import numpy as np

class RenditionStatisticsCv2(RenditionStatistics):
    """an implementation for computing rendition statistics"""
    def __init__(self, path_to_image):
        self.path_to_image = path_to_image
        self.image = self.load_image(path_to_image)
        self.image_binarized = self.binarize_image()
        self.image_contours, self.image_contour_hierarchy = self.get_hull()
        super().__init__(path_to_image)

    def load_image(self, path_to_image):
        #TODO I think this sets image to self.image in the base class although ya gonna have to check
        return cv2.imread(path_to_image)
    
    def binarize_image(self):
        #convert to greyscale
        im_gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        #NOTE I tried to set this threshold value as a constant at the start of the file but I was getting errors
        _, img_binarized = cv2.threshold(im_gray, 50, 255, cv2.THRESH_BINARY)
        return img_binarized

    def get_hull(self):
        contours, hierarchy_tree = cv2.findContours(self.image_binarized, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE, )
        return contours, hierarchy_tree
    
    def compute_area_presented(self):
        #TODO subtract inner areas
        areas = []
        for contour in self.image_contours:
            areas.append(cv2.contourArea(contour))
        return areas
    
    def line_clipps_interior_hull(self, point1, point2) -> bool:
        pass
    
    def compute_longest_edge(self):
        max_hull = self.image_contours[0]
        #TODO gonna need to get contour hierarchy after all
        longest_edge_length = 0
        point1, point2 = None, None
        for i in range(len(max_hull)):
            for j in range(i+1, len(max_hull)):
                length = np.linalg.norm(max_hull[i][0] - max_hull[j][0])
                if length > longest_edge_length: #TODO gotta make sure this doesnt clip other hulls
                    longest_edge_length = length
                    point1, point2 = tuple(max_hull[i][0]), tuple(max_hull[j][0])
        return longest_edge_length, point1, point2
    
    def compute_planar_view(self):
        return super().compute_planar_view()
    
    def get_rendition_statistics(self):
        stats_dict = {}
        stats_dict["area"] = self.compute_area_presented()
        stats_dict["longest edge"] = self.compute_longest_edge()
        return stats_dict
    
