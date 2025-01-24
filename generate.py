import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")

start = 1
sizes = [start * (0.9 ** i) for i in range(10)]

for i in range(10):
    x = 0
    y = 0
    z = sizes[i] / 2
    pyrosim.Send_Cube(name=f"Box{i}", pos=[x,y,z+i] , size=[sizes[i],sizes[i],sizes[i]])

pyrosim.End()
