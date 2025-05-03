# mybots - final project

A robotics simulation project using PyBullet and neural network control. This repository contains everything you need to build and run the simulation.


## Milestones:
### Milestone 1:
- Objective: Modify solution.py to output multiple body.urdf files with offset positions.
### Milestone 2:
- Modify simulate.py to load multiple URDF files and run the simulation for the swarm. I will provide a video proof of the swarm simulation.
### Milestone 3:
- Introduce obstacles (blocks) in front of the swarm (as inspired by the Full Steam Ahead project) to cause collisions. Revised: Enhance the obstacle environment by adding multiple obstacles with varied positions, sizes, or even movement dynamics. This will create a more challenging course that forces different collision scenarios for the robots. A video will demonstrate these varied obstacle interactions.
### Milestone 4:
- Update the fitness function in robot.py to evaluate and reward the maximum distance traveled among the swarm members. Revised: Implement an A/B testing framework by modifying the fitness function to compare two evaluation approaches: one that rewards the best-performing individual (maximum distance traveled) and another that uses the average distance traveled by the entire swarm. Preliminary results and data comparisons from these two methods will be included in my final submission.

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

### 4. Choose a fitness function
```bash
export FITNESS_METHOD=max
```
OR
```bash
export FITNESS_METHOD=avg
```


### 5. Running the Simulation
```bash
python src/search.py
```