import unittest
from base.base_agent import BaseAgent
from base.base_workflow import BaseWorkflow
from workflows.workflow_engine import WorkflowEngine
from knowledge_graph.graph_structure import GraphStructure

class TestBaseAgent(unittest.TestCase):
    def setUp(self):
        self.agent = BaseAgent("TestAgent")

    def test_add_skill(self):
        self.agent.add_skill("test_skill")
        self.assertIn("test_skill", self.agent.skills)

    def test_remove_skill(self):
        self.agent.add_skill("test_skill")
        self.agent.remove_skill("test_skill")
        self.assertNotIn("test_skill", self.agent.skills)

    def test_set_get_memory(self):
        self.agent.set_memory("key", "value")
        self.assertEqual(self.agent.get_memory("key"), "value")

class TestBaseWorkflow(unittest.TestCase):
    def setUp(self):
        self.workflow = BaseWorkflow("TestWorkflow")

    def test_add_step(self):
        def test_step():
            pass
        self.workflow.add_step(test_step)
        self.assertIn(test_step, self.workflow.steps)

    def test_remove_step(self):
        def test_step():
            pass
        self.workflow.add_step(test_step)
        self.workflow.remove_step(test_step)
        self.assertNotIn(test_step, self.workflow.steps)

class TestWorkflowEngine(unittest.TestCase):
    def setUp(self):
        self.engine = WorkflowEngine()

    def test_register_workflow(self):
        workflow = BaseWorkflow("TestWorkflow")
        self.engine.register_workflow("test", workflow)
        self.assertIn("test", self.engine.workflows)

    def test_execute_workflow(self):
        class TestWorkflow(BaseWorkflow):
            def execute(self):
                return "Executed"
        
        workflow = TestWorkflow("TestWorkflow")
        self.engine.register_workflow("test", workflow)
        result = self.engine.execute_workflow("test")
        self.assertEqual(result, ["Executed"])

class TestGraphStructure(unittest.TestCase):
    def setUp(self):
        self.graph = GraphStructure("bolt://localhost:7687", "neo4j", "password")

    def test_create_node(self):
        node_id = self.graph.create_node("TestNode", {"prop": "value"})
        self.assertIsNotNone(node_id)

    def test_create_relationship(self):
        node1_id = self.graph.create_node("TestNode1", {})
        node2_id = self.graph.create_node("TestNode2", {})
        rel_type = self.graph.create_relationship(node1_id, node2_id, "TEST_REL")
        self.assertEqual(rel_type, "TEST_REL")

if __name__ == '__main__':
    unittest.main()