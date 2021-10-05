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

