"""
constants.py
Holds global constants such as the number of simulation steps, motor frequencies, amplitudes,
and other physical constants (gravity, max force, etc.).
"""

STEPS = 10000
SLEEP_TIME = 1/600

MAX_FORCE = 30

NUMBER_OF_GENERATIONS = 75
POPULATION_SIZE = 3
SWARM_SIZE = 3

NUM_SENSOR_NEURONS = 4
NUM_MOTOR_NEURONS = 8
MOTOR_JOINT_RANGE = 0.75

GRAV_X = 0
GRAV_Y = 0
GRAV_Z = -9.8