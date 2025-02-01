"""
simulate.py
Script to run a PyBullet simulation that loads a plane and an SDF world file, 
sets gravity, and continuously steps through the simulation loop.
"""

import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time
import generate as g
import numpy as np

def main():
    STEPS = 1000
    g.main()

    physicsClient = p.connect(p.GUI)
    p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0,0,-9.8)
    p.loadSDF("world.sdf")

    planeId = p.loadURDF("plane.urdf")
    robotId = p.loadURDF("three_link.urdf")

    pyrosim.Prepare_To_Simulate(robotId)

    backLegSensorValues = np.zeros(STEPS)
    frontLegSensorValues = np.zeros(STEPS)

    for i in range(STEPS):
        p.stepSimulation()

        backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
        frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

        pyrosim.Set_Motor_For_Joint(
            bodyIndex = robotId,
            jointName = "Torso_BackLeg",
            controlMode = p.POSITION_CONTROL,
            targetPosition = -np.pi/3,
            maxForce = 500
        )

        pyrosim.Set_Motor_For_Joint(
            bodyIndex = robotId,
            jointName = "Torso_FrontLeg",
            controlMode = p.POSITION_CONTROL,
            targetPosition = np.pi/3,
            maxForce = 500
        )

        time.sleep(.005)

    p.disconnect()
    np.save('data/backLegSensorValues.npy', backLegSensorValues)
    np.save('data/frontLegSensorValues.npy', frontLegSensorValues)

if __name__ == '__main__':
    main()
