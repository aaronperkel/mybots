"""
motor.py
Implements increasingly efficient, but increasingly complex 
search methods to find good synaptic weights for a given 
desired behavior.
"""

from solution import SOLUTION
import constants as c
import copy

class HILL_CLIMBER:
    def __init__(self):
        self.parent = SOLUTION()

    def Evolve(self):
        self.parent.Evaluate('DIRECT')
        for _ in range(c.NUMBER_OF_GENERATIONS):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.child.Evaluate('DIRECT')
        self.Select()

    def Spawn(self):
        self.child = copy.deepcopy(self.parent)

    def Mutate(self):
        self.child.Mutate()

    def Select(self):
        if self.parent.fitness > self.child.fitness:
            self.parent = self.child
    
    def Print(self):
        print(f'Parent: {self.parent.fitness} Child: {self.child.fitness}')

    def Show_Best(self):
        self.parent.Evaluate('GUI')