"""
world.py
Defines the World class, which loads the SDF world and plane into the PyBullet simulation.
"""

import pybullet as p
import os # For path joining

class World:
    """
    Represents the simulation world in PyBullet.
    It loads the environment from an SDF (Simulation Description Format) file
    and adds a standard ground plane URDF (Unified Robot Description Format).
    """
    def __init__(self):
        """
        Initializes the world by loading the SDF file defining static environment
        elements and a plane URDF to serve as the ground.
        Error handling is included for file loading issues.
        """
        world_sdf_path = os.path.join("./src/data", "world.sdf")
        plane_urdf_path = "plane.urdf" # Standard PyBullet plane

        # Load the world description from an SDF file.
        try:
            p.loadSDF(world_sdf_path)
        except p.error as e:
            print(f"Error loading world SDF '{world_sdf_path}': {e}")
            # Consider raising the error or having a fallback mechanism
        
        # Load a plane URDF to act as the ground.
        try:
            self.plane_id = p.loadURDF(plane_urdf_path)
        except p.error as e:
            print(f"Error loading plane URDF '{plane_urdf_path}': {e}")
            # Consider raising the error or having a fallback mechanism
