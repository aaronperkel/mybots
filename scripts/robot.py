"""
robot.py
Defines the ROBOT class, which aggregates all the robot's sensors and motors.
It loads the robot's URDF, prepares the sensors and motors, and coordinates sensing/acting.
"""

import pybullet as p
from pyrosim import pyrosim
from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK

class ROBOT:
    def __init__(self):
        self.robot_id = p.loadURDF("data/body.urdf")
        pyrosim.Prepare_To_Simulate(self.robot_id)
        self.nn = NEURAL_NETWORK("data/brain.nndf")
        self.Prepare_To_Sense()
        self.Prepare_To_Act()

    def Prepare_To_Sense(self):
        self.sensors = {}
        for link_name in pyrosim.linkNamesToIndices:
            self.sensors[link_name] = SENSOR(link_name)

    def Sense(self, t):
        for _, sensor_obj in self.sensors.items():
            sensor_obj.Get_Value(t)

    def Prepare_To_Act(self):
        self.motors = {}
        for joint_name in pyrosim.jointNamesToIndices:
            self.motors[joint_name] = MOTOR(joint_name)

    def Act(self, t):
        for neuron_name in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuron_name):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuron_name)
                desiredAngle = self.nn.Get_Value_Of(neuron_name)
                print(desiredAngle)

        # for _, motor_obj in self.motors.items():
        #     motor_obj.Set_Value(t, self.robot_id)

    def Think(self):
        self.nn.Update()
        self.nn.Print()
