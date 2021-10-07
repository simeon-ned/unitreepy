
from unitree_legged_msgs.msg import IMU,Cartesian
from scipy.spatial.transform import Rotation as R

class GazeboMsgParser:
    '''
        Class to parse and vectorize unitree messages
    '''
    def __init__(self):
        pass
    
    def vectorizeImuMsg(self,msg):
        vector = [0]*10

        vector[0] = msg.orientation.w
        vector[1] = msg.orientation.x
        vector[2] = msg.orientation.y
        vector[3] = msg.orientation.z

        vector[4] = msg.angular_velocity.x
        vector[5] = msg.angular_velocity.y
        vector[6] = msg.angular_velocity.z

        vector[7] = msg.linear_acceleration.x
        vector[8] = msg.linear_acceleration.y
        vector[9] = msg.linear_acceleration.z

        return vector

    def vectorizeEeForce(self,msg):
        vector = [0]*3
        vector[0] = msg.wrench.force.x
        vector[1] = msg.wrench.force.y
        vector[2] = msg.wrench.force.z
        return vector

    def parseImuVector(self,vector):
        imu = IMU()
        imu.quaternion[0] = vector[0]
        imu.quaternion[1] = vector[1]
        imu.quaternion[2] = vector[2]
        imu.quaternion[3] = vector[3]

        imu.gyroscope[0] = vector[4]
        imu.gyroscope[1] = vector[5]
        imu.gyroscope[2] = vector[6]

        imu.accelerometer[0] = vector[7]
        imu.accelerometer[1] = vector[8]
        imu.accelerometer[2] = vector[9]
        return imu

    def parseEeForceVector(self,vector):
        eeForce = Cartesian()
        eeForce.x = vector[0]
        eeForce.y = vector[1]
        eeForce.z = vector[2]
        return eeForce , vector[2]  #Foot force is taken as it's z component