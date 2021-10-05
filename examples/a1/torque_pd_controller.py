from pyunitree.robots.a1 import robot
from pyunitree.robots.a1.constants import STAND_ANGLES, NUM_MOTORS
from numpy import array, sin, cos, zeros, ones

# start robot process and move to initial position

robot.start()

desired_angles = array(STAND_ANGLES)
torques = zeros(NUM_MOTORS)

amplitude = 0.25
frequency = 2

robot.move_to(desired_angles)


initial_time = robot.state.time
time = 0

position_gains = 60 * ones(NUM_MOTORS)
damping_gains = 0.6 * ones(NUM_MOTORS)

while time < 10:
    time = robot.state.time - initial_time

    desired_angles = array(STAND_ANGLES)*(1 + amplitude * sin(frequency*time))
    desired_speeds = array(STAND_ANGLES)*amplitude * \
        frequency * cos(frequency*time)

    angles = robot.state.joint_angles
    sppeds = robot.state.joint_speed

    pos_error = desired_angles - angles
    speed_error = desired_speeds - sppeds

    for motor_id in range(NUM_MOTORS):
        torques[motor_id] = position_gains[motor_id] * pos_error[motor_id] +\
            damping_gains[motor_id] * speed_error[motor_id]

    robot.set_torques(torques)

robot.move_to_init()
robot.stop()
