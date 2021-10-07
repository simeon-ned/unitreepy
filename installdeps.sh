#!/bin/bash

sudo apt install liblcm-dev
git clone https://github.com/RumblingTurtle/unitree_legged_sdk.git
cd ./unitree_legged_sdk/
sudo python3 setup.py install
cd ..