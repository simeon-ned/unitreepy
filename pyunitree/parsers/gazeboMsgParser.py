from unitree_legged_msgs.msg import IMU,MotorState,Cartesian
from scipy.spatial.transform import Rotation as R

class GazeboMsgParser:
    def __init__(self):
        pass

    def parseImuMsg(self,msg):
        imu = IMU()
        imu.quaternion[0] = msg.orientation.w
        imu.quaternion[1] = msg.orientation.x
        imu.quaternion[2] = msg.orientation.y
        imu.quaternion[3] = msg.orientation.z

        imu.gyroscope[0] = msg.angular_velocity.x
        imu.gyroscope[1] = msg.angular_velocity.y
        imu.gyroscope[2] = msg.angular_velocity.z

        imu.accelerometer[0] = msg.linear_acceleration.x
        imu.accelerometer[1] = msg.linear_acceleration.y
        imu.accelerometer[2] = msg.linear_acceleration.z
        return imu

    def parseMotorState(self,msg):
        motorState = MotorState()

        motorState.mode = msg.mode
        motorState.q = msg.q
        motorState.dq = msg.dq
        motorState.tauEst = msg.tauEst
        motorState.temperature = msg.temperature

        return motorState

    def parseEeForce(self,msg):
        eeForce = Cartesian()
        eeForce.x = msg.wrench.force.x
        eeForce.y = msg.wrench.force.y
        eeForce.z = msg.wrench.force.z
        return eeForce
    
    def parseFootForce(self,msg):
        return msg.wrench.force.z
    
    def parseImuOrientation(self,msg):
        q = msg.orientation
        r = R.from_quat([q.x,q.y,q.z,q.w])
        rpy_angles = r.as_euler("xyz")

        return rpy_angles[0], rpy_angles[1]