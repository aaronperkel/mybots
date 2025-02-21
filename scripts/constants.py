"""
constants.py
Holds global constants such as the number of simulation steps, motor frequencies, amplitudes,
and other physical constants (gravity, max force, etc.).
"""

import numpy as np

STEPS = 1000

NUMBER_OF_GENERATIONS = 10

POPULATION_SIZE = 10

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
