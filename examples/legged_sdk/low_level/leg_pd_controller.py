from pyunitree.legged_sdk import HighLevelInterface
from numpy import zeros, rad2deg
from time import perf_counter

interface = HighLevelInterface()
command = zeros(10)

initial_time = perf_counter()
actual_time = 0
terminal_time = 5

while actual_time < terminal_time:
    actual_time = perf_counter() - initial_time
    command[7] = 1
    interface.send(command)
    state = interface.receive()
    print(rad2deg(state.imu.rpy[1]))
