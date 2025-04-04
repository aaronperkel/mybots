"""
sensor.py
Defines the SENSOR class, which measures touch sensor values for a single link.
Stores a time-series of sensor readings for each simulation timestep.
"""

import constants as c
import numpy as np
from pyrosim import pyrosim

class SENSOR:
    """
    An object that allows the robot to know if it is in contact wiht something
    """
    def __init__(self, link_name):
        self.link_name = link_name
        self.values = np.zeros(c.STEPS)

    def Get_Value(self, t):
        """
        Gets the value of the sensor and stores it in a dictionary
        """
        self.values[t] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.link_name)

    def Save_Values(self):
        np.save(f'./src/data/{self.link_name}_sensor_values.npy', self.values)
