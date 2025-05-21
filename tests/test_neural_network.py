import unittest
from unittest.mock import patch, mock_open, MagicMock, call
import sys
import os

# Adjust path to import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))) # Go up to root then src

from pyrosim.neuralNetwork import NeuralNetwork
from pyrosim.neuron import Neuron # Needed for spec and type checks
from pyrosim.synapse import Synapse # Needed for spec and type checks

class TestNeuralNetwork(unittest.TestCase):
    """
    Tests for the NeuralNetwork class in src.pyrosim.neuralNetwork.py.
    """

    def test_initialization_empty_file(self):
        """
        Test that NeuralNetwork initializes with empty neurons and synapses
        when given an empty NNDF file.
        """
        nndf_content = ""
        with patch("builtins.open", mock_open(read_data=nndf_content)) as mock_file:
            nn = NeuralNetwork("dummy.nndf")
            mock_file.assert_called_once_with("dummy.nndf", "r")
            self.assertEqual(len(nn.neurons), 0)
            self.assertEqual(len(nn.synapses), 0)

    @patch('pyrosim.neuralNetwork.Neuron') # Mock Neuron class within neuralNetwork.py
    @patch('pyrosim.neuralNetwork.Synapse') # Mock Synapse class
    def test_initialization_parses_neurons_and_synapses(self, mock_synapse_class, mock_neuron_class):
        """
        Test that NeuralNetwork correctly parses neuron and synapse lines from NNDF
        and creates Neuron and Synapse objects.
        """
        nndf_content = (
            'neuron name="0" type="sensor" linkName="Leg0"\n'
            'neuron name="1" type="motor" jointName="Joint0"\n'
            'synapse sourceNeuronName="0" targetNeuronName="1" weight="0.5"\n'
        )
        
        # Mock instances that Neuron and Synapse constructors would return
        mock_sensor_neuron = MagicMock(spec=Neuron)
        mock_sensor_neuron.get_name.return_value = "0" # Crucial for dict key
        
        mock_motor_neuron = MagicMock(spec=Neuron)
        mock_motor_neuron.get_name.return_value = "1" # Crucial for dict key

        mock_synapse = MagicMock(spec=Synapse)
        mock_synapse.get_source_neuron_name.return_value = "0"
        mock_synapse.get_target_neuron_name.return_value = "1"

        # Make the mocked Neuron class return our specific neuron mocks
        # This requires knowing which line corresponds to which neuron if order matters
        # For simplicity, assume Neuron constructor is called in order of lines
        mock_neuron_class.side_effect = [mock_sensor_neuron, mock_motor_neuron]
        mock_synapse_class.return_value = mock_synapse

        with patch("builtins.open", mock_open(read_data=nndf_content)):
            nn = NeuralNetwork("dummy.nndf")

        # Check Neuron calls
        expected_neuron_calls = [
            call('neuron name="0" type="sensor" linkName="Leg0"\n'),
            call('neuron name="1" type="motor" jointName="Joint0"\n')
        ]
        mock_neuron_class.assert_has_calls(expected_neuron_calls)
        self.assertEqual(mock_neuron_class.call_count, 2)
        
        # Check Synapse call
        mock_synapse_class.assert_called_once_with('synapse sourceNeuronName="0" targetNeuronName="1" weight="0.5"\n')

        # Check internal storage
        self.assertEqual(len(nn.neurons), 2)
        self.assertIn("0", nn.neurons)
        self.assertIn("1", nn.neurons)
        self.assertEqual(nn.neurons["0"], mock_sensor_neuron)
        self.assertEqual(nn.neurons["1"], mock_motor_neuron)
        
        self.assertEqual(len(nn.synapses), 1)
        self.assertIn(("0", "1"), nn.synapses)
        self.assertEqual(nn.synapses[("0", "1")], mock_synapse)


    def test_get_neuron_names(self):
        """
        Test get_neuron_names returns the keys of the neurons dictionary.
        """
        nn = NeuralNetwork("dummy.nndf") # Assume empty for this direct test
        nn.neurons = {"n1": MagicMock(), "n2": MagicMock()}
        self.assertListEqual(sorted(list(nn.get_neuron_names())), sorted(["n1", "n2"]))

    def test_is_motor_neuron(self):
        """
        Test is_motor_neuron correctly queries the neuron object.
        """
        nn = NeuralNetwork("dummy.nndf")
        mock_neuron = MagicMock(spec=Neuron)
        nn.neurons = {"motor_n": mock_neuron}
        
        mock_neuron.is_motor_neuron.return_value = True
        self.assertTrue(nn.is_motor_neuron("motor_n"))
        mock_neuron.is_motor_neuron.assert_called_once()

        mock_neuron.reset_mock()
        mock_neuron.is_motor_neuron.return_value = False
        self.assertFalse(nn.is_motor_neuron("motor_n"))
        
        # Test non-existent neuron
        self.assertFalse(nn.is_motor_neuron("non_existent_n"))


    def test_get_motor_neurons_joint(self):
        """
        Test get_motor_neurons_joint correctly queries the neuron object.
        """
        nn = NeuralNetwork("dummy.nndf")
        mock_motor = MagicMock(spec=Neuron)
        mock_motor.is_motor_neuron.return_value = True
        mock_motor.get_joint_name.return_value = "TestJoint"
        nn.neurons = {"motor_n": mock_motor}

        self.assertEqual(nn.get_motor_neurons_joint("motor_n"), "TestJoint")
        mock_motor.get_joint_name.assert_called_once()

        # Test non-motor neuron
        mock_sensor = MagicMock(spec=Neuron)
        mock_sensor.is_motor_neuron.return_value = False
        nn.neurons["sensor_n"] = mock_sensor
        self.assertIsNone(nn.get_motor_neurons_joint("sensor_n"))
        
        # Test non-existent neuron
        self.assertIsNone(nn.get_motor_neurons_joint("non_existent_n"))


    def test_get_value_of(self):
        """
        Test get_value_of correctly queries the neuron object.
        """
        nn = NeuralNetwork("dummy.nndf")
        mock_neuron = MagicMock(spec=Neuron)
        mock_neuron.get_value.return_value = 0.99
        nn.neurons = {"n1": mock_neuron}

        self.assertEqual(nn.get_value_of("n1"), 0.99)
        mock_neuron.get_value.assert_called_once()
        
        # Test non-existent neuron
        self.assertIsNone(nn.get_value_of("non_existent_n"))

    def test_update(self):
        """
        Test that update calls the correct update methods on neurons.
        """
        nn = NeuralNetwork("dummy.nndf") # Assume empty for this direct test

        mock_sensor_neuron = MagicMock(spec=Neuron)
        mock_sensor_neuron.is_sensor_neuron.return_value = True
        
        mock_hidden_neuron = MagicMock(spec=Neuron)
        mock_hidden_neuron.is_sensor_neuron.return_value = False # e.g. hidden or motor
        
        mock_motor_neuron = MagicMock(spec=Neuron)
        mock_motor_neuron.is_sensor_neuron.return_value = False # e.g. hidden or motor

        nn.neurons = {
            "s0": mock_sensor_neuron,
            "h0": mock_hidden_neuron,
            "m0": mock_motor_neuron
        }
        nn.synapses = {"dummy_synapse_key": "dummy_synapse_value"} # Pass synapses dict

        nn.update()

        mock_sensor_neuron.update_sensor_neuron.assert_called_once()
        mock_sensor_neuron.update_hidden_or_motor_neuron.assert_not_called()
        
        mock_hidden_neuron.update_hidden_or_motor_neuron.assert_called_once_with(nn.neurons, nn.synapses)
        mock_hidden_neuron.update_sensor_neuron.assert_not_called()

        mock_motor_neuron.update_hidden_or_motor_neuron.assert_called_once_with(nn.neurons, nn.synapses)
        mock_motor_neuron.update_sensor_neuron.assert_not_called()

if __name__ == '__main__':
    unittest.main()
