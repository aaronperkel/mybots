"""
solution.py
"""

import numpy as np
from pyrosim import pyrosim
import os

class SOLUTION:
    def __init__(self):
        self.weights = np.random.rand(3, 2)
        self.weights = self.weights * 2 - 1

    def Evaluate(self):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system("python scripts/simulate.py")
        with open('data/fitness.txt', 'r') as f:
            self.fitness = f.read()
            self.fitness = float(self.fitness)
            f.close()

    def Create_World(self):
        pyrosim.Start_SDF("data/world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[-4, 4, 0.5], size=[1, 1, 1])
        pyrosim.End()

    def Create_Body(self):
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

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("data/brain.nndf")
        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")
        pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")

        for currentRow in range(3):
            for currentColumn in range(2):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, 
                                     targetNeuronName=currentColumn+3, 
                                     weight=self.weights[currentRow][currentColumn])
        pyrosim.End()