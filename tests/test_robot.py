import unittest
from unittest.mock import patch, MagicMock, call
import sys
import os

# Adjust path to import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.robot import Robot
import src.constants as c

# Mock external dependencies that are not part of the Robot class itself
# We need to mock them BEFORE Robot is imported if Robot uses them at module level,
# but here Robot uses them within methods or __init__, so patching at method/class level is fine.

class TestRobot(unittest.TestCase):
    """
    Tests for the Robot class in src.robot.py.
    """

    @patch('src.robot.os.path.exists')
    @patch('src.robot.os.remove')
    @patch('src.robot.NeuralNetwork')
    @patch('src.robot.pyrosim')
    @patch('src.robot.p') # Mocking pybullet (p)
    def setUp(self, mock_p, mock_pyrosim, mock_neural_network, mock_os_remove, mock_os_path_exists):
        """
        Set up for Robot tests. This is called before each test method.
        Mocks are injected by the @patch decorators in reverse order of decorators.
        """
        self.solution_id = 0
        
        # Configure mocks
        mock_os_path_exists.return_value = False # Assume brain file doesn't exist by default
        mock_p.loadURDF.return_value = 0 # Mock robot_id
        
        # Mock pyrosim.linkNamesToIndices and pyrosim.jointNamesToIndices
        # These are set by pyrosim.Prepare_To_Simulate
        # We can simulate this by setting them directly on the mock_pyrosim object
        mock_pyrosim.linkNamesToIndices = {'Link0': 0, 'Link1': 1}
        mock_pyrosim.jointNamesToIndices = {'Joint0': 0, 'Joint1': 1}

        # We need to mock methods that would be called on the Robot instance during __init__
        # because self.prepare_to_sense and self.prepare_to_act are called in __init__
        # and we want to test them separately.
        with patch.object(Robot, 'prepare_to_sense', MagicMock()) as self.mock_prepare_to_sense, \
             patch.object(Robot, 'prepare_to_act', MagicMock()) as self.mock_prepare_to_act:
            
            self.robot = Robot(self.solution_id)

            # Store mocks for individual test methods if needed
            self.mock_p = mock_p
            self.mock_pyrosim = mock_pyrosim
            self.mock_neural_network = mock_neural_network
            self.mock_os_remove = mock_os_remove
            self.mock_os_path_exists = mock_os_path_exists


    def test_robot_initialization(self):
        """
        Test that __init__ correctly initializes the robot.
        """
        self.assertEqual(self.robot.solution_id, self.solution_id)
        self.mock_p.loadURDF.assert_called_once_with("./src/data/body.urdf")
        self.mock_pyrosim.Prepare_To_Simulate.assert_called_once_with(0) # 0 is the mocked robot_id
        
        expected_brain_file = f"./src/data/brain{self.solution_id}.nndf"
        self.mock_neural_network.assert_called_once_with(expected_brain_file)
        
        # Test that prepare_to_sense and prepare_to_act were called by __init__
        self.mock_prepare_to_sense.assert_called_once()
        self.mock_prepare_to_act.assert_called_once()

        # Test brain file removal logic (default: file does not exist)
        self.mock_os_path_exists.assert_called_with(expected_brain_file)
        self.mock_os_remove.assert_not_called()

    @patch('src.robot.os.path.exists')
    @patch('src.robot.os.remove')
    def test_robot_initialization_removes_existing_brain_file(self, mock_os_remove, mock_os_path_exists):
        """
        Test that __init__ removes an existing brain file.
        Need to re-patch os.path.exists for this specific test.
        """
        mock_os_path_exists.return_value = True # Simulate brain file exists
        expected_brain_file = f"./src/data/brain{self.solution_id}.nndf"

        # Re-initialize robot to trigger the logic with new mock value
        with patch.object(Robot, 'prepare_to_sense', MagicMock()), \
             patch.object(Robot, 'prepare_to_act', MagicMock()):
            robot_for_this_test = Robot(self.solution_id)

        mock_os_path_exists.assert_called_with(expected_brain_file)
        mock_os_remove.assert_called_with(expected_brain_file)


    @patch('src.robot.Sensor') # Mock the Sensor class
    def test_prepare_to_sense(self, mock_sensor_class):
        """
        Test that prepare_to_sense creates Sensor objects for each link.
        """
        # Undo the specific mock for prepare_to_sense from setUp for this one test
        with patch.object(Robot, 'prepare_to_act', MagicMock()): # keep this one mocked
            # We need to call prepare_to_sense directly as it was mocked in setUp's Robot instance
            # Create a new robot instance or call it on the existing one after removing the specific mock
            # For simplicity, let's just call it on the existing robot, assuming the mock can be "overridden"
            # by a direct call if we unpatch or use the original method.
            # The most robust way is to create a new instance OR to ensure setUp's mock is not active for this.
            # However, setUp mocks instance methods, not the class's methods globally.
            # The Robot instance `self.robot` already had its `prepare_to_sense` mocked and called.
            # So, we need to call the *original* method.
            
            # Get the original method before it was mocked in setUp for the instance
            # This is a bit tricky. Let's re-initialize a robot for this test without the method mock.
            
            # Restore original prepare_to_sense for a new instance
            # This requires careful handling of the patches in setUp.
            # Simpler: call the method on the instance, but first ensure its `self.sensors` is empty
            self.robot.sensors = {} # Reset from potential setUp call
            Robot.prepare_to_sense(self.robot) # Call the original method

        self.assertEqual(len(self.robot.sensors), len(self.mock_pyrosim.linkNamesToIndices))
        
        expected_calls = [call(link_name) for link_name in self.mock_pyrosim.linkNamesToIndices.keys()]
        mock_sensor_class.assert_has_calls(expected_calls, any_order=True)


    def test_sense(self):
        """
        Test that sense calls get_value on all sensor objects.
        """
        # Create mock sensor objects and assign to self.robot.sensors
        self.robot.sensors = {
            'Link0': MagicMock(spec=sys.modules['src.sensor'].Sensor), 
            'Link1': MagicMock(spec=sys.modules['src.sensor'].Sensor)
        }
        
        time_step = 10
        self.robot.sense(time_step)
        
        for mock_sensor_obj in self.robot.sensors.values():
            mock_sensor_obj.get_value.assert_called_once_with(time_step)

    @patch('src.robot.Motor') # Mock the Motor class
    def test_prepare_to_act(self, mock_motor_class):
        """
        Test that prepare_to_act creates Motor objects for each joint.
        """
        self.robot.motors = {} # Reset
        Robot.prepare_to_act(self.robot) # Call original method

        self.assertEqual(len(self.robot.motors), len(self.mock_pyrosim.jointNamesToIndices))
        expected_calls = [call(joint_name) for joint_name in self.mock_pyrosim.jointNamesToIndices.keys()]
        mock_motor_class.assert_has_calls(expected_calls, any_order=True)

    def test_act(self):
        """
        Test that act calls set_value on motor objects based on neural network output.
        """
        # Mock the neural network (self.robot.nn was set in setUp)
        self.robot.nn.get_neuron_names.return_value = ['neuron_motor0', 'neuron_sensor', 'neuron_motor1']
        
        def is_motor_side_effect(neuron_name):
            return "motor" in neuron_name
        self.robot.nn.is_motor_neuron.side_effect = is_motor_side_effect
        
        def get_joint_name_side_effect(neuron_name):
            if neuron_name == 'neuron_motor0': return 'Joint0'
            if neuron_name == 'neuron_motor1': return 'Joint1'
            return None
        self.robot.nn.get_motor_neurons_joint.side_effect = get_joint_name_side_effect
        
        self.robot.nn.get_value_of.return_value = 1.0 # Assume all motor neurons output 1.0

        # Create mock motor objects
        self.robot.motors = {
            'Joint0': MagicMock(spec=sys.modules['src.motor'].Motor),
            'Joint1': MagicMock(spec=sys.modules['src.motor'].Motor)
        }
        
        time_step = 0 # 't' is not used by 'act' in current impl, but passed
        self.robot.act(time_step)
        
        # Check calls for Joint0
        self.robot.motors['Joint0'].set_value.assert_called_once_with(
            1.0 * c.MOTOR_JOINT_RANGE, # desired_angle
            self.robot.robot_id
        )
        # Check calls for Joint1
        self.robot.motors['Joint1'].set_value.assert_called_once_with(
            1.0 * c.MOTOR_JOINT_RANGE, # desired_angle
            self.robot.robot_id
        )
        # Ensure sensor neuron didn't cause issues
        self.assertEqual(self.robot.nn.is_motor_neuron.call_count, 3)


    def test_think(self):
        """
        Test that think calls update on the neural network.
        """
        self.robot.nn.update = MagicMock() # Ensure nn.update is a mock for this test
        self.robot.think()
        self.robot.nn.update.assert_called_once()

    @patch('src.robot.os.rename')
    @patch('src.robot.open', new_callable=mock_open)
    def test_get_fitness(self, mock_file_open, mock_os_rename):
        """
        Test that get_fitness retrieves position, writes to file, and renames.
        """
        mocked_x_position = 1.23
        self.mock_p.getBasePositionAndOrientation.return_value = ([mocked_x_position, 0, 0], [0,0,0,1])
        
        self.robot.get_fitness()
        
        self.mock_p.getBasePositionAndOrientation.assert_called_once_with(self.robot.robot_id)
        
        tmp_file = f'./src/data/tmp{self.solution_id}.txt'
        final_file = f'./src/data/fitness{self.solution_id}.txt'
        
        mock_file_open.assert_called_once_with(tmp_file, 'w')
        mock_file_open().write.assert_called_once_with(str(mocked_x_position))
        
        mock_os_rename.assert_called_once_with(tmp_file, final_file)

if __name__ == '__main__':
    unittest.main()
