from legged_sdk import LowLevelInterface
from lib._parsers._low_level import A1LowLevelParser
from lib._constants import LEG_NAMES
from time import perf_counter, sleep
import numpy as np

interface = LowLevelInterface()

sleep(4)

robot_parser = A1LowLevelParser()
# interface = LowLevelInterface()


t0 = perf_counter()


while True:
    t = perf_counter() - t0

    command = robot_parser.build_command()

    interface.send(command)
    low_state = interface.receive()

    robot_parser.parse_state(low_state)

    p = robot_parser.foot_positions
    v = robot_parser.foot_velocity

    q = robot_parser.joint_angles

    for leg_id, leg_name in enumerate(LEG_NAMES):
        leg_pos = p[3*leg_id: 3*(leg_id+1)]
        leg_vel = v[3*leg_id: 3*(leg_id+1)]

    #     print(
    #         f'LEG {leg_name}: FOOT POS [mm]: {np.round(1000*leg_pos)} ', 
    #         f'FOOT VEL [mm/s]: {np.round(1000*leg_vel)} ',
    #         end=10*" " + "\n", flush=True)
    # print(4*'\033[A', end="\r", flush=True)

        print(
        f'LEG {leg_name}: FOOT POS [mm]: {q} ', 
        f'FOOT VEL [mm/s]: {np.round(1000*leg_vel)} ',
        end=10*" " + "\n", flush=True)
    print(4*'\033[A', end="\r", flush=True)



