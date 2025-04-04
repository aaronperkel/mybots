"""
world.py
Defines the WORLD class, which loads the SDF world and plane into the PyBullet simulation.
"""

import pybullet as p

class WORLD:
    """
    Loads a world and a plane for the simulation
    """
    def __init__(self):
        p.loadSDF("./src/data/world.sdf")
        self.plane_id = p.loadURDF("plane.urdf")
