"""
neuralNetwork.py

This module defines the NeuralNetwork class, which is responsible for
parsing a Neural Network Definition File (NNDF), constructing the network
of neurons and synapses, and managing its state and updates.
"""

from pyrosim.neuron  import Neuron
from pyrosim.synapse import Synapse

class NeuralNetwork:
    """
    Represents a neural network, managing neurons and synapses loaded from an NNDF file.
    The network is built by parsing neuron and synapse definitions from the file.
    It supports updating neuron states and querying network properties.
    """
    def __init__(self, nndf_file_name):
        """
        Initializes the neural network by loading its structure from an NNDF file.

        Args:
            nndf_file_name (str): Path to the Neural Network Definition File (.nndf).
        """
        self.neurons = {}
        self.synapses = {}

        try:
            with open(nndf_file_name, "r") as f:
                for line in f:
                    self._digest_line(line)
        except FileNotFoundError:
            print(f"Error: NNDF file '{nndf_file_name}' not found.")
            # Consider raising an error or specific handling if NN cannot be built
        except Exception as e: # Catch other potential file reading errors
            print(f"Error reading NNDF file '{nndf_file_name}': {e}")


    def print_values(self):
        """Prints the current activation values of sensor, hidden, and motor neurons."""
        self._print_sensor_neuron_values()
        self._print_hidden_neuron_values()
        self._print_motor_neuron_values()
        print("") # Adds a final newline for clean output

    def update(self):
        """
        Updates the state of all neurons in the network.
        Sensor neurons are updated based on external input (via Neuron methods).
        Hidden and motor neurons are updated based on weighted inputs from connected neurons.
        """
        for neuron in self.neurons.values(): # Iterate over neuron objects
            if neuron.is_sensor_neuron():
                neuron.update_sensor_neuron()
            else:
                neuron.update_hidden_or_motor_neuron(self.neurons, self.synapses)

    def get_neuron_names(self):
        """Returns a list of all neuron names (identifiers) in the network."""
        return list(self.neurons.keys())
    
    def is_motor_neuron(self, neuron_name):
        """
        Checks if the neuron with the given name is a motor neuron.

        Args:
            neuron_name (str): The name of the neuron to check.
        Returns:
            bool: True if the neuron is a motor neuron, False otherwise.
                  Returns False if neuron_name is not found.
        """
        neuron = self.neurons.get(neuron_name)
        return neuron.is_motor_neuron() if neuron else False
    
    def get_motor_neurons_joint(self, neuron_name):
        """
        Gets the joint name associated with the specified motor neuron.

        Args:
            neuron_name (str): The name of the motor neuron.
        Returns:
            str or None: The name of the joint, or None if not a motor neuron
                         or neuron_name not found.
        """
        neuron = self.neurons.get(neuron_name)
        return neuron.get_joint_name() if neuron and neuron.is_motor_neuron() else None
    
    def get_value_of(self, neuron_name):
        """
        Gets the current activation value of the specified neuron.

        Args:
            neuron_name (str): The name of the neuron.
        Returns:
            float or None: The activation value, or None if neuron_name not found.
        """
        neuron = self.neurons.get(neuron_name)
        return neuron.get_value() if neuron else None

# ---------------- Internal methods (conventionally private) -------------------

    def _add_neuron_from_line(self, line):
        """Creates a Neuron object from a definition line and adds it to the network."""
        neuron = Neuron(line)
        self.neurons[neuron.get_name()] = neuron

    def _add_synapse_from_line(self, line):
        """Creates a Synapse object from a definition line and adds it to the network."""
        synapse = Synapse(line)
        source_neuron_name = synapse.get_source_neuron_name() 
        target_neuron_name = synapse.get_target_neuron_name()
        self.synapses[(source_neuron_name, target_neuron_name)] = synapse

    def _digest_line(self, line):
        """
        Processes a single line from the NNDF file.
        If the line defines a neuron, it's added. If it defines a synapse, it's added.
        """
        if self._line_contains_neuron_definition(line):
            self._add_neuron_from_line(line)
        elif self._line_contains_synapse_definition(line): # Use elif for mutual exclusivity
            self._add_synapse_from_line(line)

    def _line_contains_neuron_definition(self, line):
        """Checks if a line from NNDF contains a neuron definition."""
        return "neuron" in line # Simple check, might need refinement for robustness

    def _line_contains_synapse_definition(self, line):
        """Checks if a line from NNDF contains a synapse definition."""
        return "synapse" in line # Simple check, might need refinement for robustness

    def _print_sensor_neuron_values(self):
        """Helper method to print values of all sensor neurons, sorted by name."""
        print("sensor neuron values: ", end="")
        for neuron_name in sorted(self.neurons.keys()):
            neuron = self.neurons[neuron_name]
            if neuron.is_sensor_neuron(): 
                neuron.print_value()
        print("")

    def _print_hidden_neuron_values(self):
        """Helper method to print values of all hidden neurons, sorted by name."""
        print("hidden neuron values: ", end="")
        for neuron_name in sorted(self.neurons.keys()):
            neuron = self.neurons[neuron_name]
            if neuron.is_hidden_neuron():
                neuron.print_value() 
        print("")

    def _print_motor_neuron_values(self):
        """Helper method to print values of all motor neurons, sorted by name."""
        print("motor neuron values: ", end="")
        for neuron_name in sorted(self.neurons.keys()):
            neuron = self.neurons[neuron_name]
            if neuron.is_motor_neuron():
                neuron.print_value()
        print("")
