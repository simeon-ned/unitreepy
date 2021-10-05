from pyunitree.controllers.positionController.RobotController import RobotController
import pyunitree.controllers.positionController.robotIK as robotIK

class PositionController:

    def __init__(self,update_rate, stateHandler):

            body = [0.366, 0.094]   
            legs = [0.,0.08505, 0.2, 0.2] 

            self.robotController = RobotController.Robot(body, legs, True, 1/update_rate, stateHandler)
            self.inverseKinematics = robotIK.InverseKinematics(body, legs)
            self.linearSpeed = [0,0]
            self.angularSpeed = 0
            self.useImu = False

    def setDesiredSpeed(self,linSpeed = 0,angSpeed = 0, useImu = False):
        self.linearSpeed = linSpeed
        self.angularSpeed = angSpeed
        self.useImu = useImu

    def transformCommandToControllerInput(self):
        """ Simulates controller input from linear and angular speeds """
        inputVec = [0,0,1,0,0,1,0,0]
        buttons = [False]*8

        inputVec[4] = self.linearSpeed[0]
        inputVec[3] = self.linearSpeed[1]
        inputVec[0] = self.angularSpeed

        if self.useImu == True:
          buttons[7]=True
        if self.robotController.trotGaitController.use_imu == True and self.useImu==True:
            buttons[7]=False
        if self.robotController.trotGaitController.use_imu == True and self.useImu==False:
            buttons[7]=True
        return inputVec,buttons

    def getPositionCommand(self):
        inputVec,buttons = self.transformCommandToControllerInput()
        self.robotController.set_movement("trot",inputVec,buttons)
        
        self.leg_positions = self.robotController.run()
        self.robotController.change_controller()

        dx = self.robotController.state.body_local_position[0]
        dy = self.robotController.state.body_local_position[1]
        dz = self.robotController.state.body_local_position[2]
        
        roll = self.robotController.state.body_local_orientation[0]
        pitch = self.robotController.state.body_local_orientation[1]
        yaw = self.robotController.state.body_local_orientation[2]

        try:
            joint_angles = self.inverseKinematics.inverse_kinematics(self.leg_positions,
                                dx, dy, dz, roll, pitch, yaw)
            command = joint_angles
        except:
            print("POSITION FAIL")
            command = None

        return command
