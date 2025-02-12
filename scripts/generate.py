"""
generate.py
Contains methods for programmatically generating SDF and URDF files for the robot(s) and environment.
"""

from pyrosim import pyrosim
import random
import os


if not os.path.exists("data"):
    os.makedirs("data")


def create_world():
    """
    Create an SDF file named 'world.sdf' containing a single cube.
    """
    pyrosim.Start_SDF("data/world.sdf")
    pyrosim.Send_Cube(name="Box", pos=[-4, 4, 0.5], size=[1, 1, 1])
    pyrosim.End()


def create_robot():
    """
    Create a URDF file named 'body.urdf' containing a multi-link robot.
    """
    pyrosim.Start_URDF("data/body.urdf")

    pyrosim.Send_Cube(name="Link0", pos=[0, 0, 0.5], size=[1, 1, 1])
    pyrosim.Send_Joint(
        name="Link0_Link1",
        parent="Link0",
        child="Link1",
        type="revolute",
        position=[0.0, 0.0, 1.0],
    )
    pyrosim.Send_Cube(name="Link1", pos=[0, 0, 0.5], size=[1, 1, 1])

    pyrosim.Send_Joint(
        name="Link1_Link2",
        parent="Link1",
        child="Link2",
        type="revolute",
        position=[0.0, 0.0, 1.0],
    )
    pyrosim.Send_Cube(name="Link2", pos=[0, 0, 0.5], size=[1, 1, 1])

    pyrosim.Send_Joint(
        name="Link2_Link3",
        parent="Link2",
        child="Link3",
        type="revolute",
        position=[0.0, 0.5, 0.5],
    )
    pyrosim.Send_Cube(name="Link3", pos=[0, 0.5, 0], size=[1, 1, 1])

    pyrosim.Send_Joint(
        name="Link3_Link4",
        parent="Link3",
        child="Link4",
        type="revolute",
        position=[0.0, 1.0, 0.0],
    )
    pyrosim.Send_Cube(name="Link4", pos=[0, 0.5, 0], size=[1, 1, 1])

    # Typo fix: 'osition' -> 'position'
    pyrosim.Send_Joint(
        name="Link4_Link5",
        parent="Link4",
        child="Link5",
        type="revolute",
        position=[0.0, 0.5, -0.5],
    )
    pyrosim.Send_Cube(name="Link5", pos=[0, 0, -0.5], size=[1, 1, 1])

    pyrosim.Send_Joint(
        name="Link5_Link6",
        parent="Link5",
        child="Link6",
        type="revolute",
        position=[0.0, 0.0, -1.0],
    )
    pyrosim.Send_Cube(name="Link6", pos=[0, 0, -0.5], size=[1, 1, 1])

    pyrosim.End()


def create_three_link_two_joint():
    """
    Creates a 3-link robot with two revolute joints.
    """
    pyrosim.Start_URDF("data/three_link.urdf")

    pyrosim.Send_Cube(
        name="Torso",
        pos=[1.5, 0.0, 1.5],
        size=[1, 1, 1]
    )

    # First joint: Torso -> BackLeg
    pyrosim.Send_Joint(
        name="Torso_BackLeg",
        parent="Torso",
        child="BackLeg",
        type="revolute",
        position=[1.0, 0.0, 0.5],
    )
    pyrosim.Send_Cube(
        name="BackLeg",
        pos=[-0.5, 0.0, 0],
        size=[1, 1, 1]
    )

    # Second joint: Torso -> FrontLeg
    pyrosim.Send_Joint(
        name="Torso_FrontLeg",
        parent="Torso",
        child="FrontLeg",
        type="revolute",
        position=[2.0, 0.0, 0.5],
    )
    pyrosim.Send_Cube(
        name="FrontLeg",
        pos=[0.5, 0.0, 0],
        size=[1, 1, 1]
    )

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

    # First joint: Torso -> BackLeg
    pyrosim.Send_Joint(
        name="Torso_BackLeg",
        parent="Torso",
        child="BackLeg",
        type="revolute",
        position=[1.0, 0.0, 0.5],
    )
    pyrosim.Send_Cube(
        name="BackLeg",
        pos=[-0.5, 0.0, 0],
        size=[1, 1, 1]
    )

    # Second joint: Torso -> FrontLeg
    pyrosim.Send_Joint(
        name="Torso_FrontLeg",
        parent="Torso",
        child="FrontLeg",
        type="revolute",
        position=[2.0, 0.0, 0.5],
    )
    pyrosim.Send_Cube(
        name="FrontLeg",
        pos=[0.5, 0.0, 0],
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
    main()
