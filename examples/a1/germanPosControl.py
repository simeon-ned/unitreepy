from pyunitree.robots import build_robot
from pyunitree._handler import RobotHandler
from pyunitree.interfaces.gazeboInterface import GazeboInterface
from pyunitree._constants import STAND_ANGLES
from pyunitree.controllers.positionController.positionController import PositionController
import numpy as np
import time 
import matplotlib.pyplot as plt

UPDATE_RATE = 300
robotHandler = RobotHandler(update_rate=UPDATE_RATE)
commsInterface = GazeboInterface()

robot = build_robot(robotHandler,commsInterface.send, commsInterface.receive)

posController = PositionController(robot.update_rate, commsInterface)
robot.start()

desired_angles = np.array(STAND_ANGLES)
robot.move_to(desired_angles)
initial_time = robot.state.time

currentTime = 0
angles = []
while robot.state.time - initial_time < 5:
    t = robot.state.time - initial_time
    desired_angles = posController.getPositionCommand()
    desired_angles = np.array(STAND_ANGLES)*(1 + 0.25 * np.sin(3*t))
    angles.append(desired_angles)
    robot.set_angles(desired_angles)
    time.sleep(1/UPDATE_RATE)

robot.move_to_init()
robot.stop()

plt.plot(angles)
plt.show()