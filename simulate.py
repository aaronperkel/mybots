import pybullet as p
import pybullet_data
import time

physicsClient = p.connect(p.GUI)
p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0,0,-9.8)

planeId = p.loadURDF("plane.urdf")

p.loadSDF("boxes.sdf")

# for i in range(2000):
#     p.stepSimulation()
#     time.sleep(1/60)
#     print(i)

while True:
    p.stepSimulation()
    time.sleep(.005)

p.disconnect()
