"""
solution.py
"""

import numpy as np
from pyrosim import pyrosim
import os
import random
import time
import constants as c

class SOLUTION:
    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.weights = np.random.rand(c.NUM_SENSOR_NEURONS, c.NUM_MOTOR_NEURONS)
        self.weights = self.weights * 2 - 1

    def Evaluate(self, directOrGUI='DIRECT'):
        self.Start_Simulation(directOrGUI)
        self.Wait_For_Simulation_To_End()

    def Start_Simulation(self, directOrGUI='DIRECT'):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system(f"python scripts/simulate.py {directOrGUI} {self.myID} &>/dev/null &")

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists(f'data/fitness{self.myID}.txt'):
            time.sleep(0.01)
        with open(f'data/fitness{self.myID}.txt', 'r') as f:
            self.fitness = f.read()
            self.fitness = float(self.fitness)
            f.close()
        os.system(f'rm data/fitness{self.myID}.txt')


    def Create_World(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        pyrosim.Start_SDF("data/world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[-4, 4, 0.5], size=[1, 1, 1])
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("data/body.urdf")

        pyrosim.Send_Cube(
            name="Torso",
            pos=[0.0, 0.0, 1.0],
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
            position=[0, 0.5, 1.0],
        )
        pyrosim.Send_Cube(
            name="FrontLeg",
            pos=[0.5, 0.5, 0],
            size=[0.2, 1.0, 0.2]
        )

        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"data/brain{self.myID}.nndf")
        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")
        pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")

        for currentRow in range(c.NUM_SENSOR_NEURONS):
            for currentColumn in range(c.NUM_MOTOR_NEURONS):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, 
                                     targetNeuronName=currentColumn+3, 
                                     weight=self.weights[currentRow][currentColumn])
        pyrosim.End()

    def Mutate(self):
        rand_row = random.randint(c.NUM_SENSOR_NEURONS)
        rand_col = random.randint(c.NUM_MOTOR_NEURONS)
        self.weights[rand_row,rand_col] = random.random() * 2 - 1

    def Set_ID(self, newID):
        self.myID = newID