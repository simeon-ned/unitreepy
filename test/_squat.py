from lib._parsers._low_level import A1LowLevelParser
from lib._constants import POSITION_GAINS, DAMPING_GAINS, STAND_ANGLES
from legged_sdk import LowLevelInterface
from time import perf_counter
from numpy import sin, array

robot_parser = A1LowLevelParser()
interface = LowLevelInterface()

initial_angles = array(STAND_ANGLES)
position_gains = POSITION_GAINS
damping_gains = DAMPING_GAINS

t0 = perf_counter()

while True:
    t = perf_counter() - t0
    desired_angles = initial_angles*(1 + 0.15*sin(3*t))
    command = robot_parser.build_command(desired_pos=desired_angles,
                                         position_gains=position_gains,
                                         damping_gains=damping_gains)
    interface.send(command)
    low_state = interface.receive()
    robot_parser.parse_state(low_state)

    print(f'On Board Time [ms]: {robot_parser.tick}',
          end=5*" " + "\n", flush=True)
    print('\033[A', end="\r", flush=True)
