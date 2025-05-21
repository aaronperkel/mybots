"""
sensor.py
Defines the Sensor class, which measures touch sensor values for a single link.
Stores a time-series of sensor readings for each simulation timestep.
"""

import constants as c
import numpy as np
from pyrosim import pyrosim

class Sensor:
    """
    Represents a touch sensor on a specific link of the robot.
    It records a time-series of sensor readings (e.g., contact data)
    during a simulation.
    """
    def __init__(self, link_name):
        """
        Initializes the Sensor.

        Args:
            link_name (str): The name of the robot link this sensor is associated with.
        """
        self.link_name = link_name
        # Initialize a NumPy array to store sensor values for each simulation step.
        self.values = np.zeros(c.STEPS) 

    def get_value(self, t):
        """
        Retrieves the sensor's touch value from Pyrosim at a given time step
        and stores it in the `self.values` array.

        Args:
            t (int): The current time step in the simulation.
        """
        # Get the touch sensor value for the specified link using the pyrosim library.
        self.values[t] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.link_name)

    def save_values(self):
        """
        Saves the recorded sensor values to a NumPy binary file (.npy).
        The filename is constructed based on the sensor's link name and stored
        in the './src/data/' directory. This method is useful for debugging or
        data analysis post-simulation.
        """
        # Construct the full file path for saving the sensor data.
        file_path = f'./src/data/{self.link_name}_sensor_values.npy'
        np.save(file_path, self.values)
