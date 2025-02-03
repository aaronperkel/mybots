"""
simulate.py
Script to run a PyBullet simulation that loads a plane and an SDF world file,
sets gravity, and continuously steps through the simulation loop.
"""

import time

import pybullet as p
import pybullet_data
import numpy as np
import random

from pyrosim import pyrosim
from scripts import generate


def main():
    """
    Main function to create the world/robot, load them in PyBullet, and simulate.
    """
    STEPS = 1000

    AMPLITUDE_BL = np.pi/3
    FREQUENCY_BL = 10
    PHASE_OFFSET_BL = 0

    AMPLITUDE_FL = np.pi/4
    FREQUENCY_FL = 10
    PHASE_OFFSET_FL = np.pi

    # Generate the world and a sample 3-link robot
    generate.main()

    physics_client = p.connect(p.GUI)
    p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.8)

    # Because generate.py wrote 'world.sdf' in data/ but we load it here:
    # either move or rename to load the correct path
    p.loadSDF("data/world.sdf")

    plane_id = p.loadURDF("plane.urdf")
    robot_id = p.loadURDF("data/three_link.urdf")

    pyrosim.Prepare_To_Simulate(robot_id)

    i_vals = np.arange(STEPS)
    target_angles_bl = AMPLITUDE_BL * np.sin(2 * np.pi * FREQUENCY_BL * i_vals / STEPS + PHASE_OFFSET_BL)
    target_angles_fl = AMPLITUDE_FL * np.sin(2 * np.pi * FREQUENCY_FL * i_vals / STEPS + PHASE_OFFSET_FL)

    back_leg_vals = np.zeros(STEPS)
    front_leg_vals = np.zeros(STEPS)

    # np.save("data/sin_values_bl.npy", target_angles_bl)
    # np.save("data/sin_values_fl.npy", target_angles_fl)
    # exit()

    for i in range(STEPS):
        p.stepSimulation()

        back_leg_vals[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
        front_leg_vals[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

        pyrosim.Set_Motor_For_Joint(
            bodyIndex=robot_id,
            jointName="Torso_BackLeg",
            controlMode=p.POSITION_CONTROL,
            targetPosition=target_angles_bl[i],
            maxForce=20,
        )

        pyrosim.Set_Motor_For_Joint(
            bodyIndex=robot_id,
            jointName="Torso_FrontLeg",
            controlMode=p.POSITION_CONTROL,
            targetPosition=target_angles_fl[i],
            maxForce=20,
        )

        time.sleep(0.005)

    p.disconnect()

    # Save sensor arrays for analysis
    np.save("data/backLegSensorValues.npy", back_leg_vals)
    np.save("data/frontLegSensorValues.npy", front_leg_vals)


def random_in_range(low, high):
    return low + (high - low) * random.random()


if __name__ == "__main__":
    main()
