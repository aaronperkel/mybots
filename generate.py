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
    pyrosim.Send_Joint(name="Link0_Link1", parent="Link0", child="Link1", type="revolute", position=[0.0,0.0,1.0])
    pyrosim.Send_Cube(name="Link1", pos=[0,0,0.5], size=[1,1,1])
    pyrosim.Send_Joint(name="Link1_Link2", parent="Link1", child="Link2", type="revolute", position=[0.0,0.0,1.0])
    pyrosim.Send_Cube(name="Link2", pos=[0,0,0.5], size=[1,1,1])
    pyrosim.Send_Joint(name="Link2_Link3", parent="Link2", child="Link3", type="revolute", position=[0.0,0.5,0.5])
    pyrosim.Send_Cube(name="Link3", pos=[0,0.5,0], size=[1,1,1])
    pyrosim.Send_Joint(name="Link3_Link4", parent="Link3", child="Link4", type="revolute", position=[0.0,1.0,0.0])
    pyrosim.Send_Cube(name="Link4", pos=[0,0.5,0], size=[1,1,1])
    pyrosim.Send_Joint(name="Link4_Link5", parent="Link4", child="Link5", type="revolute", position=[0.0,0.5,-0.5])
    pyrosim.Send_Cube(name="Link5", pos=[0,0,-0.5], size=[1,1,1])
    pyrosim.Send_Joint(name="Link5_Link6", parent="Link5", child="Link6", type="revolute", position=[0.0,0.0,-1.0])
    pyrosim.Send_Cube(name="Link6", pos=[0,0,-0.5], size=[1,1,1])
    pyrosim.End()

if __name__ == '__main__':
    Create_World()
    Create_Robot()