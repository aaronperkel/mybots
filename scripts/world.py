"""
world.py
Defines the WORLD class, which loads the SDF world and plane into the PyBullet simulation.
"""

class WORLD:
    def __init__(self):
        import pybullet as p
        p.loadSDF("data/world.sdf")
        self.plane_id = p.loadURDF("plane.urdf")