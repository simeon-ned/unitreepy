import numpy as np
from time import perf_counter


def leg_kinematics(q, l, r0):

    q1, q2, q3 = q
    r0_x, r0_y = r0
    l1, l2, l3 = l

    c1, s1 = np.cos(q1), np.sin(q1)
    c2, s2 = np.cos(q2), np.sin(q2)
    c23, s23 = np.cos(q2 + q3), np.sin(q2 + q3)

    position = np.array([-l2*s2 - l3*s23 + r0_x,
                         -l1*c1 + (l2*c2 + l3*c23)*s1 + r0_y,
                         -l1*s1 - (l2*c2 + l3*c23)*c1])

    jacobian = np.array([[0, -l2*c2 - l3*c23, -l3*c23],
                         [l1*s1 + (l2*c2 + l3*c23)*c1, -
                          (l2*s2 + l3*s23)*s1, -l3*s1*s23],
                         [-l1*c1 + (l2*c2 + l3*c23)*s1, (l2*s2 + l3*s23)*c1, l3*s23*s1]])

    rotation_matrix = np.array([[c23, s1*s23, -s23*c1],
                                [0, c1, s1],
                                [s23, -s1*c23, c1*c23]])
    # jacobian = np.zeros((3,3))
    # rotation_matrix = np.zeros((3,3))

    return position, jacobian, rotation_matrix


r0 = np.zeros(2)
l = np.array([0.0838, 0.2, 0.2])
for i in range(100):
    q = np.random.randn(3)
    t0 = perf_counter()
    position, jacobian, rotation_matrix = leg_kinematics(q, l, r0)
    t1 = perf_counter()
    print(1000*(t1 - t0)*4)



