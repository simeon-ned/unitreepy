<!-- TODO: Write the readme -->
<!-- ADD THE PICTURE -->
<!-- TODO:ADD THE STRUCTURE OF REPOSITORY -->
# UnitreePy

UnitreePy is a lightweight python package that facilitate low and high level control of [unitree](https://www.unitree.com/) quadruped robots.
The package provide minimal easy to use interface to unitree legged SDK as well as several technical features,
such as forward kinematics, setting down motion and etc.

The project consist of following parts:

- [The Legged SDK Interface](#the-legged-sdk-interface): The interface to C++ legged sdk library to send both high and low level commands and receive respective replies. This is done by modifying pybindings from the [motion imitation project](https://github.com/google-research/motion_imitation/tree/master/third_party/unitree_legged_sdk)
- [The Parsers](#the-parsers): Are used to parse the robots and wireless remote states to intuitive python structures
  - [High Level Parser](#high-level-parser): parse the ***high*** states
  - [Low Level Parser](#low-level-parser): parse the *low* **states**  
  - [Remote Parser](#remote-parser) parse the commands from the wireless remote
- [The Robot Handler](#the-robot-handler): Provide the object that can be used to generate commands based on desired robot behavior i.e desired torques, positions in joints etc. Update the actual state of the robot and initialize the specific While being bind to the chosen interface will send and receive messages with predefined update rate.

## Installing the package

First you need to build the python interface to unitree legged sdk from [unitreepy/unitree_legged_sdk/](https://github.com/SimkaNed/unitreepy/tree/main/unitree_legged_sdk)

```bash
mkdir build
cd build
cmake ../
make
```

To do so the following dependencies should be met:

- [Boost](http://www.boost.org) (version 1.5.4 or higher)
- [CMake](http://www.cmake.org) (version 2.8.3 or higher)
- [LCM](https://lcm-proj.github.io) (version 1.4.0 or higher)

Then copy the resulting *.so* file to the root of repository and install the package with

```sh
sudo python3 setup.py develop
```

<!-- ## The Basic Usage -->

## The Legged SDK Interface

You may use this package to interface directly with robot without any additional parsers.

### High Level Commands

The following will send the zero high level command to the robot (robot will hold the position):


```python
from pyunitree.legged_sdk import HighLevelInterface

high_interface = HighLevelInterface()
high_command = 10*[0]

high_interface.send(high_command)
high_state = high_interface.receive()
```

The **High Level Command** is organized as follows:
| Index  | Name           | Description                                                    |
| ------ | -------------- | -------------------------------------------------------------- |
| COM[0] | Mode           | 0 - idle, 1 - forced stand, 2 - walk continuously              |
| COM[1] | Forward Speed  | forward/backward speed: (-1,1) : (-0.7,1) (m/s)                |
| COM[2] | Side Speed     | left/right: (-1,1) :  (-0.4,0.4) (m/s)                         |
| COM[3] | Rotation Speed | clockwise/anticlockwise: (-1,1) : (-120,120) (deg/s)           |
| COM[4] | Body Height    | body height: (-1,1) : (0.3,0.45) (m)                           |
| COM[5] | Foot Height    | foot height while walking : unavailable in this version of SDK |
| COM[6] | Yaw            | desired yaw angle: (-1,1) : (-28,28) (deg)                     |
| COM[7] | Pitch          | desired pitch angle: (-1,1) : (-20,20) (deg)                   |
| COM[8] | Roll           | desired roll angle:  (-1,1) : (-20,20) (deg)                   |
| COM[9] | RESERVED       | reserved bytes in command                                      |


### Low Level Commands
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

The **Low Level Command** is organized as array of 60 floats:
| Index                 | Name          | Description                                     |
| --------------------- | ------------- | ----------------------------------------------- |
| COM[MOTOR_ID * 5]     | Position      | Desired position for 'MOTOR ID' (rad)           |
| COM[MOTOR_ID * 5 + 1] | Position Gain | Desired 'stiffness' gain for 'MOTOR ID' (N/rad) |
| COM[MOTOR_ID * 5 + 2] | Speed         | Desired speed for 'MOTOR ID' (rad/s)            |
| COM[MOTOR_ID * 5 + 3] | Speed Gain    | Desired damping gain of 'MOTOR ID' (Ns/rad)     |
| COM[MOTOR_ID * 5 + 4] | Torque        | Desired feed forward torque of  (N)             |

The motors are labeled accordingly to following table:


|       | Front Right | Front Left | Rear Right | Rear Left |
| :---: | :---------: | :--------: | :--------: | :-------: |
|  Hip  |      0      |     3      |     6      |     9     |
| Thigh |      1      |     4      |     7      |    10     |
| Knee  |      2      |     5      |     8      |    11     |


you may find the more elaborated examples in the *examples/legged_sdk/* directory.
<!-- 
### The Parsers

#### High Level Parser

#### Low Level Parser

#### Remote Parser

### The Robot Handler

#### Binding to hardware

#### Running the Robot in High Level Mode

#### Running the Robot in Low Level Mode -->
