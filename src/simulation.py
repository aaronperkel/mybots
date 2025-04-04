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
            # Each robot writes e.g. fitness0.txt, fitness1.txt, ...
            robot.Get_Fitness()
            with open(f'./src/data/fitness{robot.solutionID}.txt', 'r') as f:
                val = float(f.read())
                fitnesses.append(val)
        
        # For the “strength in numbers” objective, we take the max distance:
        best = max(fitnesses)

        # Now write this max distance to the file your solution code is *actually* waiting for:
        solutionID_from_command_line = int(self.solutionID)  # e.g. sys.argv[2]
        with open(f'./src/data/tmp{solutionID_from_command_line}.txt', 'w') as f:
            f.write(str(best))
        os.rename(
            f'./src/data/tmp{solutionID_from_command_line}.txt',
            f'./src/data/fitness{solutionID_from_command_line}.txt'
        )

        # Clean up each robot’s individual fitness file:
        for robot in self.robots:
            os.remove(f'./src/data/fitness{robot.solutionID}.txt')
        
        # Clean up the URDF files:
        for file in glob("./src/data/body_*.urdf"):
            os.remove(file)