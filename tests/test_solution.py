import unittest
from unittest.mock import patch, mock_open, MagicMock, call
import sys
import os
import numpy as np

# Adjust path to import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.solution import Solution
import src.constants as c

class TestSolution(unittest.TestCase):
    """
    Tests for the Solution class in src.solution.py.
    """

    def setUp(self):
        """
        Common setup for tests. Initializes a Solution instance.
        """
        self.solution_id = 42
        self.solution = Solution(self.solution_id)

    def test_solution_initialization(self):
        """
        Test that __init__ correctly sets the ID and initializes weights and fitness.
        """
        self.assertEqual(self.solution.my_id, self.solution_id, "Solution ID should be set correctly.")
        self.assertIsInstance(self.solution.weights, np.ndarray, "Weights should be a numpy array.")
        self.assertEqual(self.solution.weights.shape, (c.NUM_SENSOR_NEURONS, c.NUM_MOTOR_NEURONS),
                         "Weights array shape is incorrect.")
        self.assertTrue(np.all(self.solution.weights >= -1) and np.all(self.solution.weights <= 1),
                        "Weights should be initialized between -1 and 1.")
        self.assertIsNone(self.solution.fitness, "Fitness should be initialized to None.")

    @patch('src.solution.subprocess.Popen')
    @patch.object(Solution, 'create_world', MagicMock())
    @patch.object(Solution, 'create_body', MagicMock())
    @patch.object(Solution, 'create_brain', MagicMock())
    def test_start_simulation(self, mock_subprocess_popen):
        """
        Test that start_simulation calls create methods and subprocess.Popen with correct arguments.
        """
        direct_or_gui = "GUI"
        self.solution.start_simulation(direct_or_gui)

        self.solution.create_world.assert_called_once()
        self.solution.create_body.assert_called_once()
        self.solution.create_brain.assert_called_once()

        expected_command = [
            "python", "./src/simulate.py",
            direct_or_gui, str(self.solution.my_id)
        ]
        mock_subprocess_popen.assert_called_once_with(
            expected_command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    @patch('src.solution.os.remove')
    @patch('src.solution.open', new_callable=mock_open, read_data="0.75")
    @patch('src.solution.os.path.exists')
    @patch('src.solution.time.sleep', MagicMock()) # Mock time.sleep to speed up test
    def test_wait_for_simulation_to_end_reads_fitness(self, mock_path_exists, mock_file_open, mock_os_remove):
        """
        Test that wait_for_simulation_to_end reads fitness from file and removes it.
        """
        # Simulate file appearing after a few checks
        mock_path_exists.side_effect = [False, False, True] 
        
        self.solution.wait_for_simulation_to_end()

        fitness_file_path = f'./src/data/fitness{self.solution.my_id}.txt'
        
        # Check os.path.exists calls
        expected_exists_calls = [call(fitness_file_path)] * 3
        self.assertEqual(mock_path_exists.call_args_list, expected_exists_calls)
        
        # Check file open
        mock_file_open.assert_called_once_with(fitness_file_path, 'r')
        self.assertEqual(self.solution.fitness, 0.75)
        
        # Check file removal
        mock_os_remove.assert_called_once_with(fitness_file_path)

    @patch.object(Solution, 'start_simulation')
    @patch.object(Solution, 'wait_for_simulation_to_end')
    def test_evaluate(self, mock_wait_for_simulation, mock_start_simulation):
        """
        Test that evaluate calls start_simulation and wait_for_simulation_to_end.
        """
        direct_or_gui_mode = "DIRECT"
        self.solution.evaluate(direct_or_gui_mode)
        mock_start_simulation.assert_called_once_with(direct_or_gui_mode)
        mock_wait_for_simulation_to_end.assert_called_once()

    def test_mutate(self):
        """
        Test that mutate changes at least one weight in self.weights
        and keeps it within the [-1, 1] range.
        """
        initial_weights = np.copy(self.solution.weights)
        self.solution.mutate()
        mutated_weights = self.solution.weights

        self.assertEqual(initial_weights.shape, mutated_weights.shape, "Weights shape should not change after mutation.")
        # Check if at least one weight changed (probabilistic, but highly likely for non-zero matrix)
        self.assertFalse(np.array_equal(initial_weights, mutated_weights), "Mutation should change at least one weight.")
        self.assertTrue(np.all(mutated_weights >= -1) and np.all(mutated_weights <= 1),
                        "Mutated weights should be within [-1, 1] range.")

    def test_set_id(self):
        """
        Test that set_id updates the solution's my_id attribute.
        """
        new_id = 101
        self.solution.set_id(new_id)
        self.assertEqual(self.solution.my_id, new_id, "set_id should update my_id.")

    @patch('src.solution.pyrosim')
    @patch('src.solution.os.path.exists')
    @patch('src.solution.os.makedirs')
    def test_create_world(self, mock_makedirs, mock_path_exists, mock_pyrosim):
        """
        Test create_world ensures directory exists and calls pyrosim SDF functions.
        """
        mock_path_exists.return_value = False # Simulate data directory does not exist
        
        self.solution.create_world()

        data_dir = "./src/data"
        mock_path_exists.assert_called_once_with(data_dir)
        mock_makedirs.assert_called_once_with(data_dir)
        
        world_sdf_path = os.path.join(data_dir, "world.sdf")
        mock_pyrosim.Start_SDF.assert_called_once_with(world_sdf_path)
        mock_pyrosim.Send_Cube.assert_called_once() # Check at least one cube is sent
        mock_pyrosim.End.assert_called_once()

    @patch('src.solution.pyrosim')
    @patch('src.solution.os.path.join', side_effect=lambda *args: "/".join(args)) # Simple mock for os.path.join
    def test_create_body(self, mock_os_path_join, mock_pyrosim):
        """
        Test create_body calls pyrosim URDF functions.
        """
        self.solution.create_body()
        
        body_urdf_path = "./src/data/body.urdf"
        mock_pyrosim.Start_URDF.assert_called_once_with(body_urdf_path)
        # Check that Send_Cube and Send_Joint are called multiple times (at least once for Torso)
        self.assertTrue(mock_pyrosim.Send_Cube.call_count > 0)
        self.assertTrue(mock_pyrosim.Send_Joint.call_count > 0)
        mock_pyrosim.End.assert_called_once()

    @patch('src.solution.pyrosim')
    @patch('src.solution.os.path.join', side_effect=lambda *args: "/".join(args))
    def test_create_brain(self, mock_os_path_join, mock_pyrosim):
        """
        Test create_brain calls pyrosim NeuralNetwork functions.
        """
        self.solution.create_brain()

        brain_nndf_path = f"./src/data/brain{self.solution.my_id}.nndf"
        mock_pyrosim.Start_NeuralNetwork.assert_called_once_with(brain_nndf_path)
        
        # Check that sensor and motor neurons are sent
        self.assertTrue(mock_pyrosim.Send_Sensor_Neuron.call_count == c.NUM_SENSOR_NEURONS)
        self.assertTrue(mock_pyrosim.Send_Motor_Neuron.call_count == c.NUM_MOTOR_NEURONS)
        
        # Check that synapses are sent
        expected_synapse_calls = c.NUM_SENSOR_NEURONS * c.NUM_MOTOR_NEURONS
        self.assertTrue(mock_pyrosim.Send_Synapse.call_count == expected_synapse_calls)
        mock_pyrosim.End.assert_called_once()

if __name__ == '__main__':
    unittest.main()
