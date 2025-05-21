"""
constants.py
Holds global constants such as the number of simulation steps, motor frequencies, amplitudes,
and other physical constants (gravity, max force, etc.).
"""

STEPS = 5000  # Number of simulation steps for each evaluation

# Evolutionary Algorithm parameters
NUMBER_OF_GENERATIONS = 5  # Number of generations for the evolutionary algorithm
POPULATION_SIZE = 5        # Number of solutions in each generation

# Neural Network topology
NUM_SENSOR_NEURONS = 4  # Number of sensor neurons in the neural network
NUM_MOTOR_NEURONS = 8   # Number of motor neurons in the neural network

MOTOR_JOINT_RANGE = 0.2  # Range of motion for motor joints

# Physics engine parameters
GRAV_X = 0      # Gravitational acceleration in X
GRAV_Y = 0      # Gravitational acceleration in Y
GRAV_Z = -9.8   # Gravitational acceleration in Z (standard Earth gravity)

MAX_FORCE = 20  # Maximum force applicable by motors

SLEEP_TIME = 1/600  # Sleep time for GUI simulation to slow it down for visualization
