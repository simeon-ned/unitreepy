from numpy import zeros, float32
from _constants import NUM_MOTORS, NUM_LEGS

HIGH_SIZE = 10

# ///////////////////////////////
# HIGH LEVEL SEND PACKET STRUCTURE
# ///////////////////////////////
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


# ///////////////////////////////////
# HIGH LEVEL RECEIVE PACKET STRUCTURE
# ///////////////////////////////////


class HighLevelParser():
    ''''''
    def __init__(self):
     #  // High Level states and commands //
        self._zero_command = zeros(HIGH_SIZE, dtype=float32)
        self._command = self._high_zero_command
