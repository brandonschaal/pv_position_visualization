import maya.cmds as cmds
import maya.OpenMaya as om


def calculate_pv_pos(start_jnt, mid_jnt, end_jnt):
    """
    Calculates the position of a pole vector in plane of three joints and moves locators
    that are connected to nurbs curve control points at each step to visualize the vectors.
    Intended to be used with "pv_pos_vector_math_visual.ma" maya scene.
    
    Args:
    	start_jnt: (string) name of start joint
    	mid_jnt: (string) name of middle joint
    	end_jnt: (string) name of end joint
    	
    Returns:
    	(tuple) of translations of the pole vector position
    """
    
    # Getting joint translations
    start_x, start_y, start_z = cmds.xform(start_jnt, query=True, worldSpace=True, translation=True)
    mid_x, mid_y, mid_z = cmds.xform(mid_jnt, query=True, worldSpace=True, translation=True)
    end_x, end_y, end_z = cmds.xform(end_jnt, query=True, worldSpace=True, translation=True)

    # MVector objects for vectors
    start_v = om.MVector(start_x, start_y, start_z)
    mid_v = om.MVector(mid_x, mid_y, mid_z)
    end_v = om.MVector(end_x, end_y, end_z)

    # End minus start vector
    start_end = end_v - start_v
    cmds.xform('end_minus_start_vector_LOC', translation=start_end)
        
    # Mid minus start vector
    start_mid = mid_v - start_v
    cmds.xform('mid_minus_start_vector_LOC', translation=start_mid)
        
    # Getting dot product for projection
    dot_product = start_mid * start_end

    # Projection vector for mid point of start and end joint
    projection = dot_product / start_end.length()
    start_end_n = start_end.normal()
    projection_v = start_end_n * projection
    cmds.xform('startEnd_normal_mult_projection_vector_LOC', translation=projection_v)

    # Vector that points down joint chain plane
    plane_v = (start_mid - projection_v).normal()
    cmds.xform('plane_vector_LOC', translation=plane_v)

    # Getting three quarters length of the joint chain length and scaling the plane vector
    chain_len = ((mid_v - start_v).length() + (end_v - mid_v).length()) * 0.75
    plane_v_scaled = plane_v * chain_len
    cmds.xform('plane_scaled_vector_LOC', translation=plane_v_scaled)
        
    # Positioning pole vector
    pole_vector = plane_v_scaled + mid_v
    cmds.xform('plane_scaled_vector_plus_mid_vector_LOC', translation=pole_vector)
    
    return (pole_vector.x, pole_vector.y, pole_vector.z)


if __name__ == '__main__':
	pv_pos = calculate_pv_pos('joint1', 'joint2', 'joint3')
	print(pv_pos)
