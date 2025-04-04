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
python3 -m venv .venv
source .venv/bin/activate
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

### 5. Running the Simulation
```bash
python src/search.py
```

## Helpful Scripts
### 1. Generate URDF/SDF Files
```bash
python src/generate.py
```

### 2. Running the Simulation
```bash
python src/simulate.py
```