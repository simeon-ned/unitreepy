from pyunitree.legged_sdk import LowLevelInterface
from pyunitree.parsers.remote import WirelessRemote
from numpy import zeros
from time import perf_counter

interface = LowLevelInterface()
command = zeros(60)

remote = WirelessRemote()

while True:
    # Send the zero command
    interface.send(command)
    # get the lowState reply in legged_sdk format 
    low_state = interface.receive()

    # parse the wireless remote state 
    remote.set_state(low_state.wirelessRemote)
    remote.update_state()

    print(f'\n{15*"/"} WIRELESS REMOTE STATE {15*"/"}')
    print(f' BUTTONS:\n A {remote.button.A} B {remote.button.B} X {remote.button.X} Y {remote.button.Y}',
          f'\n  Right {remote.button.right} Left {remote.button.left} Up {remote.button.up} Down {remote.button.down}',
          f'\n  R1 {remote.button.R1} R2 {remote.button.R2} L1 {remote.button.L1} L2 {remote.button.L2}',
          f'\n  Start {remote.button.start} Select {remote.button.select} F1 {remote.button.F1} F2 {remote.button.F2}',
          f'\n JOYSTICKS:\n LEFT: X {round(remote.left_joystick[0],2)} Y {round(remote.left_joystick[1],2)}',
          f'\n  RIGHT: X {round(remote.right_joystick[0],2)}  Y {round(remote.right_joystick[1],2)}',
          end=10*" " + "\n", flush=True)
    print(f'{52*"/"}\n')
    print(12*'\033[A', end="\r", flush=True)
