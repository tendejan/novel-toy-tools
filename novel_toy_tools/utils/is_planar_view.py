from typing import List
#TODO remove specific import depts to generalize function better and make more maintainable (DI)
from scipy.spatial.transform import Rotation
from itertools import combinations
import numpy as np

PI = np.pi
VIEWER_3D_PERSPECTIVE_VECTOR = np.asarray([0, 1, 0])

def degree_to_rad(theta:float) -> float:
    return theta*PI/180

def normalize(vector:np.ndarray) -> np.ndarray:
    """Simple function for normalizing vectors
    Args:
        vector:np.ndarray(3,)
    Returns:
        np.ndarray: normalized vector
    
    """
    norm = np.linalg.norm(vector)
    if norm == 0:
        raise ValueError("Cannot normalize a zero vector")
    return vector/norm

#thank god for the cross product in 3d, call me when we're doing planar view in 7d
def is_colinear(vec1:np.ndarray, vec2:np.ndarray) -> bool:
    """Simple function to check if two 3d vectors are colinear.
    Args:
        vec1:np.ndarray(3,)
        vec2:np.ndarray(3,)
    Returns:
        bool: wether or not vectors are colinear.
    """
    cross = np.cross(vec1, vec2)
    return not np.any(cross)

#TODO add the trivial case
def has_colinear_planarity(object_major_axes:List[np.ndarray]) -> bool:
    """Checks if all major axis are colinear.
    
    Args:
        object_major_axes (List[np.ndarray(3,)]): a set of major axes defined for the object

    Returns:
        bool: wether or not all major axes are colinear
    """
    #remove any null space vectors, normalize any input vectors
    non_zero_vectors = []
    for vector in object_major_axes:
        if vector.any():
            non_zero_vectors.append(normalize(vector))

    #if no more axis are present raise a value error
    if len(non_zero_vectors) == 0:
        raise ValueError("No non-zero axes were provided")


    pairs = list(combinations(non_zero_vectors, 2))
    colinear_list = list([is_colinear(first_axis, second_axis) for first_axis, second_axis in pairs])
    colinear = np.all(colinear_list)
    return colinear

def is_planar_view(object_rotation:Rotation,
                    object_major_axes:List[np.ndarray],
                    planar_view_threshold:float,
                    degrees:bool=True,
                    viewer_perspective:np.ndarray=VIEWER_3D_PERSPECTIVE_VECTOR,
                    ) -> bool:
    """Calculates whether a view of an object is planar.
    
    Args:
        object_rotation: representation of a view of the rotated object.
        object_major_axes: a tuple of Rotations specifying the major axes for a given object.
        degrees (bool): wether or not to take planar_view_threshold as degrees or radians
        planar_view_threshold (float): accuracy specification of wether or not a view is considered planar. 
        viewer_perspective: a vector representation of the viewpoint.

    Returns:
        bool: wether or not the view is considered planar.
    """
    #filter out all the zero length axes
    #TODO norm the vectors here
    non_zero_object_major_axes = list(filter(np.any, object_major_axes))
    #Threshold gets converted from angle to magnitude for working with dot product
    if degrees:
        #assuming vectors are normalized
        planar_view_threshold = np.cos(degree_to_rad(planar_view_threshold))
    else:
        planar_view_threshold = np.cos(planar_view_threshold)

    #TODO I could do this in one loop by checking colinear planarity in loop but im not sure which is more readable
    #apply rotation to all axes
    for pair in combinations(non_zero_object_major_axes, 2):
        #if both vectors are non zero and they are orthogonal to each other
        if (np.any(pair[0]) and np.any(pair[1])) and np.dot(pair[0], pair[1]) == 0:
            #Add the orthogonal vector to the set of axes for planar views that are perpindicular to a pair of major axes
            non_zero_object_major_axes.append(np.cross(pair[0], pair[1]))

    rotated_axes = [object_rotation.apply(axis) for axis in non_zero_object_major_axes]

    #if object has colinear planarity then it should have 2 + infinity planar axes where the infinite axes are a plane orthogonal to the main axes
    if has_colinear_planarity(rotated_axes):
        for axis in rotated_axes:
            dot = viewer_perspective.dot(axis)
            #so just find where dot product of view is within threshold of one or zero (all orthogonal views are planar in this case)
            orthogonal_view_threshold = (1-planar_view_threshold)
            if np.abs(dot) >= planar_view_threshold or np.abs(dot) <= orthogonal_view_threshold:
                #If it has a planar view return early
                return True
        #no planar views were found, finally return false
        return False
    else:
        #slightly different case, only return if the dot product is parallel
        for axis in rotated_axes:
            dot = viewer_perspective.dot(axis)
            if np.abs(dot) >= planar_view_threshold:
                #Planar view found, return early
                return True
        #no planar views found, finally return false
        return False