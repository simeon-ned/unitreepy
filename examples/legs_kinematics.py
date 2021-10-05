from pyunitree.robots.a1 import robot
from pyunitree.robots.a1.constants import STAND_ANGLES, LEG_NAMES, LEGS_BASES, LEG_LINKS_LENGTH
from pyunitree.utils import leg_kinematics
import numpy as np

robot.start()
desired_angles = np.array(STAND_ANGLES)
robot.move_to(desired_angles)
t0 = robot.state.time

t = 0
while t < 5:
    t = robot.state.time - t0
    desired_angles = np.array(STAND_ANGLES)*(1 + 0.2 * np.sin(4*t))
    robot.set_angles(desired_angles)

    angles = robot.state.joint_angles
    speeds = robot.state.joint_speed

    for leg_id, leg_name in enumerate(LEG_NAMES):
        leg_joint_angles = angles[3*leg_id: 3*(leg_id+1)]
        leg_joint_speeds = speeds[3*leg_id: 3*(leg_id+1)]
        leg_lengths = LEG_LINKS_LENGTH[leg_name]
        leg_base = LEGS_BASES[leg_name]

        leg_pos, leg_jacobian, _ = leg_kinematics(motor_angles=leg_joint_angles,
                                                  link_lengths=leg_lengths,
                                                  base_position=leg_base)
        leg_vel = leg_jacobian @ np.array(leg_joint_speeds)

        print(f'LEG {leg_name}: RELATIVE POS [mm]: {np.round(1000*leg_pos)}',
              f' RELATIVE VEL [mm/s]: {np.round(1000*leg_vel)}',
              end=10*" " + "\n", flush=True)

    print(4*'\033[A', end="\r", flush=True)
print(3*'\n')


# /////////////////////////////////////////////////

robot.move_to_init()
robot.stop()
