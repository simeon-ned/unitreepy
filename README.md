<!-- TODO: Write the readme -->
<!-- ADD THE PICTURE -->

# UnitreePy

UnitreePy is a lightweight python package that facilitate low and high level control of [unitree](https://www.unitree.com/) quadruped robots.
The package provide minimal easy to use interface to unitree legged SDK as well as several technical features,
such as forward kinematics, setting down motion and etc.

The project consist of following parts:

- [The Interface](#the-interface): The interface to C++ legged sdk library to send both high and low level commands and recive espective replies. This is done by modifying pybindings from the [motion imitation project](https://github.com/google-research/motion_imitation/tree/master/third_party/unitree_legged_sdk)
- [The Parsers](#the-parsers): Are used to parse the robots and wireless remote states to intuitive python structures
  - [High Level Parser](#high-level-parser): parse the *high* states
  - [Low Level Parser](#low-level-parser): parse the *low* states  
  - [Remote Parser](#remote-parser) parse the commands from the wireless remote
- [The Robot Handler](#the-robot-handler): Provide the object that can be used to generate commands based on desired robot behavior i.e desired torques, positions in joints etc. Update the actual state of the robot and initialize the specific While being bind to the chosen interface will send and receive messages with predefined update rate.

### Installing the package

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

## The Basic Usage

### The Interface

You may use this package to interface directly with robot without any additional parsers.

#### The structure of commands and replies

The High Level Command is orginized as follows:
| Index | Name | Description |
| --- | --- | --- |
| COM[0] | Mode | 0 - idle, 1 - forced stand, 2 - walk continuously
| COM[1] | Forward Speed  | forward/backward speed: (-1,1) : (-0.7,1) (m/s)
| COM[2] | Side Speed   | left/right: (-1,1) :  (-0.4,0.4) (m/s)
| COM[3] | Rotation Speed   | clockwise/anticlockwise: (-1,1) : (-120,120) (deg/s)
| COM[4] | Body Height   | body height: (-1,1) : (0.3,0.45) (m)
| COM[5] | Foot Height   | foot height while walking : unavailable in this version of SDK
| COM[6] | Yaw   | desired yaw angle: (-1,1) : (-28,28) (deg)
| COM[7] | Pitch   | desired pitch angle: (-1,1) : (-20,20) (deg)
| COM[8] | Roll   | desired roll angle:  (-1,1) : (-20,20) (deg)
| COM[9] | RESERVED  | reserved bytes in command

For instance the following code will require the robot to track the pitch of 
20 degrees for 5 seconds and printout the result:
```python
from pyunitree.legged_sdk import HighLevelInterface
from numpy import zeros
from time import perf_counter

interface = HighLevelInterface()
command = zeros(10)
actual_time = 0
terminal_time = 5
while actual_time<terminal_time:
  command[7] = 1
  interface.send(command)
  state = interface.receive()
  print(state.imy.rpy[1])
```
you may find the more eloborated examples in the examples/interface/ folder.

### The Parsers

#### High Level Parser
<!-- ADD TABLE WITH MAPPING BETWEEN REPLIES AND ASSOCIATED PYTHON OBJECTS-->
#### Low Level Parser

#### Remote Parser

### The Robot Handler

#### Binding to hardware

#### Running the Robot in High Level Mode

#### Running the Robot in Low Level Mode
