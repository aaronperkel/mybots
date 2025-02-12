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
    directOrGUI = sys.argv[1]
    simulation = SIMULATION(directOrGUI)
    simulation.Run()
    simulation.Get_Fitness()

if __name__ == '__main__':
    main()
