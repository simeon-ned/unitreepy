from ...base._handler import RobotHandler
from ...legged_sdk import LowLevelInterface
from .._build_robot import _build_robot
from .constants import POSITION_GAINS, DAMPING_GAINS, INIT_ANGLES
from types import SimpleNamespace


# TODO:
# ADD HIGH LEVEL HANDLER AND INTERFACE


# TODO: MOVE THIS TO CONSTANTS
CONSTANTS = SimpleNamespace()

CONSTANTS.POSITION_GAINS = POSITION_GAINS
CONSTANTS.DAMPING_GAINS = DAMPING_GAINS
CONSTANTS.INIT_ANGLES = INIT_ANGLES

# CREATE THE ROBOT 
interface = LowLevelInterface()
handler = RobotHandler(constants = CONSTANTS)
transmitter = interface.send
receiver = interface.receive

robot = _build_robot(handler, transmitter, receiver)
