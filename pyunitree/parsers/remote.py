import ctypes
from struct import unpack

c_uint8 = ctypes.c_uint8
c_uint16 = ctypes.c_uint16

class Buttons_bits(ctypes.LittleEndianStructure):
    _fields_ = [
        ("R1", c_uint8, 1),
        ("L1", c_uint8, 1),
        ("start", c_uint8, 1),
        ("select", c_uint8, 1),
        ("R2", c_uint8, 1),
        ("L2", c_uint8, 1),
        ("F1", c_uint8, 1),
        ("F2", c_uint8, 1),
        ("A", c_uint8, 1),
        ("B", c_uint8, 1),
        ("X", c_uint8, 1),
        ("Y", c_uint8, 1),
        ("up", c_uint8, 1),
        ("right", c_uint8, 1),
        ("down", c_uint8, 1),
        ("left", c_uint8, 1),
    ]

class WirelessRemote(ctypes.Union):
    _fields_ = [("button", Buttons_bits),
                ("value", c_uint16)]

    def __init__(self):
        ctypes.Union.__init__(self)
        self.left_joystick = [0, 0]
        self.right_joystick = [0, 0]
        self.value = 0 
        self.__state = 40*[0]

    def set_state(self, remote_state):
        self.__state = remote_state

    def update_state(self):
        buttons = self.__state[2:4]
        self.value = int.from_bytes(
            bytes(buttons), byteorder='little', signed=False)

        joysticks = unpack('5f', bytes(self.__state[4: 4 + 4*5]))
        self.left_joystick = joysticks[0], joysticks[4]
        self.right_joystick = joysticks[1], joysticks[2]

