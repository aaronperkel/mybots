"""
motor.py
Defines the Motor class, which controls a single revolute joint in the robot.
It stores parameters for motion and commands the joint each timestep.
"""

import constants as c
import pybullet as p
from pyrosim import pyrosim

class Motor:
    """
    Controls a single revolute joint in the robot.
    This class is responsible for applying forces or setting target positions
    for a specific joint based on the neural network's output.
    """
    def __init__(self, joint_name):
        """
        Initializes the Motor.

        Args:
            joint_name (str): The name of the joint this motor controls,
                              as defined in the robot's URDF file.
        """
        self.joint_name = joint_name
        # self.robot_id is set in set_value when the motor acts.

    def set_value(self, desired_angle, robot_id):
        """
        Sets the target angle for the motor, commanding it to move.

        Args:
            desired_angle (float): The desired target angle for the joint,
                                   typically determined by a motor neuron.
            robot_id (int): The unique ID of the robot in the PyBullet simulation.
        """
        self.robot_id = robot_id  # Store robot_id for use in pyrosim call
        target_position = desired_angle

        pyrosim.Set_Motor_For_Joint(
                bodyIndex=self.robot_id,
                jointName=self.joint_name,
                controlMode=p.POSITION_CONTROL, # Control joint by setting target position
                targetPosition=target_position,
                maxForce=c.MAX_FORCE # Maximum force the motor can apply
            )