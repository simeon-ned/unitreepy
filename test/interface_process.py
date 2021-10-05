from pyunitree.legged_sdk import HighLevelInterface
from pyunitree.__interface import Interface
import numpy as np
from time import perf_counter

# /////////////////////////////////
# The example of High Level Control 
# /////////////////////////////////

# High level send packet structure:

# mode          | COMMAND[0]    | 0:idle, default stand
#                                 1:forced stand
#                                 2:walk continuously
#
# Forward Speed | COMMAND[1]    | forward/backward, scale: -1~1 <-> -0.7~1 [m/s]
# Side Speed    | COMMAND[2]    | left/right, scale: -1~1 <-> -0.4~0.4 [m/s]
# Rotate Speed  | COMMAND[3]    | clockwise/anticlockwise, scale: -1~1 <-> -120~120 [deg/s]
# Body Height   | COMMAND[4]    | body height, scale: -1~1 <-> 0.3~0.45 [m]
# Foot Height   | COMMAND[5]    | foot up height while walking <-> !!!unavailable!!!
# Yaw           | COMMAND[6]    | desired yaw angle scale: -1~1 <-> -28~28 [deg]
# Pitch         | COMMAND[7]    | desired pitch angle scale: -1~1 <-> -20~20 [deg]
# Roll          | COMMAND[8]    | desired roll angle scale: -1~1 <-> -20~20 [deg]
# RESERVED      | COMMAND[9] | reserved bytes in command

interface = HighLevelInterface()


interface_process = Interface()
interface_process.bind_interface(interface.receive, interface.send)
interface_process.start()
initial_time = perf_counter()
time_sample = 0

command = np.zeros(10)

while True:

    time = (perf_counter() - initial_time)
    command[6] = 0.6*np.sin(time) # yaw
    command[7] = 0.6*np.sin(2*time) # pitch
    command[8] = 0.5*np.sin(time/2) # roll 
    interface_process.set_command(command)
    state = interface_process.state
    print(state)

