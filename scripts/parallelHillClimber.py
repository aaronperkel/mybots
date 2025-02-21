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
        os.system('rm brain*.nndf')
        os.system('rm fitness*.txt')
        self.nextAvailableID = 0
        self.parents = {}
        for i in range(c.POPULATION_SIZE):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):
        for self.parent in self.parents.values():
            self.parent.Start_Simulation('DIRECT')
        for self.parent in self.parents.values():
            self.parent.Wait_For_Simulation_To_End()
        for i in range(c.NUMBER_OF_GENERATIONS):
            self.Evolve_For_One_Generation()
            pass
        #     # Create a simple progress bar (50 characters wide)
        #     progress = int((i + 1) / c.NUMBER_OF_GENERATIONS * 50)
        #     bar = '[' + '#' * progress + '-' * (50 - progress) + ']'
        #     print(f'\rGeneration {i+1}/{c.NUMBER_OF_GENERATIONS} {bar}', end='', flush=True)
        # print()  # Move to the next line after completion

    def Evolve_For_One_Generation(self):
        self.children = {}
        for key, parent in self.parents.items():
            child = copy.deepcopy(parent)
            child.Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1
            self.children[key] = child
        self.Spawn()
        self.Mutate()
        # self.child.Evaluate('DIRECT')
        # self.Select()

    def Spawn(self):
        self.child = copy.deepcopy(self.parent)
        self.child.Set_ID(self.nextAvailableID)
        self.nextAvailableID += 1

    def Mutate(self):
        for child in self.children.values():
            child.Mutate()

    def Select(self):
        if self.parent.fitness > self.child.fitness:
            self.parent = self.child
    
    def Print(self):
        print(f'Parent: {self.parent.fitness} Child: {self.child.fitness}')

    def Show_Best(self):
        # self.parent.Evaluate('GUI')
        pass