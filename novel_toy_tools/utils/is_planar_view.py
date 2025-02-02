#TODO remove specific import depts to generalize function better and make more maintainable (DI)
from typing import List
from scipy.spatial.transform import Rotation
from itertools import combinations
import numpy as np

VIEWER_3D_PERSPECTIVE_VECTOR = np.asarray([0, 1, 0])

#TODO normalize check
def normalize(vector:np.ndarray) -> np.ndarray:
    """Simple function for normalizing vectors
    Args:
        vector:np.ndarray
    Returns:
        np.ndarray: normalized vector
    
    """
    norm = np.linalg.norm(vector)
    return vector/norm

def is_colinear(vec1:np.ndarray, vec2:np.ndarray) -> bool:
    """Simple function to check if two 3d vectors are colinear.
    Args:
        vec1:np.ndarray
        vec2:np.ndarray
    Returns:
        bool: wether or not vectors are colinear.
    """
    cross = np.cross(vec1, vec2)
    if np.any(cross): return False
    else: return True

def has_colinear_planarity(object_major_axes:List[np.ndarray]) -> bool:
    """Checks if all major axis are colinear.
    
    Args:
        object_major_axes (List[np.ndarray]): a set of major axes defined for the object

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
    colinear = np.allclose(colinear_list)
    return colinear

#TODO make the planar view threshold take an angle (in radians prob) as threshold instead of float (should be by some cos)
def is_planar_view(viewer_perspective:np.ndarray, object_rotation:Rotation, object_major_axes:List[np.ndarray], planar_view_threshold:float) -> bool:
    """Calculates whether a view of an object is planar.
    
    Args:
        viewer_perspective: a vector representation of the viewpoint.
        object_rotation: representation of a view of the rotated object.
        object_major_axes: a tuple of Rotations specifying the major axes for a given object.
        planar_view_threshold (float): accuracy specification of wether or not a view is considered planar. 

    Returns:
        bool: wether or not the view is considered planar.
    """
    #TODO I could do this in one loop by checking colinear planarity in loop but im not sure which is more readable
    #apply rotation to all axes
    rotated_axes = [object_rotation.apply(axis) for axis in object_major_axes]
    #if object has colinear planarity then it should have 2 + infinity planar axes where the infinite axes are a plane orthogonal to the main axes
    if has_colinear_planarity(object_major_axes):
        for axis in rotated_axes:
            dot = viewer_perspective.dot(axis)
            #so just find where dot product of view is within threshold of one or zero (all orthogonal views are planar in this case)
            if np.abs(dot) <= (0 + planar_view_threshold) or np.abs(dot) >= (1 - planar_view_threshold):
                #If it has a planar view return early
                return True
        #no planar views were found, finally return false
        return False
    else:
        #slightly different case, only return if the dot product is parallel
        for axis in rotated_axes:
            dot = viewer_perspective.dot(axis)
            if np.abs(dot) >= (1 - planar_view_threshold):
                #Planar view found, return early
                return True
        #no planar views found, finally return false
        return False
    
#TODO unittest