"""
sensor.py
Defines the SENSOR class, which measures touch sensor values for a single link.
Stores a time-series of sensor readings for each simulation timestep.
"""

class SENSOR:
    def __init__(self, link_name):
        import constants as c
        import numpy as np

        self.link_name = link_name
        self.values = np.zeros(c.STEPS)

    def Get_Value(self, t):
        import constants as c
        from pyrosim import pyrosim

        self.values[t] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.link_name)
        # BUG: this only works with -2 and not -1?
        if t == c.STEPS - 2:
            print(self.values)