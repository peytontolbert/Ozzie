import unittest
from unittest.mock import MagicMock, patch
from virtual_environment import VirtualEnvironment

class TestVirtualEnvironment(unittest.TestCase):
    def setUp(self):
        self.ve = VirtualEnvironment()

    def test_initialization(self):
        self.assertIsNotNone(self.ve.main_menu)
        self.assertIsNotNone(self.ve.agent_manager)
        self.assertIsNotNone(self.ve.experience_engine)
        self.assertIsNone(self.ve.current_agent)

    @patch('builtins.input', side_effect=['TestAgent'])
    def test_handle_selection_create_agent(self, mock_input):
        self.ve.handle_selection("create_agent")
        self.assertIsNotNone(self.ve.current_agent)
        self.assertEqual(self.ve.current_agent.name, "TestAgent")

    @patch('builtins.input', side_effect=['TestAgent'])
    def test_handle_selection_load_agent(self, mock_input):
        # First, create an agent
        self.ve.handle_selection("create_agent")
        # Then, load the agent
        self.ve.current_agent = None
        self.ve.handle_selection("load_agent")
        self.assertIsNotNone(self.ve.current_agent)
        self.assertEqual(self.ve.current_agent.name, "TestAgent")

    @patch('builtins.input', side_effect=['test_action'])
    def test_run_scenario(self, mock_input):
        self.ve.current_agent = MagicMock()
        self.ve.experience_engine.generate_scenario = MagicMock(return_value="Test scenario")
        self.ve.experience_engine.evaluate_outcome = MagicMock(return_value="Test outcome")
        
        self.ve.run_scenario()
        
        self.ve.current_agent.learn.assert_called_once()
        self.ve.experience_engine.generate_scenario.assert_called_once()
        self.ve.experience_engine.evaluate_outcome.assert_called_once()

    @patch('builtins.print')
    async def test_process_cycle(self, mock_print):
        self.ve.current_agent = MagicMock()
        await self.ve.process_cycle({"result": "test"}, "Test explanation")
        self.ve.current_agent.learn.assert_called_once()
        mock_print.assert_called()

if __name__ == '__main__':
    unittest.main()