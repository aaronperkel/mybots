"""
generate.py
Script to create an SDF world containing a single cube using pyrosim.
"""

import pyrosim.pyrosim as pyrosim

def Create_World():
    """
    Create an SDF file named 'world.sdf' containing a single cube.
    """
    pyrosim.Start_SDF("world.sdf")
    pyrosim.Send_Cube(name="Box", pos=[-4,4,0.5], size=[1,1,1])
    pyrosim.End()

def Create_Robot():
    """
    Create a URDF file named 'body.urdf' containing a single cube.
    """
    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube(name="Torso", pos=[0,0,0.5], size=[1,1,1])
    pyrosim.Send_Joint(name="Torso_Leg", parent="Torso", child="Leg", type="revolute", position=[0.5,0,1.0])
    pyrosim.Send_Cube(name="Leg", pos=[1,0,1.5], size=[1,1,1])
    pyrosim.End()

if __name__ == '__main__':
    Create_World()
    Create_Robot()