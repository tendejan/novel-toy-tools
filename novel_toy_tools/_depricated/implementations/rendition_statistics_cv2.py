from novel_toy_tools.core.rendition_statistics import RenditionStatistics
import cv2
import numpy as np

class RenditionStatisticsCv2(RenditionStatistics):
    """an implementation for computing rendition statistics"""
    def __init__(self, path_to_image):
        self.path_to_image = path_to_image
        self.AVOID_HOLES = False #primarily a constant for setting the behavior of Longest Edge
        self.image_binarized = self.binarize_image()
        self.image_contours, self.image_contour_hierarchy = self.get_hull()
        super().__init__(path_to_image)

    def load_image(self, path_to_image):
        return cv2.imread(path_to_image)
    
    def binarize_image(self):
        #convert to greyscale
        im_gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        #NOTE I tried to set this threshold value as a constant at the start of the file but I was getting errors
        _, img_binarized = cv2.threshold(im_gray, 50, 255, cv2.THRESH_BINARY)
        return img_binarized

    def get_hull(self):
        #TODO throw err if no contours are found
        contours, hierarchy_tree = cv2.findContours(self.image_binarized, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        return contours, hierarchy_tree
    
    #NOTE this method for coputing area may be more useful if we are interested in internal hole structure at a later date
    # def compute_area_presented(self):
    #     areas = []
    #     for contour in self.image_contours:
    #         areas.append(cv2.contourArea(contour))
    #     return areas
    
    def compute_area_presented(self):
        white_space = np.count_nonzero(self.image_binarized)
        # black_space = self.image_binarized.size - white_space #may want the area presented as a proportion
        return white_space
        
    
    #TODO this function is very wrong, what really needs to happen here is such:
    #First compute all possible lines from hull, sort by size, grab the first one that passes validation
    #validation may be possible with an and function that checks line against image but this may need to be implemented by hand, alternatively investigate the dot product
    def compute_longest_edge(self):
        max_hull = self.image_contours[0] #TODO this may not return the largest hull
        longest_edge_length = 0
        longest_point1, longest_point2 = None, None
        pairs_visited = set()

        #TODO parallelize this, gpu or cpu
        for i in range(len(max_hull)):
            for j in range(i+1, len(max_hull)):
                #define the line
                point1, point2 = max_hull[i][0], max_hull[j][0]
                if ((point1[0], point1[1]), (point2[0], point2[1])) not in pairs_visited:
                    pairs_visited.add(((point1[0], point1[1]), (point2[0], point2[1])))
                    pairs_visited.add(((point2[0], point2[1]), (point1[0], point1[1])))
                    length = np.linalg.norm(point1 - point2)

                    if self.AVOID_HOLES:
                        image_with_line = self.image_binarized.copy()
                        cv2.line(image_with_line, point1, point2, 255, 1)
                        #TODO this is horrifically inefficient and needs to be changed so that it only checks the line instead of both images
                        if np.array_equal(image_with_line, self.image_binarized):
                            if length > longest_edge_length: #TODO gotta make sure this doesnt clip other hulls
                                longest_edge_length = length
                                longest_point1, longest_point2 = point1, point2
                    else:
                        if length > longest_edge_length:
                                longest_edge_length = length
                                longest_point1, longest_point2 = point1, point2
        return longest_edge_length, longest_point1, longest_point2
    
    def compute_planar_view(self):
        return super().compute_planar_view()
    
    def get_rendition_statistics(self):
        stats_dict = {}
        stats_dict["area"] = self.compute_area_presented()
        stats_dict["longest edge"] = self.compute_longest_edge()
        return stats_dict
    
