# The Legged SDK Interface

You may use this package to interface directly with robot without any additional parsers by invoking `pyunitree.legged_sdk`, this may be done in both high and low levels.

## High Level 

### High Level Command

The following will send the zero high level command to the robot (robot will hold the position):


```python
from pyunitree.legged_sdk import HighLevelInterface

high_interface = HighLevelInterface()
high_command = 10*[0]

high_interface.send(high_command)
high_state = high_interface.receive()
```

The **High Level Command** is organized as follows:
| Index    | Name           | Description                                                    |
| -------- | -------------- | -------------------------------------------------------------- |
| `COM[0]` | Mode           | 0 - idle, 1 - forced stand, 2 - walk continuously              |
| `COM[1]` | Forward Speed  | forward/backward speed: (-1,1) : (-0.7,1) (m/s)                |
| `COM[2]` | Side Speed     | left/right: (-1,1) :  (-0.4,0.4) (m/s)                         |
| `COM[3]` | Rotation Speed | clockwise/anticlockwise: (-1,1) : (-120,120) (deg/s)           |
| `COM[4]` | Body Height    | body height: (-1,1) : (0.3,0.45) (m)                           |
| `COM[5]` | Foot Height    | foot height while walking : unavailable in this version of SDK |
| `COM[6]` | Yaw            | desired yaw angle: (-1,1) : (-28,28) (deg)                     |
| `COM[7]` | Pitch          | desired pitch angle: (-1,1) : (-20,20) (deg)                   |
| `COM[8]` | Roll           | desired roll angle:  (-1,1) : (-20,20) (deg)                   |
| `COM[9]` | RESERVED       | reserved bytes in command                                      |

### High Level State

The robot reply with the following state:

| State                     | Name              | Description                                                                           |
| ------------------------- | ----------------- | ------------------------------------------------------------------------------------- |
| `state.imu.quaternion`    | orientation       | quaternion, normalized, [w,x,y,z]                                                     |
| `state.imu.rpy`           | orientation       | euler angles, [roll, pitch, yaw] (rad)                                                |
| `state.imu.gyroscope`     | angular velocity  | angular velocity with respect to base frame, [w_x, w_y, w_z]（rad/s)                  |
| `state.imu.accelerometer` | acceleration      | linear acceleration with respect to base frame, [a_x, a_y, a_z] (m/s2)                |
| `state.forwardSpeed`      | forward speed     | the estimates of the robot speed in x direction, (m/s)                                |
| `state.sideSpeed`         | side speed        | the estimates of the robot speed in y direction, (m/s)                                |
| `state.updownSpeed`       | vertical speed    | the estimates of the robot speed in z direction, (m/s)                                |
| `state.rotateSpeed`       | rotation speed    | the estimates of angular speed around z direction, (rad/s)                            |
| `state.forwardPosition`   | forward position  | the estimates of the robot position in x direction, (m)                               |
| `state.sidePosition`      | side position     | the estimates of the robot position in y direction, (m)                               |
| `state.bodyHeight`        | vertical position | the estimates of the robot position in z direction, (m)                               |
| `state.footPosition2Body` | foot position     | the cartesian positions of each foot with respect to body frame, [p_x, p_y, p_z] (m)  |
| `state.footSpeed2Body`    | foot velocity     | the cartesian velocity of each foot with respect to body frame, [v_x, v_y, v_z] (m/s) |
| `state.footForce`         | foot contact      | The raw data of contact sensor                                                        |
| `state.footForceEst`      | estimated contact | Filtered data from contact sensor                                                     |
| `state.tick`              | ticker            | controller ticker in (ms)                                                             |
| `state.wirelessRemote`    | wireless remote   | the state of wireless remote                                                          |

```python
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
```

## Low Level 

### Low Level Command
The following will send the zero command in low level mode: 
```python
from pyunitree.legged_sdk import LowLevelInterface

message = "PAY ATTENTION: ZERO TORQUES WILL BE SENT. TO PREVENT ROBOT FROM FALLING USE THE RACK"
input(message + 'Press Enter to continue...')

low_interface = HighLevelInterface()
low_command = 60*[0]

low_interface.send(low_command)
low_state = low_interface.receive()
```

The **Low Level Command** is organized as array of 60 floats (5 commands for each for 12 motors):
| Index                   | Name          | Description                                     |
| ----------------------- | ------------- | ----------------------------------------------- |
| `COM[MOTOR_ID * 5]`     | Position      | Desired position for `MOTOR_ID` (rad)           |
| `COM[MOTOR_ID * 5 + 1]` | Position Gain | Desired 'stiffness' gain for `MOTOR_ID` (N/rad) |
| `COM[MOTOR_ID * 5 + 2]` | Speed         | Desired speed for `MOTOR_ID` (rad/s)            |
| `COM[MOTOR_ID * 5 + 3]` | Speed Gain    | Desired damping gain of `MOTOR_ID` (Ns/rad)     |
| `COM[MOTOR_ID * 5 + 4]` | Torque        | Desired feed forward torque of  (N)             |

The motor labels are associated with legs and joints accordingly to following table:

|       | Front Right | Front Left | Rear Right | Rear Left |
| :---: | :---------: | :--------: | :--------: | :-------: |
|  Hip  |      0      |     3      |     6      |     9     |
| Thigh |      1      |     4      |     7      |    10     |
| Knee  |      2      |     5      |     8      |    11     |

### Low Level States

## Examples
To find some examples, including high level and low level control please follow the **examples/legged_sdk/** directory.
