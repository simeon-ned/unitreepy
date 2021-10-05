from pyunitree._parsers.gazeboMsgParser import GazeboMsgParser
from unitree_legged_msgs.msg import MotorState,LowState,MotorCmd
from sensor_msgs.msg import Imu
from geometry_msgs.msg import WrenchStamped

import rospy
import time

class GazeboInterface:
    controllerNames =  [
                        "/a1_gazebo/FR_hip_controller",
                        "/a1_gazebo/FR_thigh_controller",
                        "/a1_gazebo/FR_calf_controller",
                        "/a1_gazebo/FL_hip_controller",
                        "/a1_gazebo/FL_thigh_controller",
                        "/a1_gazebo/FL_calf_controller",
                        "/a1_gazebo/RR_hip_controller",
                        "/a1_gazebo/RR_thigh_controller",
                        "/a1_gazebo/RR_calf_controller",
                        "/a1_gazebo/RL_hip_controller",
                        "/a1_gazebo/RL_thigh_controller",
                        "/a1_gazebo/RL_calf_controller"
                        ]

    footContactNames = [ 
                        "/visual/FR_foot_contact/the_force",
                        "/visual/FL_foot_contact/the_force",
                        "/visual/RR_foot_contact/the_force",
                        "/visual/RL_foot_contact/the_force"
                        ]

    def __init__(self):
        self.np = rospy.init_node('unitreepy_node', anonymous=True)
        self.parser = GazeboMsgParser()
        self.lowState = LowState()
        self.imuRoll = 0
        self.imuPitch = 0

        self.imuSub = rospy.Subscriber("/trunk_imu", Imu, self.imuCallback)
        self.imuOrientationSub = rospy.Subscriber("/trunk_imu", Imu, self.imuOrientationCallback)

        self.footForceSubs = [rospy.Subscriber(name, WrenchStamped,lambda msg: self.FootCallback(idx,msg)) 
                                                            for idx,name in enumerate(GazeboInterface.footContactNames)]

        self.servoSubs = [rospy.Subscriber(controllerName+"/state", MotorState, lambda msg: self.motorStateCallback(idx,msg)) 
                                                            for idx,controllerName in enumerate(GazeboInterface.controllerNames)]


        self.servoPublishers = [rospy.Publisher(controllerName+"/command", MotorCmd) 
                                                            for idx,controllerName in enumerate(GazeboInterface.controllerNames)]

        time.sleep(2) #needs time to connect

    def imuCallback(self,msg):
        self.lowState.imu = self.parser.parseImuMsg(msg)

    def imuOrientationCallback(self,msg):
        self.imuRoll,self.imuPitch = self.parser.parseImuOrientation(msg)

    def motorStateCallback(self,motorIdx,msg):
        self.lowState.motorState[motorIdx] = self.parser.parseMotorState(msg)

    def FootCallback(self,footIdx,msg):
        self.lowState.eeForce[footIdx] = self.parser.parseEeForce(msg)
        self.lowState.footForce[footIdx] = self.parser.parseFootForce(msg)
        
    def send(self,cmd):

        for motorId in range(12):
            motorCmd = MotorCmd()
            motorCmd.mode = 0x0A
            motorCmd.q=cmd[motorId * 5]
            motorCmd.Kp=cmd[motorId * 5+1]
            motorCmd.dq=cmd[motorId * 5+2]
            motorCmd.Kd=cmd[motorId * 5+3]
            motorCmd.tau=cmd[motorId * 5+4]
            self.servoPublishers[motorId].publish(motorCmd)
            
    def receive(self):
        return self.lowState