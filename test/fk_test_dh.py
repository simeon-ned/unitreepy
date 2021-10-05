from sympy.utilities.codegen import codegen
from lib._constants import LEG_KINEMATICS, BODY_DIMENSIONS
from symbolical_dynamics.euler_lagrange import MechanicalSystem
from sympy import Matrix, symbols, cos, sin, simplify, pi, eye, zeros
# from sympy import rot_axis1 as Rx
# from sympy import rot_axis2 as Ry
# from sympy import rot_axis3 as Rz
# from sympy import rot_axis1 as Rx, Ry, Rz


l1, l2, l3 = symbols(r'l_1, l_2, l_3')
r0_x, r0_y = symbols(r'r0_x, r0_y')
q1, q2, q3 = symbols(r'q1, q2, q3')



def homogeneous_transform(theta, d, a, alpha):

    c_t, s_t = cos(theta), sin(theta)
    c_a, s_a = cos(alpha), sin(alpha)

    A = Matrix(
        [[c_t, - s_t*c_a, s_t*s_a, a*c_t],
         [s_t, c_t*c_a, -c_t*s_a, a*s_t],
         [0, s_a, c_a, d],
         [0, 0, 0, 1]])
    return A


theta = [pi/2, pi/2 + q1, q2+pi, q3, pi/2]
d = [0, 0, l1, 0, 0]
a = [0, 0, l2, l3, 0]
alpha = [pi/2, -pi/2, 0, 0, pi/2]

A = eye(4)
for i in range(5):
    A_T = homogeneous_transform(theta[i], d[i], a[i], alpha[i])
    A = A @ A_T 
    # print(A)

print(simplify(A[0,3]))
print(simplify(A[1,3]))
print(simplify(A[2,3]))

# print(simplify(A[3, 0]))
# print(simplify(A[3, 1]))
# print(simplify(A[3, 2]))
