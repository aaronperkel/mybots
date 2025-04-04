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
        os.system(f"python ./src/simulate.py {directOrGUI} {self.myID} &>/dev/null &")

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists(f'./src/data/fitness{self.myID}.txt'):
            time.sleep(0.01)
        with open(f'./src/data/fitness{self.myID}.txt', 'r') as f:
            self.fitness = f.read()
            self.fitness = float(self.fitness)
            f.close()
        os.system(f'rm ./src/data/fitness{self.myID}.txt')


    def Create_World(self):
        if not os.path.exists("./src/data"):
            os.makedirs("./src/data")
        pyrosim.Start_SDF("./src/data/world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[-4, 4, 0.5], size=[1, 1, 1])
        pyrosim.End()


    def Create_Body(self):
        swarm_size = 3  # number of robots in the swarm
        for i in range(swarm_size):
            # Define an offset for this robot; here we offset only in x.
            offset = [i * 3.0, 0.0, 0.0]
            # Generate a unique filename for each URDF
            urdf_filename = f"./src/data/body_{i}.urdf"
            pyrosim.Start_URDF(urdf_filename)
            
            # Torso (position offset added)
            torso_pos = [0.0 + offset[0], 0.0 + offset[1], 1.0 + offset[2]]
            pyrosim.Send_Cube(
                name="Torso",
                pos=torso_pos,
                size=[1, 1, 1]
            )
            
            # Back Leg
            backleg_joint_pos = [0.0 + offset[0], -0.5 + offset[1], 1.0 + offset[2]]
            pyrosim.Send_Joint(
                name="Torso_BackLeg",
                parent="Torso",
                child="BackLeg",
                type="revolute",
                position=backleg_joint_pos,
                jointAxis='1 0 0'
            )
            backleg_pos = [0.0 + offset[0], -0.5 + offset[1], 0.0 + offset[2]]
            pyrosim.Send_Cube(
                name="BackLeg",
                pos=backleg_pos,
                size=[0.2, 1.0, 0.2]
            )
            
            # Front Leg
            frontleg_joint_pos = [0.0 + offset[0], 0.5 + offset[1], 1.0 + offset[2]]
            pyrosim.Send_Joint(
                name="Torso_FrontLeg",
                parent="Torso",
                child="FrontLeg",
                type="revolute",
                position=frontleg_joint_pos,
                jointAxis='1 0 0'
            )
            frontleg_pos = [0.0 + offset[0], 0.5 + offset[1], 0.0 + offset[2]]
            pyrosim.Send_Cube(
                name="FrontLeg",
                pos=frontleg_pos,
                size=[0.2, 1.0, 0.2]
            )
            
            # Left Leg
            leftleg_joint_pos = [-0.5 + offset[0], 0.0 + offset[1], 1.0 + offset[2]]
            pyrosim.Send_Joint(
                name="Torso_LeftLeg",
                parent="Torso",
                child="LeftLeg",
                type="revolute",
                position=leftleg_joint_pos,
                jointAxis='0 1 0'
            )
            leftleg_pos = [-0.5 + offset[0], 0.0 + offset[1], 0.0 + offset[2]]
            pyrosim.Send_Cube(
                name="LeftLeg",
                pos=leftleg_pos,
                size=[1.0, 0.2, 0.2]
            )
            
            # Right Leg
            rightleg_joint_pos = [0.5 + offset[0], 0.0 + offset[1], 1.0 + offset[2]]
            pyrosim.Send_Joint(
                name="Torso_RightLeg",
                parent="Torso",
                child="RightLeg",
                type="revolute",
                position=rightleg_joint_pos,
                jointAxis='0 1 0'
            )
            rightleg_pos = [0.5 + offset[0], 0.0 + offset[1], 0.0 + offset[2]]
            pyrosim.Send_Cube(
                name="RightLeg",
                pos=rightleg_pos,
                size=[1.0, 0.2, 0.2]
            )
            
            # Front Lower Leg (attached to FrontLeg)
            frontlowerleg_joint_pos = [0.0 + offset[0], 1.0 + offset[1], 0.0 + offset[2]]
            pyrosim.Send_Joint(
                name="FrontLeg_FrontLowerLeg",
                parent="FrontLeg",
                child="FrontLowerLeg",
                type="revolute",
                position=frontlowerleg_joint_pos,
                jointAxis='1 0 0'
            )
            frontlowerleg_pos = [0.0 + offset[0], 0.0 + offset[1], -0.5 + offset[2]]
            pyrosim.Send_Cube(
                name="FrontLowerLeg",
                pos=frontlowerleg_pos,
                size=[0.2, 0.2, 1.0]
            )
            
            # Back Lower Leg (attached to BackLeg)
            backlowerleg_joint_pos = [0.0 + offset[0], -1.0 + offset[1], 0.0 + offset[2]]
            pyrosim.Send_Joint(
                name="BackLeg_BackLowerLeg",
                parent="BackLeg",
                child="BackLowerLeg",
                type="revolute",
                position=backlowerleg_joint_pos,
                jointAxis='1 0 0'
            )
            backlowerleg_pos = [0.0 + offset[0], 0.0 + offset[1], -0.5 + offset[2]]
            pyrosim.Send_Cube(
                name="BackLowerLeg",
                pos=backlowerleg_pos,
                size=[0.2, 0.2, 1.0]
            )
            
            # Left Lower Leg (attached to LeftLeg)
            leftlowerleg_joint_pos = [-1.0 + offset[0], 0.0 + offset[1], 0.0 + offset[2]]
            pyrosim.Send_Joint(
                name="LeftLeg_LeftLowerLeg",
                parent="LeftLeg",
                child="LeftLowerLeg",
                type="revolute",
                position=leftlowerleg_joint_pos,
                jointAxis='0 1 0'
            )
            leftlowerleg_pos = [0.0 + offset[0], 0.0 + offset[1], -0.5 + offset[2]]
            pyrosim.Send_Cube(
                name="LeftLowerLeg",
                pos=leftlowerleg_pos,
                size=[0.2, 0.2, 1.0]
            )
            
            # Right Lower Leg (attached to RightLeg)
            rightlowerleg_joint_pos = [1.0 + offset[0], 0.0 + offset[1], 0.0 + offset[2]]
            pyrosim.Send_Joint(
                name="RightLeg_RightLowerLeg",
                parent="RightLeg",
                child="RightLowerLeg",
                type="revolute",
                position=rightlowerleg_joint_pos,
                jointAxis='0 1 0'
            )
            rightlowerleg_pos = [0.0 + offset[0], 0.0 + offset[1], -0.5 + offset[2]]
            pyrosim.Send_Cube(
                name="RightLowerLeg",
                pos=rightlowerleg_pos,
                size=[0.2, 0.2, 1.0]
            )
            
            pyrosim.End()


    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"./src/data/brain{self.myID}.nndf")
        # Sensor neurons
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
        self.weights[rand_row,rand_col] = (random.random() * 2) - 1

    def Set_ID(self, newID):
        self.myID = newID