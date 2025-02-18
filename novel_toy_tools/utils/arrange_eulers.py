def arrange_eulers(euler_order:str, euler_x:float, euler_y:float, euler_z:float):
    """Takes an euler order and returns a tuple of the euler angles in that order"""
    euler_lookup = {
        "X": euler_x,
        "x": euler_x,
        "Y": euler_y,
        "y": euler_y,
        "Z": euler_z,
        "z": euler_z
    }
    #TODO throw a custom error if outside of 3
    if len(euler_order) != 3:
        raise ValueError
    else:
        return (euler_lookup[euler_order[0]],
                euler_lookup[euler_order[1]],
                euler_lookup[euler_order[2]])