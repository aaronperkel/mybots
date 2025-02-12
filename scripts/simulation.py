"""
simulation.py
Defines the SIMULATION class, which configures PyBullet, loads the world and robot,
runs the simulation loop, and orchestrates sensing and action each timestep.
"""

import constants as c
import pybullet as p
import pybullet_data
import numpy as np
import time

from world import WORLD
from robot import ROBOT

class SIMULATION:
    def __init__(self):
        self.physics_client = p.connect(p.DIRECT)
        p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(c.GRAV_X, c.GRAV_Y, c.GRAV_Z)

        self.world = WORLD()
        self.robot = ROBOT()

    def __del__(self):
        p.disconnect()

    def Run(self):
        for i in range(c.STEPS):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)
            time.sleep(c.SLEEP_TIME)

    def Get_Fitness(self):
        self.robot.Get_Fitness()
