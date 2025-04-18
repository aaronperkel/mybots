"""
constants.py
Holds global constants such as the number of simulation steps, motor frequencies, amplitudes,
and other physical constants (gravity, max force, etc.).
"""

STEPS = 5000

NUMBER_OF_GENERATIONS = 5
POPULATION_SIZE = 5

NUM_SENSOR_NEURONS = 4
NUM_MOTOR_NEURONS = 8

MOTOR_JOINT_RANGE = 0.2

GRAV_X = 0
GRAV_Y = 0
GRAV_Z = -9.8

MAX_FORCE = 20

SLEEP_TIME = 1/600