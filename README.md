<!-- TODO: Write the readme -->
<!-- ADD THE PICTURE -->

# UnitreePy

UnitreePy is a lightweight python package that facilitate low and high level control of [unitree](https://www.unitree.com/) quadruped robots.
The package provide minimal easy to use interface to unitree legged SDK as well as several technical features,
such as forward kinematics, setting down motion and etc.

The project consist of following parts:

- [The Interface](#the-interface): The interface to C++ legged sdk library to send both high and low level commands and recive espective replies. This is done by modifying pybindings from the [motion imitation project](https://github.com/google-research/motion_imitation/tree/master/third_party/unitree_legged_sdk)
- [The Parsers](#parsers): Are used to parse the robots and wireless remote states to intuitive python structures
  - [High Level Parser](#high_level_parser): parse the *high* states
  - [Low Level Parser](#hiuh_level_parser): parse the *low* states  
  - [Remote Parser](#low_level_parser) parse the commands from the wireless remote
- [The Robot Handler](#handler): Provide the object that can be used to generate commands based on desired robot behavior i.e desired torques, positions in joints etc. Update the actual state of the robot and initialize the specific While being bind to the chosen interface will send and receive messages with predefined update rate.

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

Sending the zero command in high level interface and printing the ticker:

```python
from pyunitree.legged_sdk import HighLevelInterface
import numpy as np
interface = HighLevelInterface()
command = np.zeros(10)
interface.send(command)
state = interface.receive()
print(state.tick)
```

#### The structure of commands and replies
<!-- ADD TABLE WITH MAPPING BETWEEN REPLIES AND COMMANDS -->

### The Parsers

#### High States
<!-- ADD TABLE WITH MAPPING BETWEEN REPLIES AND ASSOCIATED PYTHON OBJECTS-->
#### Low States

#### Wireless Remote

### The Robot Handler

#### Binding to hardware

#### Running the Robot in High Level Mode

#### Running the Robot in Low Level Mode
