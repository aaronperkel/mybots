"""
constants.py
Holds global constants such as the number of simulation steps, motor frequencies, amplitudes,
and other physical constants (gravity, max force, etc.).
"""

import numpy as np

STEPS = 3500

NUMBER_OF_GENERATIONS = 10

POPULATION_SIZE = 10

AMPLITUDE = np.pi/4
FREQUENCYL = 10
PHASE_OFFSET = 0

GRAV_X = 0
GRAV_Y = 0
GRAV_Z = -9.8

MAX_FORCE = 20

SLEEP_TIME = 0.005
