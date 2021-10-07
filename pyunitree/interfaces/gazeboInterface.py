from pyunitree.gazebo.gazeboMsgParser import GazeboMsgParser

import rospy
from unitree_legged_msgs.msg import LowState,MotorCmd
from sensor_msgs.msg import Imu,JointState
from geometry_msgs.msg import WrenchStamped

from multiprocessing import Process, Manager
from logging import info
import time

from scipy.spatial.transform import Rotation as R

class GazeboInterface:
    controllerNames  =  [
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

    #Joint names from JointState message
    motorNames       = [
                        "FR_hip_joint",
                        "FR_thigh_joint",
                        "FR_calf_joint",
                        "FL_hip_joint",
                        "FL_thigh_joint",
                        "FL_calf_joint",
                        "RR_hip_joint",
                        "RR_thigh_joint",
                        "RR_calf_joint",
                        "RL_hip_joint",
                        "RL_thigh_joint",
                        "RL_calf_joint"
                        ]

    #Maps joint name to it's location in position and velocity idx in joint state
    motorMappings = {name:i for i,name in enumerate(motorNames)}

    def __init__(self,update_rate):
        self.parser = GazeboMsgParser()
        self.lastState = LowState()
        self.update_rate = update_rate

        self.jointNames = None
        self.position = [0]*12
        self.velocity = [0]*12
        self.footForces = [[0]*3]*4
        self.imu = [0]*10

        self.__shared = Manager().Namespace()
        self.__shared.position = [0]*12
        self.__shared.velocity = [0]*12
        self.__shared.footForces = [[0]*3]*4
        self.__shared.imu = [0]*10
        self.__shared.jointNames = None
        
        self.__shared.handlerIsWorking = False

        self.__shared.cmd = [0]*60

        self.handlerProc = Process(target=self.__handler)
        self.handlerProc.start()

        while not self.__shared.handlerIsWorking:
            time.sleep(0.01)
    
    def __del__(self):
        self.stop()
        
    def stop(self):
        self.handlerProc.terminate()
        
    def __handler(self):
        try:
            self.node = rospy.init_node('unitreepy_node', anonymous=True)
        
            self.imuSub = rospy.Subscriber("/trunk_imu", Imu, self.imuVectorCallback)

            self.footForceSubs = [rospy.Subscriber(name, WrenchStamped,lambda msg: self.footForceVectorCallback(idx,msg)) 
                                                                for idx,name in enumerate(GazeboInterface.footContactNames)]

            self.servoSubs = rospy.Subscriber("/a1_gazebo/joint_states", JointState, self.jointStatesVectorCallback) 
            
            self.servoPublishers = [rospy.Publisher(controllerName+"/command", MotorCmd) 
                                                                for controllerName in GazeboInterface.controllerNames]


            info("Unitreepy Gazebo listener: Attempting to receive initial position from Gazebo")
            while self.jointNames==None:
                time.sleep(0.001)
            info("Unitreepy Gazebo listener: Initial state received")
            
            self.__shared.handlerIsWorking = True

            initial_time = time.perf_counter()
            last_tick = 0
            while True:
                actual_time = time.perf_counter() - initial_time
                try:
                    command = self.__shared.cmd
                except BrokenPipeError:
                    break

                if actual_time - last_tick >= 1/self.update_rate:
                    self.moveStateToShared()
                    self.sendCommand(command)
                    last_tick = actual_time

        except KeyboardInterrupt:
            print('Exit')
    

    def sendCommand(self,command):
        motorCmd = MotorCmd()
        for motorId in range(12):
            motorCmd.mode = 0x0A
            motorCmd.q=command[motorId * 5]
            motorCmd.Kp=command[motorId * 5+1]
            motorCmd.dq=command[motorId * 5+2]
            motorCmd.Kd=command[motorId * 5+3]
            motorCmd.tau=command[motorId * 5+4]
            self.servoPublishers[motorId].publish(motorCmd)

    def moveStateToShared(self):
        self.__shared.imu = self.imu
        self.__shared.footForces = self.footForces
        self.__shared.position = self.position
        self.__shared.velocity = self.velocity
        self.__shared.jointNames = self.jointNames

    def imuVectorCallback(self,msg):
        self.imu = self.parser.vectorizeImuMsg(msg)

    def footForceVectorCallback(self,legIdx,msg):
        self.footForces[legIdx] = self.parser.vectorizeEeForce(msg)

    def jointStatesVectorCallback(self,msg):
        self.position = msg.position
        self.velocity = msg.velocity
        self.jointNames = msg.name

    def send(self,cmd):
        self.__shared.cmd = cmd

    def receive(self):
        try:
            lowState = LowState()
            lowState = self.buildLowState()
        except:
            raise RuntimeError("Unitreepy Gazebo listener: Failed to build current state of the robot")

        self.lastState = lowState
        return lowState

    def buildLowState(self):
        lowState = LowState()

        position = self.__shared.position
        velocity = self.__shared.velocity
        jointNames = self.__shared.jointNames

        for i in range(4):
            jointIdx1 = GazeboInterface.motorMappings[jointNames[3*i]]
            jointIdx2 = GazeboInterface.motorMappings[jointNames[3*i+1]]
            jointIdx3 = GazeboInterface.motorMappings[jointNames[3*i+2]]

            lowState.motorState[jointIdx1].q = position[3*i]
            lowState.motorState[jointIdx2].q = position[3*i+1]
            lowState.motorState[jointIdx3].q = position[3*i+2]

            lowState.motorState[jointIdx1].dq = velocity[3*i]
            lowState.motorState[jointIdx2].dq = velocity[3*i+1]
            lowState.motorState[jointIdx3].dq = velocity[3*i+2]

        imu = self.__shared.imu
        lowState.imu = self.parser.parseImuVector(imu)

        footForces = self.__shared.footForces

        for i in range(4):
            lowState.eeForce[i],lowState.footForce[i] = self.parser.parseEeForceVector(footForces[i])
        
        return lowState

    def getPitchRoll(self):
        orientation = self.__shared.imu[:4]
        r = R.from_quat(orientation)
        rpy_angles = r.as_euler("xyz")
        return rpy_angles[1],rpy_angles[2]