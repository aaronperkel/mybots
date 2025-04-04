"""
simulation.py
Defines the SIMULATION class, which configures PyBullet, loads the world and robot,
runs the simulation loop, and orchestrates sensing and action each timestep.
"""

import constants as c
import pybullet as p
import pybullet_data
import time
import os
from glob import glob

from world import WORLD
from robot import ROBOT

class SIMULATION:
    def __init__(self, directOrGUI, solutionID):
        self.directOrGUI = directOrGUI

        if self.directOrGUI == 'GUI':
            self.physics_client = p.connect(p.GUI)
        else:
            self.physics_client = p.connect(p.DIRECT)
        
        p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(c.GRAV_X, c.GRAV_Y, c.GRAV_Z)

        self.world = WORLD()
        
        self.robots = []
        urdf_files = sorted(glob("./src/data/body_*.urdf"))
        for i, urdf_file in enumerate(urdf_files):
            self.robots.append(ROBOT(i, urdf_file))

    def __del__(self):
        p.disconnect()

    def Run(self):
        for i in range(c.STEPS):
            p.stepSimulation()
            for robot in self.robots:
                robot.Sense(i)
                robot.Think()
                robot.Act(i)
            if self.directOrGUI == 'GUI':
                time.sleep(c.SLEEP_TIME)

    def Get_Fitness(self):
        fitnesses = []
        for robot in self.robots:
            robot.Get_Fitness()
            with open(f'./src/data/fitness{robot.solutionID}.txt', 'r') as f:
                fitnesses.append(float(f.read()))
        for robot in self.robots:
            os.remove(f'./src/data/fitness{robot.solutionID}.txt')
        for file in glob("./src/data/body_*.urdf"):
            os.remove(file)