from numpy import pi, sin, cos, array

def p2p_cos_profile(time, initial_pose, final_pose, terminal_time=2):
    
    q0 = array(initial_pose)
    qf = array(final_pose)
    t = time
    tf = terminal_time

    q = .5 * (q0 - qf) * cos(pi * t / tf) + .5 * (qf + q0)
    dq = .5 * pi * (qf - q0) * sin(pi * t / tf)/tf

    if t >= tf:
        q = final_pose
        dq = 0*final_pose

    return q, dq

def leg_kinematics(motor_angles, link_lengths, base_position):

    q1, q2, q3 = motor_angles
    r0_x, r0_y = base_position
    l1, l2, l3 = link_lengths

    c1, s1 = cos(q1), sin(q1)
    c2, s2 = cos(q2), sin(q2)
    c23, s23 = cos(q2 + q3), sin(q2 + q3)
    
    # calculate the position of the foot
    position = array([-l2*s2 - l3*s23 + r0_x,
                      -l1*c1 + (l2*c2 + l3*c23)*s1 + r0_y,
                      -l1*s1 - (l2*c2 + l3*c23)*c1])
    
    # jacobian of the foot position with respect to
    jacobian = array([[0, -l2*c2 - l3*c23, -l3*c23],
                      [l1*s1 + (l2*c2 + l3*c23)*c1, -
                          (l2*s2 + l3*s23)*s1, -l3*s1*s23],
                      [-l1*c1 + (l2*c2 + l3*c23)*s1, (l2*s2 + l3*s23)*c1, l3*s23*c1]])

    rotation_matrix = array([[c23, s1*s23, -s23*c1],
                             [0, c1, s1],
                             [s23, -s1*c23, c1*c23]])

    return position, jacobian, rotation_matrix

