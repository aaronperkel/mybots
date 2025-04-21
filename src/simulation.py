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
        
        # choose fitness method: 'max' or 'avg'
        self.evalMethod = os.environ.get('FITNESS_METHOD', 'max')

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
        # gather x‐distances for all swarm members
        distances = []
        for robot in self.robots:
            pos, _ = p.getBasePositionAndOrientation(robot.robot_id)
            distances.append(pos[0])

        max_dist = max(distances)
        avg_dist = sum(distances) / len(distances)

        # save both for your A/B charts
        with open(f'./src/data/fitness_max{self.solutionID}.txt', 'w') as f:
            f.write(str(max_dist))
        with open(f'./src/data/fitness_avg{self.solutionID}.txt', 'w') as f:
            f.write(str(avg_dist))

        # pick which one drives the GA
        chosen = avg_dist if self.evalMethod == 'avg' else max_dist

        # write the “official” fitness file
        tmp = f'./src/data/tmp{self.solutionID}.txt'
        with open(tmp, 'w') as f:
            f.write(str(chosen))
        os.rename(tmp, f'./src/data/fitness{self.solutionID}.txt')

        # cleanup
        for fpath in glob("./src/data/body_*.urdf"):
            os.remove(fpath)