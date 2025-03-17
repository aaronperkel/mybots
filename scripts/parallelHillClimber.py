"""
parallelHillClimber.py
Implements increasingly efficient, but increasingly complex 
search methods to find good synaptic weights for a given 
desired behavior.
"""

from solution import SOLUTION
import constants as c
import copy
import os

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system('rm -f data/brain*.nndf')
        os.system('rm -f data/fitness*.txt')
        self.nextAvailableID = 0
        self.parents = {}
        for i in range(c.POPULATION_SIZE):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evaluate(self, solutions):
        for sol in solutions.values():
            sol.Evaluate('DIRECT')

    def Evolve(self):
        self.Evaluate(self.parents)
        for i in range(c.NUMBER_OF_GENERATIONS):
            self.Evolve_For_One_Generation()
            # Create a simple progress bar (50 characters wide)
            progress = int((i + 1) / c.NUMBER_OF_GENERATIONS * 50)
            bar = '[' + '#' * progress + '-' * (50 - progress) + ']'
            print(f'\rGeneration {i+1}/{c.NUMBER_OF_GENERATIONS} {bar}', end='', flush=True)
            # self.Print()
        print()  # Move to the next line after completion
        self.Print()

    def Evolve_For_One_Generation(self):
        self.children = {}
        for key, parent in self.parents.items():
            child = copy.deepcopy(parent)
            child.Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1
            self.children[key] = child
        self.Evaluate(self.children)
        self.Select()

    def Spawn(self):
        self.child = copy.deepcopy(self.parent)
        self.child.Set_ID(self.nextAvailableID)
        self.nextAvailableID += 1

    def Mutate(self):
        for child in self.children.values():
            child.Mutate()

    def Select(self):
        for key in self.parents:
            if self.parents[key].fitness > self.children[key].fitness:
                self.parents[key] = self.children[key]
    
    def Print(self):
        print("")  # Blank line at the start
        for key in self.parents:
            parent_fitness = self.parents[key].fitness
            # Check if there's a corresponding child; if not, print "N/A"
            child_fitness = self.children[key].fitness if key in self.children else "N/A"
            print(f"Parent {key}: {parent_fitness}  Child {key}: {child_fitness}")
        print("")  # Blank line at the end

    def Show_Best(self):
        # Find the parent with the lowest fitness
        best = min(self.parents.values(), key=lambda sol: sol.fitness)
        # Re-simulate that solution with graphics on.
        best.Start_Simulation("GUI")