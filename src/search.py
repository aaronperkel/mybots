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
    total_evaluations = c.POPULATION_SIZE + c.NUMBER_OF_GENERATIONS * c.POPULATION_SIZE
    progress = int((0 / total_evaluations) * 50)
    bar = '[' + '#' * progress + '-' * (50 - progress) + ']'
    print(f'\rEvaluation {0}/{total_evaluations} {bar}', end='', flush=True)
    main()