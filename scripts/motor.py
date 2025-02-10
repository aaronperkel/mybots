"""
motor.py
Defines the MOTOR class, which controls a single revolute joint in the robot.
It stores parameters for motion (amplitude, frequency, etc.) and commands the joint each timestep.
"""

import constants as c
import numpy as np
import pybullet as p
from pyrosim import pyrosim

class MOTOR:
    def __init__(self, joint_name):
        self.joint_name = joint_name
        self.Prepare_To_Act()

    def Prepare_To_Act(self):
        self.AMPLITUDE = c.AMPLITUDE_BL
        self.FREQUENCY = c.FREQUENCY_BL
        self.OFFSET = c.PHASE_OFFSET_BL

        i_vals = np.arange(c.STEPS)
        self.motor_values = self.AMPLITUDE * np.sin(2 * np.pi * self.FREQUENCY * i_vals / c.STEPS + self.OFFSET)

    def Set_Value(self, desiredAngle, robot_id):
        self.robot_id = robot_id
        target_position = desiredAngle

        pyrosim.Set_Motor_For_Joint(
                bodyIndex=self.robot_id,
                jointName=self.joint_name,
                controlMode=p.POSITION_CONTROL,
                targetPosition=target_position,
                maxForce=c.MAX_FORCE,
            )
        
    def Save_Values(self):
        np.save(f'data/{self.joint_name}_motor_values.npy', self.values)