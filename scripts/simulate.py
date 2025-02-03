"""
simulate.py
Entry point for running the simulation.
Creates an instance of SIMULATION and calls its Run() method.
"""

from simulation import SIMULATION

def main():
    simulation = SIMULATION()
    simulation.Run()

if __name__ == '__main__':
    main()