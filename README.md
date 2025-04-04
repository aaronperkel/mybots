# mybots - final project

A robotics simulation project using PyBullet and neural network control. This repository contains everything you need to build and run the simulation.

## Strength in numbers. (Hard)
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

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/aaronperkel/mybots.git
cd mybots
```

### 2. Create a Python Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Running the Simulation
```bash
python src/search.py
```