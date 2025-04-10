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
import pickle
import time

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system('rm -f ./src/data/brain*.nndf')
        os.system('rm -f ./src/data/fitness*.txt')
        self.nextAvailableID = 0
        self.parents = {}
        
        self.total_evaluations = c.POPULATION_SIZE + c.NUMBER_OF_GENERATIONS * c.POPULATION_SIZE
        self.evals_completed = 0
        
        for i in range(c.POPULATION_SIZE):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1


    def Evaluate(self, solutions):
        # Record the start time at the first evaluation.
        if self.evals_completed == 0:
            self.start_time = time.time()

        for sol in solutions.values():
            sol.Evaluate('DIRECT')
            self.evals_completed += 1

            # Calculate elapsed time and estimate remaining time.
            elapsed_time = time.time() - self.start_time
            avg_time = elapsed_time / self.evals_completed
            remaining_evals = self.total_evaluations - self.evals_completed
            estimated_remaining = remaining_evals * avg_time

            # Convert estimated time into minutes and seconds.
            minutes = int(estimated_remaining) // 60
            seconds = int(estimated_remaining) % 60

            # Build progress bar.
            progress = int((self.evals_completed / self.total_evaluations) * 50)
            bar = '[' + '#' * progress + '-' * (50 - progress) + ']'

            # Print loading bar on one line and estimated time on the next.
            print(f'\rEvaluation {self.evals_completed}/{self.total_evaluations} {bar}')
            print(f'Estimated Time Remaining: {minutes:02d}:{seconds:02d}')
            
            # Move the cursor up 2 lines so the next update overwrites them.
            print("\033[2A", end='', flush=True)

    def Evolve(self):
        self.Evaluate(self.parents)
        for _ in range(c.NUMBER_OF_GENERATIONS):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.children = {}
        for key, parent in self.parents.items():
            child = copy.deepcopy(parent)
            child.Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1
            self.children[key] = child
        self.Mutate()
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
        with open('./src/data/best_solution.pkl', 'wb') as f:
            pickle.dump(best, f)
        # Re-simulate that solution with graphics on.
        best.Start_Simulation("GUI")