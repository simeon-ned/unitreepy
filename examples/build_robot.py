from pyunitree._constants import STAND_ANGLES
from pyunitree._handler import RobotHandler
from pyunitree.legged_sdk import LowLevelInterface
from numpy import array


interface = LowLevelInterface()

# ////////// BUILDING ROBOT FROM HANDLER AND INTERFACE //////////////
handler = RobotHandler()
transmitter = interface.send
receiver = interface.receive

def build_robot(handler, transmitter, receiver):
    handler.set_transmitter(transmitter)
    handler.set_receiver(receiver)
    robot = handler
    return robot

robot = build_robot(handler, transmitter, receiver)

# start robot process and move to initial position
robot.start()
desired_angles = array(STAND_ANGLES)
robot.move_to(desired_angles)
robot.move_to_init()
robot.stop()
