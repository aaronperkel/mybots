"""
constants.py
Holds global constants such as the number of simulation steps, motor frequencies, amplitudes,
and other physical constants (gravity, max force, etc.).
"""

import numpy as np

STEPS = 1000

NUMBER_OF_GENERATIONS = 10
POPULATION_SIZE = 10

NUM_SENSOR_NEURONS = 4
NUM_MOTOR_NEURONS = 8

MOTOR_JOINT_RANGE = 0.4

GRAV_X = 0
GRAV_Y = 0
GRAV_Z = -9.8

MAX_FORCE = 20

SLEEP_TIME = 0.005
