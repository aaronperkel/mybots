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