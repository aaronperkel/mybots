"""
search.py
"""

from parallelHillClimber import PARALLEL_HILL_CLIMBER
import constants as c


def main():
    phc = PARALLEL_HILL_CLIMBER()
    phc.Evolve()
    phc.Show_Best()

if __name__ == '__main__':
    progress = int(1 / c.NUMBER_OF_GENERATIONS * 50)
    bar = '[' + '#' * progress + '-' * (50 - progress) + ']'
    print(f'\rGeneration {1}/{c.NUMBER_OF_GENERATIONS} {bar}', end='', flush=True)
    main()