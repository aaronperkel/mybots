"""
constants.py
Holds global constants such as the number of simulation steps, motor frequencies, amplitudes,
and other physical constants (gravity, max force, etc.).
"""

import numpy as np

STEPS = 1000

NUMBER_OF_GENERATIONS = 15

AMPLITUDE_BL = np.pi/3
FREQUENCY_BL = 10
PHASE_OFFSET_BL = 0

AMPLITUDE_FL = np.pi/4
FREQUENCY_FL = 10
PHASE_OFFSET_FL = np.pi

GRAV_X = 0
GRAV_Y = 0
GRAV_Z = -9.8

MAX_FORCE = 20

SLEEP_TIME = 0.005
