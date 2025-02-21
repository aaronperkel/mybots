"""
parallelHillClimber.py
Implements increasingly efficient, but increasingly complex 
search methods to find good synaptic weights for a given 
desired behavior.
"""

from solution import SOLUTION
import constants as c
import copy

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        self.nextAvailableID = 0
        self.parents = {}
        for i in range(c.POPULATION_SIZE):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):
        for parent in self.parents.values():
            parent.Evaluate('DIRECT')
        # for i in range(c.NUMBER_OF_GENERATIONS):
        #     self.Evolve_For_One_Generation()
        #     # Create a simple progress bar (50 characters wide)
        #     progress = int((i + 1) / c.NUMBER_OF_GENERATIONS * 50)
        #     bar = '[' + '#' * progress + '-' * (50 - progress) + ']'
        #     print(f'\rGeneration {i+1}/{c.NUMBER_OF_GENERATIONS} {bar}', end='', flush=True)
        # print()  # Move to the next line after completion

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate('DIRECT')
        self.Select()

    def Spawn(self):
        self.child = copy.deepcopy(self.parent)
        self.child.Set_ID(self.nextAvailableID)
        self.nextAvailableID += 1

    def Mutate(self):
        self.child.Mutate()

    def Select(self):
        if self.parent.fitness > self.child.fitness:
            self.parent = self.child
    
    def Print(self):
        print(f'Parent: {self.parent.fitness} Child: {self.child.fitness}')

    def Show_Best(self):
        # self.parent.Evaluate('GUI')
        pass