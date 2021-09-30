from sympy.utilities.codegen import codegen
from sympy import Matrix, symbols, cos, sin, simplify, pi, eye, zeros
from sympy import rot_axis1 as Rx
from sympy import rot_axis2 as Ry
from sympy.algebras.quaternion import Quaternion

# from sympy import rot_axis1 as Rx, Ry, Rz


l1, l2, l3 = symbols(r'l_1, l_2, l_3')
t_l, t_w = symbols(r't_l, t_w')
q1, q2, q3 = symbols(r'q1, q2, q3')


def homogeneous_transform(R, r):
    A = eye(4)
    A[:3,:3] = R
    A[3, :3] = r
    return A

R01 = Rx(q1)

A = []

A01 = homogeneous_transform(Rx(q1), Matrix([[0,0,0]])) 
A12 = homogeneous_transform(eye(3), Matrix([[0,-l1,0]])) 
A23 = homogeneous_transform(Ry(q2), Matrix([[0,0,0]])) 
A34 = homogeneous_transform(eye(3), Matrix([[0,0,-l2]]))
A45 = homogeneous_transform(Ry(q3), Matrix([[0,0,0]])) 
A56 = homogeneous_transform(eye(3), Matrix([[0,0,-l3]])) 


A = A56@A45@A34@A23@A12@A01
# R = simplify(A[:3,:3])
# print(R, '\n')
# print(R[0,:])
# print(R[1,:])
# print(R[2,:])



r = simplify(A[3, :])
print(r[0])
print(r[1])
print(r[2])

q = Matrix([q1, q2, q3])

J = simplify(r.jacobian(q))
print(J[0,:])
print(J[1,:])
print(J[2,:])


# quat = Quaternion.from_rotation_matrix(R)
# print(f'{quat.a} \n')
# print(f'{quat.b} \n')
# print(f'{quat.c} \n')
# print(f'{quat.d} \n')

