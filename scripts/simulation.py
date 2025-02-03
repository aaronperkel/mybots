"""
simulation.py
Defines the SIMULATION class, which configures PyBullet, loads the world and robot,
runs the simulation loop, and orchestrates sensing and action each timestep.
"""

class SIMULATION:
    def __init__(self):
        import constants as c
        import pybullet as p
        import pybullet_data
        import numpy as np

        from world import WORLD
        from robot import ROBOT

        c.STEPS = 1000

        c.AMPLITUDE_BL = np.pi/3
        c.FREQUENCY_BL = 10
        c.PHASE_OFFSET_BL = 0

        c.AMPLITUDE_FL = np.pi/4
        c.FREQUENCY_FL = 10
        c.PHASE_OFFSET_FL = np.pi

        self.physics_client = p.connect(p.GUI)
        p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(c.GRAV_X, c.GRAV_Y, c.GRAV_Z)

        self.world = WORLD()
        self.robot = ROBOT()

    def __del__(self):
        import pybullet as p
        
        p.disconnect()

    def Run(self):
        import constants as c
        import pybullet as p
        import time

        for i in range(c.STEPS):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Act(i)
            time.sleep(c.SLEEP_TIME)