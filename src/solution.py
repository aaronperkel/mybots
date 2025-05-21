"""
solution.py

This module defines the Solution class, which represents an individual
in the evolutionary algorithm. Each solution encapsulates a set of neural
network weights, a unique ID, and its fitness score. It handles its own
evaluation by creating the necessary robot definition files (world, body, brain)
and launching a simulation.
"""

import numpy as np
from pyrosim import pyrosim
import os
import random
import time
import constants as c
import subprocess

class Solution:
    def __init__(self, next_available_id):
        """
        Represents a single solution (a set of neural network weights) in the evolutionary search.

        Args:
            next_available_id (int): The unique ID for this solution.
        """
        self.my_id = next_available_id
        # Initialize weights with random values between -1 and 1.
        self.weights = np.random.rand(c.NUM_SENSOR_NEURONS, c.NUM_MOTOR_NEURONS) * 2 - 1
        self.fitness = None # Fitness is determined after evaluation

    def evaluate(self, direct_or_gui='DIRECT'):
        """
        Evaluates the solution by running a simulation and retrieving its fitness.

        Args:
            direct_or_gui (str): Specifies whether to run the simulation in 'DIRECT' (headless)
                                 or 'GUI' (graphical) mode.
        """
        self.start_simulation(direct_or_gui)
        self.wait_for_simulation_to_end()

    def start_simulation(self, direct_or_gui='DIRECT'):
        """
        Starts a simulation for this solution.
        It creates the world, body, and brain files, then launches simulate.py
        as a separate, non-blocking process.

        Args:
            direct_or_gui (str): Mode for the simulation ('DIRECT' or 'GUI').
        """
        self.create_world()
        self.create_body()
        self.create_brain()
        
        command = [
            "python", "./src/simulate.py", 
            direct_or_gui, str(self.my_id)
        ]
        # Launch simulate.py. stdout and stderr are redirected to /dev/null
        # to prevent cluttering the console. Popen is non-blocking.
        # The 'process' variable is not stored as we don't need to wait for it here.
        subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def wait_for_simulation_to_end(self):
        """
        Waits for the simulation (started by `start_simulation`) to complete.
        Completion is signaled by the existence of a fitness file for this solution's ID.
        Once the file appears, it reads the fitness, stores it in `self.fitness`,
        and then deletes the fitness file.
        """
        fitness_file_path = f'./src/data/fitness{self.my_id}.txt'
        while not os.path.exists(fitness_file_path):
            time.sleep(0.01)  # Brief pause to avoid busy-waiting and reduce CPU load.
        
        try:
            with open(fitness_file_path, 'r') as f:
                self.fitness = float(f.read().strip())
        except FileNotFoundError:
            print(f"Error: Fitness file {fitness_file_path} not found after waiting.")
            self.fitness = -float('inf') # Assign a very low fitness if file disappears
        except ValueError:
            print(f"Error: Could not convert fitness value in {fitness_file_path} to float.")
            self.fitness = -float('inf') # Assign a very low fitness if content is invalid
        finally:
            # Clean up the fitness file
            if os.path.exists(fitness_file_path):
                try:
                    os.remove(fitness_file_path)
                except OSError as e:
                    print(f"Error deleting fitness file {fitness_file_path}: {e}")

    def create_world(self):
        """
        Creates the simulation world definition (world.sdf) file.
        This world contains a single static box.
        The data directory is created if it doesn't exist.
        """
        data_dir = "./src/data"
        if not os.path.exists(data_dir):
            try:
                os.makedirs(data_dir)
            except OSError as e:
                print(f"Error creating directory {data_dir}: {e}")
                return # Avoid proceeding if directory creation fails
        
        world_sdf_path = os.path.join(data_dir, "world.sdf")
        pyrosim.Start_SDF(world_sdf_path)
        pyrosim.Send_Cube(name="Box", pos=[-4, 4, 0.5], size=[1, 1, 1])
        pyrosim.End()

    def create_body(self):
        """
        Creates the robot's body structure definition (body.urdf) file.
        This version defines a robot with a torso and four legs, each with a lower segment.
        """
        body_urdf_path = os.path.join("./src/data", "body.urdf")
        pyrosim.Start_URDF(body_urdf_path)
        
        pyrosim.Send_Cube(name="Torso", pos=[0.0, 0.0, 1.0], size=[1, 1, 1])
        
        # Definitions for upper legs: (name_suffix, joint_pos, joint_axis, leg_relative_pos, leg_size)
        legs_params = [
            ("BackLeg", [0.0, -0.5, 1.0], '1 0 0', [0.0, -0.5, 0.0], [0.2, 1.0, 0.2]),
            ("FrontLeg", [0.0, 0.5, 1.0], '1 0 0', [0.0, 0.5, 0.0], [0.2, 1.0, 0.2]),
            ("LeftLeg", [-0.5, 0.0, 1.0], '0 1 0', [-0.5, 0.0, 0.0], [1.0, 0.2, 0.2]),
            ("RightLeg", [0.5, 0.0, 1.0], '0 1 0', [0.5, 0.0, 0.0], [1.0, 0.2, 0.2]),
        ]

        for name_suffix, pos_joint, axis, pos_leg, size_leg in legs_params:
            pyrosim.Send_Joint(
                name=f"Torso_{name_suffix}", parent="Torso", child=name_suffix,
                type="revolute", position=pos_joint, jointAxis=axis
            )
            pyrosim.Send_Cube(name=name_suffix, pos=pos_leg, size=size_leg)

        # Definitions for lower legs: (name, parent_leg_name, joint_pos_relative_to_parent, joint_axis, lower_leg_relative_pos, lower_leg_size)
        lower_legs_params = [
            ("FrontLowerLeg", "FrontLeg", [0.0, 1.0, 0.0], '1 0 0', [0.0, 0.0, -0.5], [0.2, 0.2, 1.0]),
            ("BackLowerLeg", "BackLeg", [0.0, -1.0, 0.0], '1 0 0', [0.0, 0.0, -0.5], [0.2, 0.2, 1.0]),
            ("LeftLowerLeg", "LeftLeg", [-1.0, 0.0, 0.0], '0 1 0', [0.0, 0.0, -0.5], [0.2, 0.2, 1.0]),
            ("RightLowerLeg", "RightLeg", [1.0, 0.0, 0.0], '0 1 0', [0.0, 0.0, -0.5], [0.2, 0.2, 1.0]),
        ]

        for name, parent_name, pos_joint, axis, pos_lower_leg, size_lower_leg in lower_legs_params:
            pyrosim.Send_Joint(
                name=f"{parent_name}_{name}", parent=parent_name, child=name,
                type="revolute", position=pos_joint, jointAxis=axis
            )
            pyrosim.Send_Cube(name=name, pos=pos_lower_leg, size=size_lower_leg)
        
        pyrosim.End()

    def create_brain(self):
        """
        Creates the neural network definition file (brainX.nndf) for the robot.
        It defines sensor neurons, motor neurons, and the synapses connecting them,
        using the weights stored in `self.weights`.
        """
        brain_nndf_path = os.path.join("./src/data", f"brain{self.my_id}.nndf")
        pyrosim.Start_NeuralNetwork(brain_nndf_path)
        
        # Sensor neurons: name_id -> link_name
        sensor_neurons_map = {
            0: "FrontLowerLeg", 1: "BackLowerLeg",
            2: "LeftLowerLeg",  3: "RightLowerLeg"
        }
        for neuron_id, link_name in sensor_neurons_map.items():
            pyrosim.Send_Sensor_Neuron(name=neuron_id, linkName=link_name)

        # Motor neurons: name_id -> joint_name
        motor_neurons_map = {
            4: "Torso_BackLeg",          5: "Torso_FrontLeg",
            6: "Torso_LeftLeg",          7: "Torso_RightLeg",
            8: "FrontLeg_FrontLowerLeg", 9: "BackLeg_BackLowerLeg",
            10: "LeftLeg_LeftLowerLeg",  11: "RightLeg_RightLowerLeg"
        }
        for neuron_id, joint_name in motor_neurons_map.items():
            pyrosim.Send_Motor_Neuron(name=neuron_id, jointName=joint_name)

        # Create synapses:
        # Assumes sensor neuron names are 0 to NUM_SENSOR_NEURONS-1
        # Assumes motor neuron names are NUM_SENSOR_NEURONS to NUM_SENSOR_NEURONS+NUM_MOTOR_NEURONS-1
        # This matches the indexing in self.weights array.
        for r_idx in range(c.NUM_SENSOR_NEURONS):
            # actual_sensor_neuron_name corresponds to keys in sensor_neurons_map
            actual_sensor_neuron_name = r_idx 
            for c_idx in range(c.NUM_MOTOR_NEURONS):
                # actual_motor_neuron_name corresponds to keys in motor_neurons_map
                # The targetNeuronName for Send_Synapse is the 'name' attribute in the NNDF.
                actual_motor_neuron_name = c_idx + c.NUM_SENSOR_NEURONS
                
                weight = self.weights[r_idx, c_idx] # Direct indexing if shapes match
                pyrosim.Send_Synapse(
                    sourceNeuronName=actual_sensor_neuron_name, 
                    targetNeuronName=actual_motor_neuron_name, 
                    weight=weight
                )
        pyrosim.End()

    def mutate(self):
        """
        Applies mutation to the solution's weights by randomly changing one weight
        to a new value between -1 and 1.
        """
        # Choose a random weight to mutate.
        rand_row = random.randint(0, self.weights.shape[0] - 1)
        rand_col = random.randint(0, self.weights.shape[1] - 1)
        # Assign a new random weight between -1 and 1.
        self.weights[rand_row, rand_col] = random.uniform(-1, 1)

    def set_id(self, new_id):
        """
        Sets the ID of the solution.

        Args:
            new_id (int): The new unique ID for this solution.
        """
        self.my_id = new_id