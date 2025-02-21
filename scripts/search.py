"""
search.py
"""

from parallelHillClimber import PARALLEL_HILL_CLIMBER


def main():
    phc = PARALLEL_HILL_CLIMBER()
    phc.Evolve()
    phc.Show_Best()

if __name__ == '__main__':
    main()