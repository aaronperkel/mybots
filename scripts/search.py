"""
search.py
"""

from hillclimber import HILL_CLIMBER


def main():
    hc = HILL_CLIMBER()
    hc.Evolve()
    hc.Show_Best()

if __name__ == '__main__':
    main()