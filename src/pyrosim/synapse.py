"""
synapse.py

This module defines the Synapse class, representing a connection between
two neurons in the neural network. It stores the source and target neuron names
and the weight of the connection, parsed from an NNDF file.
"""

class Synapse:
    """
    Represents a synapse connecting two neurons in the neural network.
    It stores the source neuron name, target neuron name, and the weight 
    of the connection, as defined in an NNDF (Neural Network Definition File) line.
    """
    def __init__(self, line_from_nndf):
        """
        Initializes a Synapse based on a definition line from an NNDF file.

        Args:
            line_from_nndf (str): A string line from the .nndf file 
                                  defining the synapse's source, target, and weight.
        """
        self.source_neuron_name = None
        self.target_neuron_name = None
        self.weight = 0.0

        self._determine_source_neuron_name(line_from_nndf)
        self._determine_target_neuron_name(line_from_nndf)
        self._determine_weight(line_from_nndf)

    def get_source_neuron_name(self):
        """Returns the name of the source (presynaptic) neuron."""
        return self.source_neuron_name

    def get_target_neuron_name(self):
        """Returns the name of the target (postsynaptic) neuron."""
        return self.target_neuron_name

    def get_weight(self):
        """Returns the weight (strength) of the synapse."""
        return self.weight

# -------------------------- Internal helper methods -------------------------

    def _determine_source_neuron_name(self, line):
        """
        Extracts and sets the source neuron name from the NNDF definition line.
        Assumes format: ... sourceNeuronName="name" ...
        """
        if "sourceNeuronName" in line:
            parts = line.split('"')
            if len(parts) > 1: # Check if splitting produced enough parts
                self.source_neuron_name = parts[1]

    def _determine_target_neuron_name(self, line):
        """
        Extracts and sets the target neuron name from the NNDF definition line.
        Assumes format: ... targetNeuronName="name" ...
        """
        if "targetNeuronName" in line:
            parts = line.split('"')
            if len(parts) > 3: # Check if splitting produced enough parts
                self.target_neuron_name = parts[3]

    def _determine_weight(self, line):
        """
        Extracts and sets the synapse weight from the NNDF definition line.
        Assumes format: ... weight="value" ...
        Handles potential ValueError if weight is not a valid float.
        """
        if "weight" in line:
            parts = line.split('"')
            if len(parts) > 5: # Check if splitting produced enough parts
                try:
                    self.weight = float(parts[5])
                except ValueError:
                    # Log a warning and default weight to 0.0 if parsing fails
                    print(f"Warning: Could not parse weight '{parts[5]}' as float for synapse. Defaulting to 0.0.")
                    self.weight = 0.0
