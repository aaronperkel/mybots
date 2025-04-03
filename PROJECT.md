# Strength in numbers. (Hard)
1. You can create a swarm of robots in the following manner.
2. Change solution.py to write out multiple body.urdf files. In each one, the positions of the links and joints should be offset by some amount. This will ensure that the robot encoded in each file will not placed on top of one another.
3. Modify simulate.py's code hierarchy to read in multiple body.sdf files, and delete them when it is done with them.
4. If you strew objects in front of the swarm as described in the "Full steam ahead" project above, some members of the swarm will collide with some of them.
5. There is strength in numbers: modify the calculation of fitness to reward the distance travelled by the robot that travelled the furthest. To do so, you will hae to modify robot.py's Get_Fitness() method to consider the positions of each member of the swarm.

## Milestones:
### Milestone 1:
- Objective: Modify solution.py to output multiple body.urdf files with offset positions.
### Milestone 2:
- Modify simulate.py to load multiple URDF files and run the simulation for the swarm.
### Milestone 3:
- Introduce obstacles (blocks) in front of the swarm (as inspired by the Full Steam Ahead project) to cause some collisions.
### Milestone 4:
- Update the fitness function in robot.py to evaluate and reward the maximum distance traveled among the swarm members.