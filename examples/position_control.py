from pyunitree.robots import robot
from pyunitree._constants import STAND_ANGLES
from numpy import array, sin

# start robot process and move to initial position
robot.start()

desired_angles = array(STAND_ANGLES)
robot.move_to(desired_angles)
initial_time = robot.state.time

time = 0
while time < 5:
    t = robot.state.time - initial_time
    desired_angles = array(STAND_ANGLES)*(1 + 0.25 * sin(3*t))
    
    robot.set_angles(desired_angles)

robot.move_to_init()
robot.stop()




