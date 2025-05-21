"""
search.py

This script serves as the main entry point for running the parallel hill climber
algorithm to evolve a robot's behavior. It initializes the search process,
runs the evolutionary algorithm, and then displays the best solution found.
"""

from parallelHillClimber import ParallelHillClimber
import constants as c # Although not directly used, it's part of the project config


def main():
    """
    Initializes and runs the parallel hill climber algorithm.

    This function creates an instance of the ParallelHillClimber,
    evolves the solutions over a number of generations, and then
    simulates the best solution in a GUI.
    """
    phc = ParallelHillClimber()
    phc.evolve()
    phc.show_best()

if __name__ == '__main__':
    main()