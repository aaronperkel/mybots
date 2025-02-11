# mybots

A robotics simulation project using PyBullet and neural network control. This repository contains everything you need to build and run the simulation.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/aaronperkel/mybots.git
cd mybots
```

### 2. Create a Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install the Package

```bash
python setup.py install
```

## Generate URDF/SDF Files
```bash
python scripts/generate.py
```

## Running the Simulation
```bash
python scripts/simulate.py
```