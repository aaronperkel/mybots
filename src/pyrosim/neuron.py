"""
neuron.py

This module defines the Neuron class, representing a single unit in a neural network.
Neurons can be of type sensor, hidden, or motor, and their values are updated
based on sensor inputs or synaptic connections.
"""
import math
import pyrosim.pyrosim as pyrosim 
import pyrosim.constants as pyrosim_constants

class Neuron:
    """
    Represents a single neuron in the neural network.
    It can be a sensor, hidden, or motor neuron, parsed from an NNDF line.
    The neuron maintains its current activation value and connections.
    """
    def __init__(self, line_from_nndf):
        """
        Initializes a Neuron based on a definition line from an NNDF file.

        Args:
            line_from_nndf (str): A string line from the .nndf file defining the neuron's
                                  properties like name, type, and associated link/joint.
        """
        self.name = None
        self.type = None
        self.link_name = None  # Applicable if it's a sensor neuron
        self.joint_name = None # Applicable if it's a motor neuron
        self.value = 0.0       # Current activation value of the neuron

        self._determine_name(line_from_nndf)
        self._determine_type(line_from_nndf)
        self._search_for_link_name(line_from_nndf)
        self._search_for_joint_name(line_from_nndf)
        # Initial value is already 0.0

    def add_to_value(self, value_to_add):
        """Adds a specified value to the neuron's current activation value."""
        self.set_value(self.get_value() + value_to_add)

    def get_joint_name(self):
        """Returns the name of the joint this motor neuron is associated with, if any."""
        return self.joint_name

    def get_link_name(self):
        """Returns the name of the link this sensor neuron is associated with, if any."""
        return self.link_name

    def get_name(self):
        """Returns the unique name (identifier) of the neuron."""
        return self.name

    def get_value(self):
        """Returns the current activation value of the neuron."""
        return self.value

    def is_sensor_neuron(self):
        """Checks if this neuron is a sensor neuron."""
        return self.type == pyrosim_constants.SENSOR_NEURON

    def is_hidden_neuron(self):
        """Checks if this neuron is a hidden neuron."""
        return self.type == pyrosim_constants.HIDDEN_NEURON

    def is_motor_neuron(self):
        """Checks if this neuron is a motor neuron."""
        return self.type == pyrosim_constants.MOTOR_NEURON
    
    def update_sensor_neuron(self):
        """
        Updates the value of this sensor neuron by fetching the latest
        touch sensor reading for its associated link from Pyrosim.
        """
        if self.link_name:  # Ensure it's a sensor neuron with an associated link
            self.set_value(pyrosim.Get_Touch_Sensor_Value_For_Link(self.get_link_name()))
        else:
            # This condition should ideally not be met if NNDF is correct and parsing is robust
            print(f"Warning: update_sensor_neuron called on neuron '{self.name}' which has no link_name.")

    def update_hidden_or_motor_neuron(self, neurons_dict, synapses_dict):
        """
        Updates the value of a hidden or motor neuron. The value is calculated
        as the sum of weighted inputs from all connected presynaptic neurons,
        followed by applying a threshold (activation) function.

        Args:
            neurons_dict (dict): A dictionary of all neuron objects in the network,
                                 keyed by neuron names.
            synapses_dict (dict): A dictionary of all synapse objects in the network,
                                  keyed by (source_neuron_name, target_neuron_name) tuples.
        """
        self.set_value(0.0) # Reset value before accumulating new input
        for (source_neuron_name, target_neuron_name), synapse_obj in synapses_dict.items():
            if target_neuron_name == self.get_name(): # If this neuron is the target of the synapse
                presynaptic_neuron = neurons_dict.get(source_neuron_name)
                if presynaptic_neuron:
                    presynaptic_value = presynaptic_neuron.get_value()
                    weight = synapse_obj.get_weight() 
                    self._allow_presynaptic_neuron_to_influence_me(weight, presynaptic_value)
                else:
                    # This might indicate an issue in NNDF or network construction
                    print(f"Warning: Presynaptic neuron '{source_neuron_name}' not found for neuron '{self.name}'.")
        self._threshold()

    def _allow_presynaptic_neuron_to_influence_me(self, weight, presynaptic_value):
        """
        Calculates the influence of a single presynaptic neuron (weight * presynaptic_value)
        and adds it to this neuron's current activation value.
        This is an internal helper for update_hidden_or_motor_neuron.
        """
        influence = weight * presynaptic_value
        self.add_to_value(influence)

    def print_value(self):
        """Prints the neuron's current activation value to the console."""
        self._print_internal_value() 
        # Newline is not added here, allowing multiple values on one line if called in a loop.

    def set_value(self, new_value):
        """Sets the neuron's activation value to a new specified value."""
        self.value = new_value

# -------------------------- Internal helper methods -------------------------

    def _determine_name(self, line):
        """Extracts and sets the neuron's name from its NNDF definition line."""
        if "name" in line:
            parts = line.split('"')
            if len(parts) > 1: # e.g. neuron id="0" ...
                self.name = parts[1]

    def _determine_type(self, line):
        """Determines and sets the neuron's type (sensor, motor, hidden) from its NNDF line."""
        if "sensor" in line:
            self.type = pyrosim_constants.SENSOR_NEURON
        elif "motor" in line:
            self.type = pyrosim_constants.MOTOR_NEURON
        else:
            self.type = pyrosim_constants.HIDDEN_NEURON # Default if not specified as sensor/motor

    def _print_name(self):
        """Internal helper to print the neuron's name (primarily for debugging)."""
        print(self.name)

    def _print_type(self):
        """Internal helper to print the neuron's type (primarily for debugging)."""
        print(self.type)

    def _print_internal_value(self):
        """Internal helper to print the neuron's value with specific formatting."""
        print(self.value, " ", end="")

    def _search_for_joint_name(self, line):
        """Extracts and sets the joint name if this neuron is a motor neuron, from its NNDF line."""
        if "jointName" in line:
            parts = line.split('"')
            if len(parts) > 5: # e.g. ... jointName="Torso_BackLeg" ...
                self.joint_name = parts[5]

    def _search_for_link_name(self, line):
        """Extracts and sets the link name if this neuron is a sensor neuron, from its NNDF line."""
        if "linkName" in line:
            parts = line.split('"')
            if len(parts) > 5: # e.g. ... linkName="Torso" ...
                self.link_name = parts[5]

    def _threshold(self):
        """Applies the hyperbolic tangent (tanh) activation function to the neuron's current value."""
        self.value = math.tanh(self.value)
