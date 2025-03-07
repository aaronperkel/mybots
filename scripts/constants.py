"""
constants.py
Holds global constants such as the number of simulation steps, motor frequencies, amplitudes,
and other physical constants (gravity, max force, etc.).
"""

import numpy as np

STEPS = 1000

NUMBER_OF_GENERATIONS = 1
POPULATION_SIZE = 1

NUM_SENSOR_NEURONS = 9
NUM_MOTOR_NEURONS = 8

MOTOR_JOINT_RANGE = 0.2

AMPLITUDE_BL = 1.0
FREQUENCY_BL = 2.0
PHASE_OFFSET_BL = 0

AMPLITUDE_FL = 1.0
FREQUENCY_FL = 2.0
PHASE_OFFSET_FL = np.pi

GRAV_X = 0
GRAV_Y = 0
GRAV_Z = -9.8

MAX_FORCE = 20

SLEEP_TIME = 0.005
