# Number of motors
NUM_MOTORS = 12
# Number of legs
NUM_LEGS = 4

# //////
#  Legs
# //////

LEG_NAMES = ["FR",  # Front Right
             "FL",  # Front Left
             "RR",  # Rear Right
             "RL"]  # Rear Left

# //////////////
#  Joint Types:
# //////////////

JOINT_TYPES = [0,  # Hip
               1,  # Thigh
               2]  # Knee

# ///////////////
#  Joint Mapping
# ///////////////
#  Joint names are given by concatenation of
#  LEG_NAME + JOINT_TYPE as in following table
#
# ______| Front Right | Front Left | Rear Right | Rear Left
# Hip   | FR_0 = 0    | FL_0 = 3   | RR_0 = 6   | RL_0 = 9
# Thigh | FR_1 = 1    | FL_1 = 4   | RR_1 = 7   | RL_1 = 10
# Knee  | FR_2 = 2    | FL_2 = 5   | RR_2 = 8   | RL_2 = 11


# ///////////////
# Joint Constants 
# ///////////////

JOINT_LIMITS_MIN = 4*[-0.802, -1.05, -2.7]
JOINT_LIMITS_MAX = 4*[0.802, 4.19, 0.916]

TORQUE_LIMITS_MIN = -4*[-10, -10, -10]
TORQUE_LIMITS_MAX = 4*[10, 10, 10]

# Motor angles in initial stand pose
STAND_ANGLES = 4*[0.0, 0.8, -1.65]

# Motor angles of initialization pose
INIT_ANGLES = [-0.25,  1.14, -2.72,  # FR
               0.25,  1.14, -2.72,  # FL
               -0.25,  1.14, -2.72,  # RR
               0.25,  1.14, -2.72]  # RL

POSITION_GAINS = 4*[100, 100, 100]

DAMPING_GAINS = 4*[1, 2, 2]

# ////////////////////

# TODO: Add high level commands scaling factors


# ////////////////////
# KINEMATIC_PARAMETERS
# ////////////////////

TRUNK_LENGTH = 0.1805 * 2
TRUNK_WIDTH = 0.047 * 2

LEGS_BASES = {'FR': [TRUNK_LENGTH/2, -TRUNK_WIDTH/2],
              'FL': [TRUNK_LENGTH/2, TRUNK_WIDTH/2],
              'RR': [-TRUNK_LENGTH/2, -TRUNK_WIDTH/2],
              'RL': [-TRUNK_LENGTH/2, TRUNK_WIDTH/2]}

LEG_LINKS_LENGTH = {'FR': [0.0838, 0.2, 0.2],
                    'FL': [-0.0838, 0.2, 0.2],
                    'RR': [0.0838, 0.2, 0.2],
                    'RL': [-0.0838, 0.2, 0.2]}

# LEG_DYNAMICS =
# BODY_DYNAMICS =
BODY_MASS = None
BODY_INERTIA = None
MOTOR_INERTIAS = None
MOTOR_DAMPING = None
