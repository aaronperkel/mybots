"""
parallelHillClimber.py
Implements a parallel hill climber search algorithm to find optimal synaptic 
weights for a robot's neural network, aiming for a desired behavior.
"""

from solution import Solution # Updated import
import constants as c
import copy
import os
import glob

class ParallelHillClimber:
    """
    Manages the parallel hill climbing evolutionary process.
    It maintains a population of parent solutions, generates child solutions
    through mutation, evaluates them, and selects the fittest ones.
    """
    def __init__(self):
        """
        Initializes the ParallelHillClimber.
        This includes cleaning up old data files (brains, fitness scores)
        and creating an initial population of parent solutions.
        """
        # Clean up previous run's data files
        for file_pattern in ['./src/data/brain*.nndf', './src/data/fitness*.txt']:
            for file_path in glob.glob(file_pattern):
                try:
                    os.remove(file_path)
                except OSError as e:
                    print(f"Error removing file {file_path}: {e}")

        self.next_available_id = 0 # Renamed attribute
        self.parents = {}
        
        for i in range(c.POPULATION_SIZE):
            self.parents[i] = Solution(self.next_available_id) # Use Solution
            self.next_available_id += 1

    def evaluate(self, solutions_dict):
        """
        Evaluates the fitness of each solution in the provided dictionary.

        Args:
            solutions_dict (dict): A dictionary of solutions to evaluate,
                                   where keys are solution IDs and values are Solution objects.
        """
        for solution in solutions_dict.values():
            solution.evaluate('DIRECT') # Updated method call

    def evolve(self):
        """
        Runs the main evolutionary loop for a set number of generations.
        This includes evaluating initial parents, and then iteratively
        generating and selecting children.
        """
        self.evaluate(self.parents)
        for current_generation in range(c.NUMBER_OF_GENERATIONS):
            self.evolve_for_one_generation()
            progress = int((current_generation + 1) / c.NUMBER_OF_GENERATIONS * 50)
            bar = '[' + '#' * progress + '-' * (50 - progress) + ']'
            print(f'\rGeneration {current_generation + 1}/{c.NUMBER_OF_GENERATIONS} {bar}', end='', flush=True)
            # self.print_results() # Optional: print results at each generation
        print()  # Move to the next line after completion

    def evolve_for_one_generation(self):
        """
        Performs one generation of evolution:
        1. Spawns children from parents.
        2. Mutates the children.
        3. Evaluates the children.
        4. Selects children to replace parents if they are fitter.
        """
        self.children = {}
        for key, parent_solution in self.parents.items():
            child_solution = copy.deepcopy(parent_solution)
            child_solution.set_id(self.next_available_id) # Updated method call
            self.next_available_id += 1
            self.children[key] = child_solution
        
        self.mutate_children() # Changed to a more descriptive name
        self.evaluate(self.children)
        self.select_fitter() # Changed to a more descriptive name
        # self.print_results() # Optional: print results after selection

    def mutate_children(self): # Renamed for clarity
        """
        Applies mutation to each child solution in the current generation's children.
        """
        for child_solution in self.children.values():
            child_solution.mutate() # Updated method call

    def select_fitter(self): # Renamed for clarity
        """
        Compares each child solution with its parent. If the child is fitter
        (has a lower fitness score, assuming lower is better), it replaces the parent.
        """
        for key in self.parents:
            # Assuming lower fitness is better as per typical optimization problems
            if self.children[key].fitness < self.parents[key].fitness:
                self.parents[key] = self.children[key]
    
    def print_results(self):
        """
        Prints the fitness scores of the current parent and child populations.
        Useful for debugging or tracking progress.
        """
        print("\n--- Generation Results ---")
        for key in self.parents:
            parent_fitness = self.parents[key].fitness
            child_fitness_str = "N/A"
            if key in self.children and self.children[key].fitness is not None:
                 child_fitness_str = f"{self.children[key].fitness:.4f}"
            else: # Child might not exist or not have fitness if accessed at wrong time
                child_fitness_str = "N/A (or not yet evaluated)"

            print(f"Parent {key}: {parent_fitness:.4f} | Child {key}: {child_fitness_str}")
        print("-------------------------\n")

    def show_best(self):
        """
        Identifies the solution with the best (lowest) fitness score from the
        final parent population and simulates it in GUI mode.
        """
        if not self.parents:
            print("No solutions available to show.")
            return

        # Find the parent with the lowest fitness (assuming lower is better)
        best_solution = min(self.parents.values(), key=lambda sol: sol.fitness if sol.fitness is not None else float('inf'))
        
        if best_solution.fitness is None:
            print("Best solution has no fitness value, cannot simulate.")
            return

        print(f"\nShowing best solution (ID: {best_solution.my_id}, Fitness: {best_solution.fitness:.4f})")
        # Re-simulate that solution with graphics on.
        best_solution.start_simulation('GUI') # Updated method call