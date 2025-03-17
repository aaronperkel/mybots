"""
search.py
"""

from hillclimber import HILL_CLIMBER

def main():
    hc = HILL_CLIMBER()
    
    # Show the initial random solution in GUI mode.
    print("Showing initial solution:")
    hc.parent.Evaluate("GUI")
    input("Press Enter to start blind evolution...")

    # Run the blind evolution.
    hc.Evolve()

    # Show the final evolved solution in GUI mode.
    print("Showing final evolved solution:")
    hc.Show_Best()

if __name__ == '__main__':
    main()