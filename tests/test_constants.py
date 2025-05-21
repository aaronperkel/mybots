import unittest
import src.constants as c

class TestConstants(unittest.TestCase):
    """
    Tests for the constants defined in src/constants.py.
    """

    def test_simulation_steps_defined(self):
        """
        Test that STEPS constant is defined and is an integer.
        """
        self.assertTrue(hasattr(c, 'STEPS'), "STEPS constant should be defined.")
        self.assertIsInstance(c.STEPS, int, "STEPS should be an integer.")
        self.assertGreater(c.STEPS, 0, "STEPS should be positive.")

    def test_number_of_generations_defined(self):
        """
        Test that NUMBER_OF_GENERATIONS constant is defined and is an integer.
        """
        self.assertTrue(hasattr(c, 'NUMBER_OF_GENERATIONS'), "NUMBER_OF_GENERATIONS constant should be defined.")
        self.assertIsInstance(c.NUMBER_OF_GENERATIONS, int, "NUMBER_OF_GENERATIONS should be an integer.")
        self.assertGreater(c.NUMBER_OF_GENERATIONS, 0, "NUMBER_OF_GENERATIONS should be positive.")

    def test_population_size_defined(self):
        """
        Test that POPULATION_SIZE constant is defined and is an integer.
        """
        self.assertTrue(hasattr(c, 'POPULATION_SIZE'), "POPULATION_SIZE constant should be defined.")
        self.assertIsInstance(c.POPULATION_SIZE, int, "POPULATION_SIZE should be an integer.")
        self.assertGreater(c.POPULATION_SIZE, 0, "POPULATION_SIZE should be positive.")

    def test_neural_network_topology_defined(self):
        """
        Test that NUM_SENSOR_NEURONS and NUM_MOTOR_NEURONS are defined and are integers.
        """
        self.assertTrue(hasattr(c, 'NUM_SENSOR_NEURONS'), "NUM_SENSOR_NEURONS constant should be defined.")
        self.assertIsInstance(c.NUM_SENSOR_NEURONS, int, "NUM_SENSOR_NEURONS should be an integer.")
        self.assertGreaterEqual(c.NUM_SENSOR_NEURONS, 0, "NUM_SENSOR_NEURONS should be non-negative.")

        self.assertTrue(hasattr(c, 'NUM_MOTOR_NEURONS'), "NUM_MOTOR_NEURONS constant should be defined.")
        self.assertIsInstance(c.NUM_MOTOR_NEURONS, int, "NUM_MOTOR_NEURONS should be an integer.")
        self.assertGreaterEqual(c.NUM_MOTOR_NEURONS, 0, "NUM_MOTOR_NEURONS should be non-negative.")

    def test_physics_parameters_defined(self):
        """
        Test that gravity constants and MAX_FORCE are defined and have correct types.
        """
        for gravity_component in ['GRAV_X', 'GRAV_Y', 'GRAV_Z']:
            self.assertTrue(hasattr(c, gravity_component), f"{gravity_component} constant should be defined.")
            self.assertIsInstance(getattr(c, gravity_component), (int, float), f"{gravity_component} should be a number.")
        
        self.assertTrue(hasattr(c, 'MAX_FORCE'), "MAX_FORCE constant should be defined.")
        self.assertIsInstance(c.MAX_FORCE, (int, float), "MAX_FORCE should be a number.")
        self.assertGreater(c.MAX_FORCE, 0, "MAX_FORCE should be positive.")

    def test_sleep_time_defined(self):
        """
        Test that SLEEP_TIME constant is defined and is a float.
        """
        self.assertTrue(hasattr(c, 'SLEEP_TIME'), "SLEEP_TIME constant should be defined.")
        self.assertIsInstance(c.SLEEP_TIME, float, "SLEEP_TIME should be a float.")
        self.assertGreaterEqual(c.SLEEP_TIME, 0, "SLEEP_TIME should be non-negative.")

if __name__ == '__main__':
    unittest.main()
