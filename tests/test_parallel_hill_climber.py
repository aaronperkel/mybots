import unittest
from unittest.mock import patch, MagicMock, call
import sys
import os
import glob # For mocking

# Adjust path to import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.parallelHillClimber import ParallelHillClimber
from src.solution import Solution # Need Solution for type hints and instantiation
import src.constants as c

class TestParallelHillClimber(unittest.TestCase):
    """
    Tests for the ParallelHillClimber class in src.parallelHillClimber.py.
    """

    @patch('src.parallelHillClimber.glob.glob')
    @patch('src.parallelHillClimber.os.remove')
    @patch('src.parallelHillClimber.Solution') # Mock the Solution class
    def setUp(self, mock_solution_class, mock_os_remove, mock_glob_glob):
        """
        Set up for ParallelHillClimber tests.
        """
        # Mock glob.glob to return empty lists, simulating no old files
        mock_glob_glob.return_value = []

        # Configure the mock Solution class to return mock Solution instances
        # Each mock solution instance needs a fitness attribute for comparisons
        self.mock_solution_instances = []
        for i in range(c.POPULATION_SIZE * 2): # Enough for parents and potential children
            mock_sol = MagicMock(spec=Solution)
            mock_sol.fitness = float(i) # Assign some default fitness
            mock_sol.my_id = i
            self.mock_solution_instances.append(mock_sol)
        
        mock_solution_class.side_effect = self.mock_solution_instances

        self.phc = ParallelHillClimber()

        # Store mocks if needed
        self.mock_solution_class = mock_solution_class
        self.mock_os_remove = mock_os_remove
        self.mock_glob_glob = mock_glob_glob


    def test_initialization(self):
        """
        Test that __init__ initializes parents, next_available_id,
        and performs cleanup.
        """
        # Test cleanup calls
        expected_glob_calls = [call('./src/data/brain*.nndf'), call('./src/data/fitness*.txt')]
        self.mock_glob_glob.assert_has_calls(expected_glob_calls, any_order=True)
        # self.mock_os_remove would be called if glob.glob returned files

        self.assertEqual(len(self.phc.parents), c.POPULATION_SIZE)
        self.assertEqual(self.phc.next_available_id, c.POPULATION_SIZE)
        for i in range(c.POPULATION_SIZE):
            self.mock_solution_class.assert_any_call(i)
            self.assertIsInstance(self.phc.parents[i], MagicMock) # Since Solution is mocked


    @patch.object(ParallelHillClimber, 'evaluate')
    @patch.object(ParallelHillClimber, 'evolve_for_one_generation')
    def test_evolve_loop(self, mock_evolve_one_gen, mock_evaluate):
        """
        Test that evolve calls evolve_for_one_generation the correct number of times
        and calls evaluate on initial parents.
        """
        self.phc.evolve()
        
        mock_evaluate.assert_called_once_with(self.phc.parents)
        self.assertEqual(mock_evolve_one_gen.call_count, c.NUMBER_OF_GENERATIONS)


    @patch.object(ParallelHillClimber, 'mutate_children')
    @patch.object(ParallelHillClimber, 'evaluate')
    @patch.object(ParallelHillClimber, 'select_fitter')
    @patch('src.parallelHillClimber.copy.deepcopy') # Mock deepcopy
    def test_evolve_for_one_generation(self, mock_deepcopy, mock_select, mock_evaluate, mock_mutate):
        """
        Test the sequence of operations in evolve_for_one_generation.
        """
        # Ensure parents are set up with mock solutions that can be deepcopied
        for i in range(c.POPULATION_SIZE):
             # Make deepcopy return a new mock for each parent to simulate new child objects
            new_mock_child = MagicMock(spec=Solution)
            new_mock_child.my_id = self.phc.next_available_id + i # Simulate ID setting
            # Ensure deepcopy returns distinct mocks if called multiple times in the loop
            # For this, we'll use a side_effect on deepcopy if it's simpler.
            # Here, we assume each parent is a distinct mock_solution_instance from setUp.
            # Let's make deepcopy return a new distinct mock each time it's called.
            
            # This part is tricky because deepcopy is called inside a loop.
            # We need deepcopy to return a *new* mock each time.
            # The easiest way is to have a list of mocks and pop from it.
            
        # Let's simplify: assume deepcopy works and returns a new mock.
        # The actual test is whether the methods are called.
        
        # Configure deepcopy to return new mock solution instances for children
        # Take from the latter half of self.mock_solution_instances
        mock_deepcopy.side_effect = self.mock_solution_instances[c.POPULATION_SIZE:]

        self.phc.evolve_for_one_generation()

        # Check that children are created (deepcopy is called for each parent)
        self.assertEqual(mock_deepcopy.call_count, c.POPULATION_SIZE)
        
        # Check that each child had set_id called (this is done on the mocked child)
        for i in range(c.POPULATION_SIZE):
            # The child objects are the ones returned by deepcopy
            child_obj = self.mock_solution_instances[c.POPULATION_SIZE + i]
            child_obj.set_id.assert_called_with(self.phc.next_available_id - c.POPULATION_SIZE + i)
            
        mock_mutate.assert_called_once()
        mock_evaluate.assert_called_once_with(self.phc.children)
        mock_select.assert_called_once()


    def test_evaluate_method(self):
        """
        Test that the evaluate method calls solution.evaluate on all solutions.
        """
        mock_solutions_dict = {
            0: MagicMock(spec=Solution),
            1: MagicMock(spec=Solution)
        }
        self.phc.evaluate(mock_solutions_dict)
        
        for sol in mock_solutions_dict.values():
            sol.evaluate.assert_called_once_with('DIRECT')

    def test_mutate_children(self):
        """
        Test that mutate_children calls mutate on all child solutions.
        """
        # Setup children
        self.phc.children = {i: MagicMock(spec=Solution) for i in range(c.POPULATION_SIZE)}
        self.phc.mutate_children()
        for child_sol in self.phc.children.values():
            child_sol.mutate.assert_called_once()

    def test_select_fitter_child_is_better(self):
        """
        Test select_fitter: child replaces parent if child's fitness is lower (better).
        """
        parent_mock = MagicMock(spec=Solution)
        parent_mock.fitness = 10.0
        
        child_mock = MagicMock(spec=Solution)
        child_mock.fitness = 5.0 # Lower fitness is better
        
        self.phc.parents = {0: parent_mock}
        self.phc.children = {0: child_mock}
        
        self.phc.select_fitter()
        self.assertEqual(self.phc.parents[0], child_mock, "Child should replace parent if fitter.")

    def test_select_fitter_parent_is_better(self):
        """
        Test select_fitter: parent is kept if parent's fitness is lower or equal.
        """
        parent_mock = MagicMock(spec=Solution)
        parent_mock.fitness = 5.0
        
        child_mock = MagicMock(spec=Solution)
        child_mock.fitness = 10.0
        
        self.phc.parents = {0: parent_mock}
        self.phc.children = {0: child_mock}
        
        self.phc.select_fitter()
        self.assertEqual(self.phc.parents[0], parent_mock, "Parent should be kept if fitter or equal.")

        # Test case: equal fitness
        child_mock.fitness = 5.0
        self.phc.select_fitter()
        self.assertEqual(self.phc.parents[0], parent_mock, "Parent should be kept if fitness is equal.")


    def test_show_best(self):
        """
        Test show_best: finds the best solution and calls its start_simulation method.
        """
        # Ensure parents are actual mock solution instances from setUp for this
        # or re-mock them here with fitness attributes.
        # Let's use a clear setup for parents for this test
        mock_sol_best = MagicMock(spec=Solution)
        mock_sol_best.fitness = 1.0
        mock_sol_best.my_id = 100

        mock_sol_worst = MagicMock(spec=Solution)
        mock_sol_worst.fitness = 10.0
        mock_sol_worst.my_id = 101
        
        self.phc.parents = {0: mock_sol_worst, 1: mock_sol_best}
        
        self.phc.show_best()
        
        # Verify that start_simulation was called on the best solution with 'GUI'
        mock_sol_best.start_simulation.assert_called_once_with('GUI')
        mock_sol_worst.start_simulation.assert_not_called()

    def test_show_best_no_parents(self):
        """
        Test show_best when there are no parents.
        """
        self.phc.parents = {}
        # We expect a print statement, can use patch('builtins.print') if needed
        with patch('builtins.print') as mock_print:
            self.phc.show_best()
            mock_print.assert_any_call("No solutions available to show.")


if __name__ == '__main__':
    unittest.main()
