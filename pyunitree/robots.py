from ._handler import RobotHandler
from .legged_sdk import LowLevelInterface



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
