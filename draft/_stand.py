from lib._parsers._low_level import A1LowLevelParser
from lib._constants import POSITION_GAINS, DAMPING_GAINS, STAND_ANGLES
from legged_sdk import LowLevelInterface


robot_parser = A1LowLevelParser()
interface = LowLevelInterface()


desired_angles = STAND_ANGLES
position_gains = POSITION_GAINS
damping_gains = DAMPING_GAINS


while True:
    command = robot_parser.build_command(desired_pos=desired_angles,
                                         position_gains=position_gains,
                                         damping_gains=damping_gains)

    interface.send(command)
    low_state = interface.receive()
    robot_parser.parse_state(low_state)
    print(f'On Board Time [ms]: {robot_parser.tick}', end=5*" " + "\n", flush=True)
    print('\033[A', end="\r", flush=True)
