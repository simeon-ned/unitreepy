from lib._parsers._low_level import A1LowLevelParser
from lib._constants import POSITION_GAINS, DAMPING_GAINS, STAND_ANGLES, INIT_ANGLES
from legged_sdk import LowLevelInterface
from time import perf_counter
from numpy import array
from lib._utils import p2p_cos_profile

robot_parser = A1LowLevelParser()
interface = LowLevelInterface()

initial_angles = array(INIT_ANGLES)
stand_angles = array(STAND_ANGLES)
position_gains = POSITION_GAINS
damping_gains = DAMPING_GAINS

t0 = perf_counter()


for i in range(100):
    command = robot_parser.build_command()
    interface.send(command)
    low_state = interface.receive()
    robot_parser.parse_state(low_state)
    q_start = robot_parser.joint_angles
    initial_angles = array(q_start)

while True:
    t = perf_counter() - t0

    q_des, dq_des = p2p_cos_profile(t,
                                    array(initial_angles),
                                    array(STAND_ANGLES),
                                    terminal_time=1)

    desired_angles = q_des
    desired_speeds = dq_des

    command = robot_parser.build_command(desired_pos=desired_angles,
                                         desired_vel=desired_speeds,
                                         position_gains=position_gains,
                                         damping_gains=damping_gains)

    # command = robot_parser.build_command()

    interface.send(command)
    low_state = interface.receive()
    robot_parser.parse_state(low_state)
    # print(initial_angles)

    print(f'On Board Time [ms]: {robot_parser.tick}',
          end=5*" " + "\n", flush=True)
    print('\033[A', end="\r", flush=True)
