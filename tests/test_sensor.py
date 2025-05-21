import unittest
from unittest.mock import patch, mock_open, MagicMock
import sys
import os
import numpy as np

# Adjust path to import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.sensor import Sensor
import src.constants as c

class TestSensor(unittest.TestCase):
    """
    Tests for the Sensor class in src.sensor.py.
    """

    def setUp(self):
        """
        Common setup for tests. Initializes a Sensor instance.
        """
        self.link_name = "TestLink"
        self.sensor = Sensor(self.link_name)

    def test_sensor_initialization(self):
        """
        Test that __init__ correctly stores link_name and initializes values array.
        """
        self.assertEqual(self.sensor.link_name, self.link_name, "Sensor should store the link_name.")
        self.assertIsInstance(self.sensor.values, np.ndarray, "Sensor values should be a numpy array.")
        self.assertEqual(len(self.sensor.values), c.STEPS, f"Sensor values array should have length {c.STEPS}.")
        self.assertTrue(np.all(self.sensor.values == 0), "Sensor values should be initialized to zeros.")

    @patch('src.sensor.pyrosim') # Mocking the pyrosim module used within sensor.py
    def test_get_value_stores_sensor_reading(self, mock_pyrosim_module):
        """
        Test that get_value calls pyrosim.Get_Touch_Sensor_Value_For_Link
        and stores the returned value in the correct time step.
        """
        mock_touch_value = 0.75
        mock_pyrosim_module.Get_Touch_Sensor_Value_For_Link.return_value = mock_touch_value
        
        time_step = 5
        self.sensor.get_value(time_step)
        
        # Verify the pyrosim call
        mock_pyrosim_module.Get_Touch_Sensor_Value_For_Link.assert_called_once_with(self.link_name)
        
        # Verify the value was stored
        self.assertEqual(self.sensor.values[time_step], mock_touch_value,
                         "Sensor value was not stored correctly at the given time step.")

    @patch('src.sensor.np.save') # Mock numpy.save
    def test_save_values_calls_numpy_save_correctly(self, mock_numpy_save):
        """
        Test that save_values calls numpy.save with the correct file path and data.
        """
        # Populate some dummy values
        self.sensor.values = np.array([0.1, 0.2, 0.3] + [0.0]*(c.STEPS-3))
        
        self.sensor.save_values()
        
        expected_file_path = f'./src/data/{self.link_name}_sensor_values.npy'
        
        # Assert that np.save was called once
        mock_numpy_save.assert_called_once()
        
        # Check the arguments of the call
        # The first argument to assert_called_with is the first positional arg to np.save
        # The second is the second positional arg.
        args, _ = mock_numpy_save.call_args
        self.assertEqual(args[0], expected_file_path, "np.save called with incorrect file path.")
        np.testing.assert_array_equal(args[1], self.sensor.values, 
                                      "np.save called with incorrect data.")

if __name__ == '__main__':
    unittest.main()
