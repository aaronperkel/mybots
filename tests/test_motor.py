import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Adjust path to import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.motor import Motor
import src.constants as c 
# We need pybullet for p.POSITION_CONTROL, but we don't want to start a simulation
# We can mock the pybullet module if it's not essential for simple constant values
try:
    import pybullet as p
except ImportError:
    # If pybullet is not installed (e.g. in a CI environment without it),
    # create a mock for p.POSITION_CONTROL
    p = MagicMock()
    p.POSITION_CONTROL = 0 # Assign a dummy value


class TestMotor(unittest.TestCase):
    """
    Tests for the Motor class in src.motor.py.
    """

    def test_motor_initialization_stores_joint_name(self):
        """
        Test that the __init__ method correctly stores the joint_name.
        """
        joint_name = "TestJoint"
        motor = Motor(joint_name)
        self.assertEqual(motor.joint_name, joint_name, "Motor should store the joint_name.")

    @patch('src.motor.pyrosim') # Mocking the pyrosim module used within motor.py
    def test_set_value_calls_pyrosim_set_motor_for_joint(self, mock_pyrosim_module):
        """
        Test that set_value calls pyrosim.Set_Motor_For_Joint with correct arguments.
        """
        joint_name = "TestJoint"
        motor = Motor(joint_name)
        
        robot_id = 0
        desired_angle = 0.5
        
        # Call the method to test
        motor.set_value(desired_angle, robot_id)
        
        # Assert that pyrosim.Set_Motor_For_Joint was called once
        mock_pyrosim_module.Set_Motor_For_Joint.assert_called_once()
        
        # Get the arguments it was called with
        # The first way is to get the call_args attribute
        # args, kwargs = mock_pyrosim_module.Set_Motor_For_Joint.call_args
        # Or, more directly if you know the signature (keyword args here)
        mock_pyrosim_module.Set_Motor_For_Joint.assert_called_once_with(
            bodyIndex=robot_id,
            jointName=joint_name,
            controlMode=p.POSITION_CONTROL, # Assuming p.POSITION_CONTROL is a known constant
            targetPosition=desired_angle,
            maxForce=c.MAX_FORCE
        )
        
        # Also test if robot_id is stored in the motor instance
        self.assertEqual(motor.robot_id, robot_id, "Motor should store robot_id after set_value.")

if __name__ == '__main__':
    unittest.main()
