"""
generate.py
Contains methods for programmatically generating SDF and URDF files for the robot(s) and environment.
"""

from pyrosim import pyrosim
import random
import os


def create_world():
    """
    Create an SDF file named 'world.sdf' containing a single cube.
    """
    pyrosim.Start_SDF("data/world.sdf")
    pyrosim.Send_Cube(name="Box", pos=[-4, 4, 0.5], size=[1, 1, 1])
    pyrosim.End()


def Generate_Body():
    """
    Creates a 3-link robot with two revolute joints.
    """
    pyrosim.Start_URDF("data/body.urdf")

    pyrosim.Send_Cube(
        name="Torso",
        pos=[1.5, 0.0, 1.5],
        size=[1, 1, 1]
    )

    # Second joint: Torso -> FrontLeg
    pyrosim.Send_Joint(
        name="Torso_FrontLeg",
        parent="Torso",
        child="FrontLeg",
        type="revolute",
        position=[2.0, 0.0, 1.0],
    )


    pyrosim.Send_Cube(
        name="FrontLeg",
        pos=[0.5, 0.0, -0.5],
        size=[1, 1, 1]
    )

    # First joint: Torso -> BackLeg
    pyrosim.Send_Joint(
        name="Torso_BackLeg",
        parent="Torso",
        child="BackLeg",
        type="revolute",
        position=[1.0, 0.0, 1.0],
    )
    pyrosim.Send_Cube(
        name="BackLeg",
        pos=[-0.5, 0.0, -0.5],
        size=[1, 1, 1]
    )
    pyrosim.End()


def Generate_Brain():
    """
    Creates a brain.
    """
    pyrosim.Start_NeuralNetwork("data/brain.nndf")
    pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
    pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
    pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")
    pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
    pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")

    for i in range(3):
        for j in range(3,5):
            pyrosim.Send_Synapse(sourceNeuronName=i, targetNeuronName=j, weight=2*random.random()-1)
    pyrosim.End()


def main():
    """
    Main function to create both the robot
    """
    create_world()
    Generate_Body()
    Generate_Brain()


if __name__ == "__main__":
    if not os.path.exists("data"):
        os.makedirs("data")
    main()
