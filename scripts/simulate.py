"""
simulate.py
Entry point for running the simulation.
Creates an instance of SIMULATION and calls its Run() method.
"""

from simulation import SIMULATION
import sys

def main():
    """
    Creates and runs the simulation
    """
    if len(sys.argv) > 1:
        simulation = SIMULATION(sys.argv[1])
    else:
        simulation = SIMULATION('DIRECT')
    simulation.Run()
    simulation.Get_Fitness()

if __name__ == '__main__':
    main()
