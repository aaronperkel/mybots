"""
simulation.py
Defines the Simulation class, which configures PyBullet, loads the world and robot,
runs the simulation loop, and orchestrates sensing and action each timestep.
"""

import constants as c
import pybullet as p
import pybullet_data
import time

from world import World
from robot import Robot

class Simulation:
    """
    Manages a single simulation instance in PyBullet.
    It sets up the physics client, loads the world and robot,
    runs the simulation loop, and orchestrates robot sensing and action.
    """
    def __init__(self, direct_or_gui, solution_id):
        """
        Initializes the simulation environment.

        Args:
            direct_or_gui (str): Specifies 'GUI' for graphical mode or 'DIRECT' for headless.
            solution_id (int): The ID of the solution being simulated, used to load
                               the corresponding robot brain.
        """
        self.direct_or_gui = direct_or_gui

        # Connect to PyBullet physics server
        if self.direct_or_gui == 'GUI':
            self.physics_client = p.connect(p.GUI)
            p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0) # Disable PyBullet's default GUI
        else:
            self.physics_client = p.connect(p.DIRECT) # Run in headless mode
        
        p.setAdditionalSearchPath(pybullet_data.getDataPath()) # For loading standard URDFs (e.g., plane)
        p.setGravity(c.GRAV_X, c.GRAV_Y, c.GRAV_Z)

        self.world = World()
        self.robot = Robot(solution_id)

    def __del__(self):
        """
        Ensures PyBullet disconnects when the simulation object is deleted.
        This is a cleanup measure to prevent resource leaks.
        """
        if p.isConnected(self.physics_client): # Check if connected before disconnecting
            p.disconnect(self.physics_client)

    def run(self):
        """
        Runs the main simulation loop for a predefined number of steps (c.STEPS).
        In each step, it advances the physics simulation and triggers the robot's
        sense-think-act cycle. If in GUI mode, a small delay is introduced
        to make the simulation viewable.
        """
        for i in range(c.STEPS):
            p.stepSimulation()
            self.robot.sense(i)
            self.robot.think()
            self.robot.act(i)
            if self.direct_or_gui == 'GUI':
                time.sleep(c.SLEEP_TIME)

    def get_fitness(self):
        """
        Retrieves the fitness of the robot from the current simulation run.
        This typically involves calling a method on the robot object that
        calculates or reports its fitness.
        """
        self.robot.get_fitness()
