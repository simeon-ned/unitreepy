
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
#  JOINT_MAPPING
# ///////////////
#  Joint names are given by concatenation of
#  LEG_NAME + JOINT_TYPE as in following table
#
# ______| Front Right | Front Left | Rear Right | Rear Left
# Hip   | FR_0 = 0    | FL_0 = 3   | RR_0 = 6   | RL_0 = 9
# Thigh | FR_1 = 1    | FL_1 = 4   | RR_1 = 7   | RL_1 = 10
# Knee  | FR_2 = 2    | FL_2 = 5   | RR_2 = 8   | RL_2 = 11

GAINS = {0: {'P': 100, 'D': 1},
         1: {'P': 100, 'D': 2},
         2: {'P': 100, 'D': 2}}

# Define the joint limits in rad

LEG_JOINT_LIMITS = {0: {'MIN': -0.802, 'MAX': 0.802},
                    1: {'MIN': -1.05, 'MAX': 4.19},
                    2: {'MIN': -2.7, 'MAX': -0.916}}

# Define torque limits in Nm

LEG_TORQUE_LIMITS = {0: {'MIN': -10, 'MAX': 10},
                     1: {'MIN': -10, 'MAX': 10},
                     2: {'MIN': -10, 'MAX': 10}}

LEG_JOINT_INITS = {0: 0,
                   1: 0,
                   2: 0}

LEG_JOINT_OFFSETS = {0: 0,
                     1: 0,
                     2: 0}


# TODO: Do it more concisely


# stand_angles = 4*[0.0, 0.77, -1.82]

# init_angles = [-0.25,  1.14, -2.72,
#                0.25,  1.14, -2.72,
#                -0.25,  1.14, -2.72,
#                0.25,  1.14, -2.72]


# ////////////////////////////////////////////////////////////////////////

JOINT_CONSTANTS = {
    'OFFSETS': [],
    'INITS': [],
    'POS_LIMITS': {'MIN': [],
                   'MAX': []},
    'TORQUE_LIMITS': {'MIN': [],
                      'MAX': []},
    'GAINS': {'P': [],
              'D': []}}

for JOINT in range(NUM_MOTORS):

    JOINT_ID = JOINT % 3
    JOINT_CONSTANTS['OFFSETS'].append(LEG_JOINT_INITS[JOINT_ID])
    JOINT_CONSTANTS['INITS'].append(LEG_JOINT_OFFSETS[JOINT_ID])

    for BOUND in {'MIN', 'MAX'}:
        POS_LIMIT = LEG_JOINT_LIMITS[JOINT_ID][BOUND]
        JOINT_CONSTANTS['TORQUE_LIMITS'][BOUND].append(POS_LIMIT)
        JOINT_CONSTANTS['POS_LIMITS'][BOUND].append(POS_LIMIT)

    for GAIN_TYPE in {'P', 'D'}:
        GAIN = GAINS[JOINT_ID][GAIN_TYPE]
        JOINT_CONSTANTS['GAINS'][GAIN_TYPE].append(GAIN)


JOINT_LIMITS = JOINT_CONSTANTS['POS_LIMITS']
JOINT_LIMITS_MIN = JOINT_LIMITS['MIN']
JOINT_LIMITS_MAX = JOINT_LIMITS['MAX']

TORQUE_LIMITS = JOINT_CONSTANTS['TORQUE_LIMITS']
TORQUE_LIMITS_MIN = TORQUE_LIMITS['MIN']
TORQUE_LIMITS_MAX = TORQUE_LIMITS['MAX']

JOINT_OFFSETS = JOINT_CONSTANTS['OFFSETS']
JOINT_INITS = JOINT_CONSTANTS['INITS']
POSITION_GAINS = JOINT_CONSTANTS['GAINS']['P']
DAMPING_GAINS = JOINT_CONSTANTS['GAINS']['D']

# ////////////////////////////////////////////////////////////////////////


# TODO: Add high level commands scaling factors

# KINEMATIC_PARAMETERS


LEG_KINEMATICS = [0.0838,
                  0.2,
                  0.2]

TRUNK_LENGTH = 0.1805 * 2

TRUNK_WIDTH = 0.047 * 2

LEGS_BASES = [[TRUNK_LENGTH/2, -TRUNK_WIDTH/2],
              [TRUNK_LENGTH/2, TRUNK_WIDTH/2],
              [-TRUNK_LENGTH/2, -TRUNK_WIDTH/2],
              [-TRUNK_LENGTH/2, TRUNK_WIDTH/2]]


# LEG_DYNAMICS =
# BODY_DYNAMICS =
