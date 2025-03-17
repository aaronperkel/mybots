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
        """
        Creates a 3-link robot with two revolute joints.
        """
        pyrosim.Start_URDF("data/body.urdf")
        
        # Torso centered at (0,0,1)
        pyrosim.Send_Cube(
            name="Torso",
            pos=[0.0, 0.0, 1.0],
            size=[1, 1, 1]
        )
        
        # Back Leg (front/back leg: axis = "1 0 0")
        pyrosim.Send_Joint(
            name="Torso_BackLeg",
            parent="Torso",
            child="BackLeg",
            type="revolute",
            position=[0.0, -0.5, 1.0],
            jointAxis='1 0 0'
        )
        pyrosim.Send_Cube(
            name="BackLeg",
            pos=[0.0, -0.5, 0.0],
            size=[0.2, 1.0, 0.2]
        )
        
        pyrosim.Send_Joint(
            name="Torso_FrontLeg",
            parent="Torso",
            child="FrontLeg",
            type="revolute",
            position=[0.0, 0.5, 1.0],
            jointAxis='1 0 0'
        )


        pyrosim.Send_Cube(
            name="FrontLeg",
            pos=[0.0, 0.5, 0.0],
            size=[0.2, 1.0, 0.2]
        )
        
        # Left Leg (side leg: change joint axis to "1 0 0")
        pyrosim.Send_Joint(
            name="Torso_LeftLeg",
            parent="Torso",
            child="LeftLeg",
            type="revolute",
            position=[-0.5, 0.0, 1.0],
            jointAxis='0 1 0' 
        )
        pyrosim.Send_Cube(
            name="LeftLeg",
            pos=[-0.5, 0.0, 0.0],  # This is relative to the joint
            size=[1.0, 0.2, 0.2]
        )
        
        # Right Leg (side leg: change axis to "0 1 0")
        pyrosim.Send_Joint(
            name="Torso_RightLeg",
            parent="Torso",
            child="RightLeg",
            type="revolute",
            position=[0.5, 0.0, 1.0],
            jointAxis='0 1 0'
        )
        pyrosim.Send_Cube(
            name="RightLeg",
            pos=[0.5, 0.0, 0.0],
            size=[1.0, 0.2, 0.2]
        )
        
        # Lower legs:
        # Front Lower Leg (attached to FrontLeg, use "1 0 0")
        pyrosim.Send_Joint(
            name="FrontLeg_FrontLowerLeg",
            parent="FrontLeg",
            child="FrontLowerLeg",
            type="revolute",
            position=[0.0, 1.0, 0.0],  # relative to FrontLeg
            jointAxis='1 0 0'
        )
        pyrosim.Send_Cube(
            name="FrontLowerLeg",
            pos=[0.0, 0.0, -0.5],
            size=[0.2, 0.2, 1.0]
        )
        
        pyrosim.Send_Joint(
            name="BackLeg_BackLowerLeg",
            parent="BackLeg",
            child="BackLowerLeg",
            type="revolute",
            position=[0.0, -1.0, 0.0],
            jointAxis='1 0 0'
        )
        # Adjust the position of the BackLowerLeg so its top aligns with the joint:
        pyrosim.Send_Cube(
            name="BackLowerLeg",
            pos=[0.0, 0.0, -0.5],
            size=[0.2, 0.2, 1.0]
        )
        
        # Left Lower Leg (attached to LeftLeg, use "0 1 0")
        pyrosim.Send_Joint(
            name="LeftLeg_LeftLowerLeg",
            parent="LeftLeg",
            child="LeftLowerLeg",
            type="revolute",
            position=[-1.0, 0.0, 0.0],
            jointAxis='0 1 0'
        )
        pyrosim.Send_Cube(
            name="LeftLowerLeg",
            pos=[0.0, 0.0, -0.5],
            size=[0.2, 0.2, 1.0]
        )

        # Left Lower Leg (attached to LeftLeg, use "0 1 0")
        pyrosim.Send_Joint(
            name="RightLeg_RightLowerLeg",
            parent="RightLeg",
            child="RightLowerLeg",
            type="revolute",
            position=[1.0, 0.0, 0.0],
            jointAxis='0 1 0'
        )
        pyrosim.Send_Cube(
            name="RightLowerLeg",
            pos=[0.0, 0.0, -0.5],
            size=[0.2, 0.2, 1.0]
        )
        
        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"data/brain{self.myID}.nndf")
        # Sensor neurons
        # pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        # pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
        # pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")
        # pyrosim.Send_Sensor_Neuron(name=3, linkName="LeftLeg")
        # pyrosim.Send_Sensor_Neuron(name=4, linkName="RightLeg")
        pyrosim.Send_Sensor_Neuron(name=0, linkName="FrontLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="LeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=3, linkName="RightLowerLeg")
        # Motor neurons (joints)
        pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=5, jointName="Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron(name=6, jointName="Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron(name=7, jointName="Torso_RightLeg")
        pyrosim.Send_Motor_Neuron(name=8, jointName="FrontLeg_FrontLowerLeg")
        pyrosim.Send_Motor_Neuron(name=9, jointName="BackLeg_BackLowerLeg")
        pyrosim.Send_Motor_Neuron(name=10, jointName="LeftLeg_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron(name=11, jointName="RightLeg_RightLowerLeg")

        for currentRow in range(c.NUM_SENSOR_NEURONS):
            for currentColumn in range(c.NUM_MOTOR_NEURONS):
                weight = self.weights[currentRow % self.weights.shape[0]][currentColumn % self.weights.shape[1]]
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, 
                                  targetNeuronName=currentColumn+c.NUM_SENSOR_NEURONS, 
                                  weight=weight)
        pyrosim.End()

    def Mutate(self):
        rand_row = random.randint(0, c.NUM_SENSOR_NEURONS - 1)
        rand_col = random.randint(0, c.NUM_MOTOR_NEURONS - 1)
        self.weights[rand_row,rand_col] = random.random() * 2 - 1

    def Set_ID(self, newID):
        self.myID = newID