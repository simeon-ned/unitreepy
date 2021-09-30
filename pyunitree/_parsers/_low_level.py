from numpy import array
from .._utils import leg_kinematics
from numpy import zeros, float32
from .._constants import NUM_MOTORS, NUM_LEGS, LEG_NAMES, LEGS_BASES, LEG_LINKS_LENGTH


# TODO: Add parsing

# ///////////////////////////////
# LEGGED SDK LOW LEVEL SEND PACKET STRUCTURE
# ///////////////////////////////
# Low level send packet is the array of 60 floats according to joint mapping of 12 motors:
#
# ______| Front Right | Front Left | Rear Right | Rear Left
# Hip   | FR_0 = 0    | FL_0 = 3   | RR_0 = 6   | RL_0 = 9
# Thigh | FR_1 = 1    | FL_1 = 4   | RR_1 = 7   | RL_1 = 10
# Knee  | FR_2 = 2    | FL_2 = 5   | RR_2 = 8   | RL_2 = 11
#
#
# Desired position for motor ID | COMMAND[ID * 5]
# Position gain for motor ID    | COMMAND[ID * 5 + 1]
# Desired speed for motor ID    | COMMAND[ID * 5 + 2]
# Damping gain for motor ID     | COMMAND[ID * 5 + 3]
# Desired torque for motor ID   | COMMAND[ID * 5 + 4]

LOW_SIZE = 60

# ///////////////////////////////////
# LEGGED SDK LOW LEVEL RECEIVE PACKET STRUCTURE
# ///////////////////////////////////


class LowLevelParser:
    '''Legged SDK Low Level parser'''

    def __init__(self):
        # // Low Level states and commands //
        self._zero_command = zeros(LOW_SIZE, dtype=float32)
        self._command = self._zero_command

        # Motor Gains
        self.position_gains = zeros(NUM_MOTORS)
        self.damping_gains = zeros(NUM_MOTORS)

        self.initialize_states()

    def initialize_states(self):
        # Motor states
        self.joint_angles = zeros(NUM_MOTORS)
        self.joint_speed = zeros(NUM_MOTORS)
        self.joint_torques = zeros(NUM_MOTORS)
        self.joint_temperature = zeros(NUM_MOTORS)

        self.motor_states = self.joint_angles, self.joint_speed

        # Foot force estimates
        self.foot_force = zeros(NUM_LEGS)
        self.foot_force_est = zeros(NUM_LEGS)

        # IMU states
        self.quaternion = None
        self.gyro = None
        self.accelerometer = None
        self.euler_angles = None

                # reference real-time from motion controller (unit: milliseconds)
        self.tick = 0

    def _reset_command(self):
        ''''''
        self._command = self._zero_command

    def parse_state(self, low_state):
        ''''''
        # parsing imu states
        self.quaternion = low_state.imu.quaternion
        self.gyro = low_state.imu.gyroscope
        self.accelerometer = low_state.imu.accelerometer
        # parsing the motor states
        _motors_state = low_state.motorState
        self._parse_motor_states(_motors_state)
        # parsing foot forces
        self.foot_force = low_state.footForce
        self.foot_force_est = low_state.footForceEst
        # get controller ticker
        self.tick = low_state.tick

    # def get_motor_states(self):
    #     motor_states = self.joint_angles, self.joint_speed
    #     return motor_states

    def _parse_motor_states(self, motors_state):
        ''''''
        for motor_id in range(NUM_MOTORS):
            self.joint_angles[motor_id] = motors_state[motor_id].q
            self.joint_speed[motor_id] = motors_state[motor_id].dq
            self.joint_torques[motor_id] = motors_state[motor_id].tauEst
            self.joint_temperature[motor_id] = motors_state[motor_id].temperature

    def build_command(self,
                      desired_pos=zeros(NUM_MOTORS),
                      desired_vel=zeros(NUM_MOTORS),
                      desired_torque=zeros(NUM_MOTORS),
                      position_gains=zeros(NUM_MOTORS),
                      damping_gains=zeros(NUM_MOTORS)):
        ''''''
        self._reset_command()

        for motor_id in range(NUM_MOTORS):
            self._command[motor_id * 5] = desired_pos[motor_id]
            self._command[motor_id * 5 + 1] = position_gains[motor_id]
            self._command[motor_id * 5 + 2] = desired_vel[motor_id]
            self._command[motor_id * 5 + 3] = damping_gains[motor_id]
            self._command[motor_id * 5 + 4] = desired_torque[motor_id]

        return self._command


class A1LowLevelParser(LowLevelParser):
    '''The A1 Low Level Robot parser'''

    def __init__(self):
        LowLevelParser.__init__(self)

class AliengoLowLevelParser(LowLevelParser):
    '''The Aliengo Low Level Robot parser'''

    def __init__(self):
        LowLevelParser.__init__(self)

