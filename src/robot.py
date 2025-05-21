"""
robot.py
Defines the Robot class, which aggregates all the robot's sensors and motors.
It loads the robot's URDF, prepares the sensors and motors, and coordinates sensing/acting.
"""

import pybullet as p
from pyrosim import pyrosim
from sensor import Sensor
from motor import Motor
from pyrosim.neuralNetwork import NeuralNetwork
import os
import constants as c

class Robot:
    """
    Represents the robot in the simulation. This class handles the robot's
    physical presence (URDF), its neural network, sensors, and motors.
    It coordinates the sense-think-act cycle.
    """
    def __init__(self, solution_id):
        """
        Initializes the Robot.

        Args:
            solution_id (int): The unique identifier for this robot's brain (solution).
                               This ID is used to load the correct neural network file.
        """
        self.solution_id = solution_id
        self.robot_id = p.loadURDF("./src/data/body.urdf") # Load robot model
        pyrosim.Prepare_To_Simulate(self.robot_id) # Prepare Pyrosim for this robot

        # Load the neural network for this robot
        brain_file_path = f"./src/data/brain{self.solution_id}.nndf"
        self.nn = NeuralNetwork(brain_file_path)
        
        self.prepare_to_sense() # Initialize sensors
        self.prepare_to_act()   # Initialize motors
        
        # Clean up the temporary brain file after it's loaded into the neural network.
        if os.path.exists(brain_file_path):
            try:
                os.remove(brain_file_path)
            except OSError as e:
                print(f"Error deleting brain file {brain_file_path}: {e}")

    def prepare_to_sense(self):
        """
        Initializes all sensors for the robot based on its URDF definition.
        Each link in the URDF gets a corresponding Sensor object.
        """
        self.sensors = {}
        for link_name in pyrosim.linkNamesToIndices:
            self.sensors[link_name] = Sensor(link_name)

    def sense(self, t):
        """
        Collects sensor data from the environment at the current time step.

        Args:
            t (int): The current simulation time step.
        """
        for sensor_obj in self.sensors.values(): # Iterate directly over values
            sensor_obj.get_value(t)

    def prepare_to_act(self):
        """
        Initializes all motors for the robot based on its URDF definition.
        Each joint in the URDF gets a corresponding Motor object.
        """
        self.motors = {}
        for joint_name in pyrosim.jointNamesToIndices:
            self.motors[joint_name] = Motor(joint_name)

    def act(self, t):
        """
        Performs actions based on the neural network's output at the current time step.
        The neural network determines the desired angle for each motor.
        Note: Parameter 't' (time step) is currently unused in this method but
        is kept for potential future use and API consistency.
        """
        for neuron_name in self.nn.get_neuron_names():
            if self.nn.is_motor_neuron(neuron_name):
                joint_name = self.nn.get_motor_neurons_joint(neuron_name)
                desired_angle = self.nn.get_value_of(neuron_name) * c.MOTOR_JOINT_RANGE
                self.motors[joint_name].set_value(desired_angle, self.robot_id)

    def think(self):
        """
        Updates the state of the robot's neural network.
        This typically involves propagating activation values through the network.
        """
        self.nn.update()

    def get_fitness(self):
        """
        Calculates the robot's fitness based on its performance (e.g., distance traveled).
        The fitness value (x-position of the base) is written to a temporary file,
        which is then renamed to a final fitness file.
        """
        base_position_and_orientation = p.getBasePositionAndOrientation(self.robot_id) # Renamed variable
        base_position = base_position_and_orientation[0] # Renamed variable
        x_position = base_position[0] # Renamed variable
        
        # Use self.solution_id for consistency
        tmp_fitness_file = f'./src/data/tmp{self.solution_id}.txt'
        final_fitness_file = f'./src/data/fitness{self.solution_id}.txt'

        with open(tmp_fitness_file, 'w') as f:
            f.write(str(x_position))
        
        try:
            os.rename(tmp_fitness_file, final_fitness_file)
        except FileNotFoundError:
            print(f"Error: Temporary fitness file {tmp_fitness_file} not found for renaming.")
        except OSError as e:
            print(f"Error renaming fitness file {tmp_fitness_file} to {final_fitness_file}: {e}")
