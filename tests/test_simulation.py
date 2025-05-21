import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Adjust path to import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.simulation import Simulation
import src.constants as c

# Mock pybullet at the module level if its methods are called globally or at import time
# For Simulation, p.connect is called in __init__
# We also need p.GUI, p.DIRECT, p.COV_ENABLE_GUI, p.setAdditionalSearchPath, p.setGravity, p.stepSimulation, p.disconnect, p.isConnected
# Mocking the entire pybullet module
mock_p = MagicMock()
sys.modules['pybullet'] = mock_p
sys.modules['pybullet_data'] = MagicMock() # If pybullet_data.getDataPath() is used

class TestSimulation(unittest.TestCase):
    """
    Tests for the Simulation class in src.simulation.py.
    """

    @patch('src.simulation.Robot')  # Mock the Robot class
    @patch('src.simulation.World')  # Mock the World class
    def setUp(self, mock_world_class, mock_robot_class):
        """
        Set up for Simulation tests. This is called before each test method.
        """
        # Reset global pybullet mock calls for each test
        mock_p.reset_mock()

        self.direct_or_gui_direct = "DIRECT"
        self.direct_or_gui_gui = "GUI"
        self.solution_id = 123

        # Configure mock return values for World and Robot instances
        self.mock_world_instance = mock_world_class.return_value
        self.mock_robot_instance = mock_robot_class.return_value
        
        # Store mocks for use in tests
        self.mock_robot_class = mock_robot_class
        self.mock_world_class = mock_world_class


    def test_simulation_initialization_direct_mode(self):
        """
        Test __init__ in 'DIRECT' mode.
        """
        sim = Simulation(self.direct_or_gui_direct, self.solution_id)

        mock_p.connect.assert_called_once_with(mock_p.DIRECT)
        mock_p.configureDebugVisualizer.assert_not_called() # Should not be called in DIRECT
        mock_p.setAdditionalSearchPath.assert_called_once() # Assuming pybullet_data.getDataPath() is resolved by mock
        mock_p.setGravity.assert_called_once_with(c.GRAV_X, c.GRAV_Y, c.GRAV_Z)
        
        self.mock_world_class.assert_called_once()
        self.mock_robot_class.assert_called_once_with(self.solution_id)
        self.assertEqual(sim.world, self.mock_world_instance)
        self.assertEqual(sim.robot, self.mock_robot_instance)
        self.assertEqual(sim.physics_client, mock_p.connect.return_value)


    def test_simulation_initialization_gui_mode(self):
        """
        Test __init__ in 'GUI' mode.
        """
        sim = Simulation(self.direct_or_gui_gui, self.solution_id)

        mock_p.connect.assert_called_once_with(mock_p.GUI)
        mock_p.configureDebugVisualizer.assert_called_once_with(mock_p.COV_ENABLE_GUI, 0)
        # Other calls are the same as DIRECT mode
        mock_p.setAdditionalSearchPath.assert_called_once()
        mock_p.setGravity.assert_called_once_with(c.GRAV_X, c.GRAV_Y, c.GRAV_Z)
        self.mock_world_class.assert_called_once()
        self.mock_robot_class.assert_called_once_with(self.solution_id)

    @patch('src.simulation.time.sleep') # Mock time.sleep
    def test_run_simulation_loop_direct_mode(self, mock_time_sleep):
        """
        Test the run method in 'DIRECT' mode.
        Robot methods should be called, sleep should not.
        """
        sim = Simulation(self.direct_or_gui_direct, self.solution_id)
        # Replace the robot instance with its mock for this test if not already done by setUp
        sim.robot = self.mock_robot_instance 

        sim.run()

        self.assertEqual(mock_p.stepSimulation.call_count, c.STEPS)
        self.assertEqual(sim.robot.sense.call_count, c.STEPS)
        self.assertEqual(sim.robot.think.call_count, c.STEPS)
        self.assertEqual(sim.robot.act.call_count, c.STEPS)
        
        # Check arguments for one of the calls to sense and act
        sim.robot.sense.assert_any_call(0) # Example for the first step
        sim.robot.sense.assert_any_call(c.STEPS - 1) # Example for the last step
        sim.robot.act.assert_any_call(0)
        sim.robot.act.assert_any_call(c.STEPS - 1)

        mock_time_sleep.assert_not_called() # sleep should not be called in DIRECT mode

    @patch('src.simulation.time.sleep') # Mock time.sleep
    def test_run_simulation_loop_gui_mode(self, mock_time_sleep):
        """
        Test the run method in 'GUI' mode.
        Robot methods and time.sleep should be called.
        """
        sim = Simulation(self.direct_or_gui_gui, self.solution_id)
        sim.robot = self.mock_robot_instance

        sim.run()

        self.assertEqual(mock_p.stepSimulation.call_count, c.STEPS)
        self.assertEqual(sim.robot.sense.call_count, c.STEPS)
        self.assertEqual(sim.robot.think.call_count, c.STEPS)
        self.assertEqual(sim.robot.act.call_count, c.STEPS)
        
        self.assertEqual(mock_time_sleep.call_count, c.STEPS)
        mock_time_sleep.assert_called_with(c.SLEEP_TIME) # Check it's called with the constant

    def test_get_fitness(self):
        """
        Test that get_fitness calls robot.get_fitness.
        """
        sim = Simulation(self.direct_or_gui_direct, self.solution_id)
        sim.robot = self.mock_robot_instance # Ensure we're using the mocked robot

        sim.get_fitness()
        sim.robot.get_fitness.assert_called_once()

    def test_del_disconnects_pybullet(self):
        """
        Test that the __del__ method disconnects from PyBullet if connected.
        """
        sim = Simulation(self.direct_or_gui_direct, self.solution_id)
        physics_client_id = sim.physics_client
        
        # Simulate being connected
        mock_p.isConnected.return_value = True
        
        # Call __del__ explicitly for testing (not typical, but useful here)
        sim.__del__()
        
        mock_p.isConnected.assert_called_once_with(physics_client_id)
        mock_p.disconnect.assert_called_once_with(physics_client_id)

    def test_del_does_not_disconnect_if_not_connected(self):
        """
        Test that __del__ does not call disconnect if not connected.
        """
        sim = Simulation(self.direct_or_gui_direct, self.solution_id)
        
        # Simulate not being connected
        mock_p.isConnected.return_value = False
        
        sim.__del__()
        
        mock_p.isConnected.assert_called_once_with(sim.physics_client)
        mock_p.disconnect.assert_not_called()


if __name__ == '__main__':
    unittest.main()
