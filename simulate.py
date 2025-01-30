"""
simulate.py
Script to run a PyBullet simulation that loads a plane and an SDF world file, 
sets gravity, and continuously steps through the simulation loop.
"""

import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time

def main():
    running = True

    physicsClient = p.connect(p.GUI)
    p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0,0,-9.8)
    p.loadSDF("world.sdf")

    planeId = p.loadURDF("plane.urdf")
    robotId = p.loadURDF("three_link.urdf")

    pyrosim.Prepare_To_Simulate(robotId)
    while running:
        p.stepSimulation()
        # Adding a touch sensor to the back leg
        backLegTouch = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
        time.sleep(.005)

    p.disconnect()

if __name__ == '__main__':
    main()
