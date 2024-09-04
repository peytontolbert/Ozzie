import unittest
from agent import Agent
from agent_systems import SkillSystem, MemorySystem, GoalSystem

class TestAgent(unittest.TestCase):
    def setUp(self):
        self.agent = Agent("TestAgent")

    def test_agent_initialization(self):
        self.assertEqual(self.agent.name, "TestAgent")
        self.assertIsInstance(self.agent.memory, MemorySystem)
        self.assertIsInstance(self.agent.skills, SkillSystem)
        self.assertIsInstance(self.agent.goals, GoalSystem)

    def test_perform_action(self):
        result = self.agent.perform_action("test_action")
        self.assertEqual(result, "Action test_action not supported")

        # Add a skill and test again
        self.agent.skills.add_skill(lambda: "Skill executed")
        result = self.agent.perform_action("test_action")
        self.assertEqual(result, "Skill executed")

    def test_learn(self):
        experience = {"action": "test_action", "outcome": "success"}
        self.agent.learn(experience)
        self.assertEqual(len(self.agent.memory.memories), 1)
        self.assertIn("test_action", self.agent.skills.get_all_skills())

    def test_update_goals(self):
        new_goals = ["Goal 1", "Goal 2"]
        self.agent.update_goals(new_goals)
        self.assertEqual(self.agent.goals.get_current_goals(), new_goals)

    def test_get_status(self):
        status = self.agent.get_status()
        self.assertIn("name", status)
        self.assertIn("skills", status)
        self.assertIn("goals", status)
        self.assertIn("memory_size", status)

if __name__ == '__main__':
    unittest.main()