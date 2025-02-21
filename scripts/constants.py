"""
constants.py
Holds global constants such as the number of simulation steps, motor frequencies, amplitudes,
and other physical constants (gravity, max force, etc.).
"""

import numpy as np

STEPS = 1000

NUMBER_OF_GENERATIONS = 25

POPULATION_SIZE = 7

AMPLITUDE_BL = 0.8
FREQUENCY_BL = 1.5
PHASE_OFFSET_BL = 0

AMPLITUDE_FL = 0.8
FREQUENCY_FL = 1.5
PHASE_OFFSET_FL = np.pi/2

GRAV_X = 0
GRAV_Y = 0
GRAV_Z = -9.8

MAX_FORCE = 20

SLEEP_TIME = 0.005
