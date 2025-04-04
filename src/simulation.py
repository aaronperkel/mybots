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
        self.solutionID = solutionID

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
        for urdf_file in urdf_files:
            self.robots.append(ROBOT(self.solutionID, urdf_file))

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
        # 1) Pick a single robot to write the fitness file
        #    In a swarm with a shared ID, it doesn't matter which one.
        chosen_robot = self.robots[-1]
        chosen_robot.Get_Fitness()

        # 2) Now read that single fitness file
        #    (All swarm members share self.solutionID, so it’s 'fitness{solutionID}.txt')
        with open(f'./src/data/fitness{self.solutionID}.txt', 'r') as f:
            best = float(f.read())

        # 3) Write it back under the same name (or rename if needed)
        with open(f'./src/data/tmp{self.solutionID}.txt', 'w') as f:
            f.write(str(best))
        os.rename(
            f'./src/data/tmp{self.solutionID}.txt',
            f'./src/data/fitness{self.solutionID}.txt'
        )

        # 4) Remove extra URDF files, if you want to keep the directory clean
        for file in glob("./src/data/body_*.urdf"):
            os.remove(file)