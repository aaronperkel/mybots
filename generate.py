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
    pyrosim.Send_Cube(name="Link0", pos=[0,0,0.5], size=[1,1,1])
    pyrosim.Send_Joint(name="Link0_Link1", parent="Link0", child="Link1", type="revolute", position=[0,0,1.0])
    pyrosim.Send_Cube(name="Link1", pos=[0,0,0.5], size=[1,1,1])
    pyrosim.Send_Joint(name="Link1_Link2", parent="Link1", child="Link2", type="revolute", position=[0,0,1.0])
    pyrosim.Send_Cube(name="Link2", pos=[0,0,0.5], size=[1,1,1])
    pyrosim.End()

if __name__ == '__main__':
    Create_World()
    Create_Robot()