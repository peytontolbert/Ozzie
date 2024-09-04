import unittest
from agents.ozzie import Ozzie
from workflows.workflow_engine import WorkflowEngine
from knowledge_graph.graph_structure import GraphStructure
from cosmic_web.web_structure import WebStructure

class TestOzzieScenarios(unittest.TestCase):
    def setUp(self):
        self.ozzie = Ozzie()
        self.workflow_engine = WorkflowEngine()
        self.graph = GraphStructure("bolt://localhost:7687", "neo4j", "password")
        self.web = WebStructure(self.graph)

    def test_ozzie_learns_and_creates_workflow(self):
        # Scenario: Ozzie learns a new concept and creates a workflow based on it
        
        # Step 1: Ozzie learns a new concept
        concept_id = self.web.add_concept("MachineLearning", {"field": "AI"})
        self.ozzie.learn({"concept_id": concept_id, "name": "MachineLearning", "details": "A subset of AI"})
        
        # Step 2: Ozzie creates a workflow based on the learned concept
        workflow = self.ozzie.create_workflow("MLWorkflow")
        self.workflow_engine.register_workflow("ML", workflow)
        
        # Step 3: Execute the workflow
        result = self.workflow_engine.execute_workflow("ML")
        
        # Assertions
        self.assertIsNotNone(workflow)
        self.assertIn("MachineLearning", str(result))

    def test_ozzie_optimizes_existing_workflow(self):
        # Scenario: Ozzie optimizes an existing workflow
        
        # Step 1: Create an initial workflow
        def step1():
            return "Step 1"
        def step2():
            return "Step 2"
        
        initial_workflow = self.ozzie.create_workflow("InitialWorkflow", [step1, step2])
        self.workflow_engine.register_workflow("initial", initial_workflow)
        
        # Step 2: Ozzie optimizes the workflow
        optimized_workflow = self.ozzie.optimize_workflow("initial")
        self.workflow_engine.register_workflow("optimized", optimized_workflow)
        
        # Step 3: Execute both workflows and compare
        initial_result = self.workflow_engine.execute_workflow("initial")
        optimized_result = self.workflow_engine.execute_workflow("optimized")
        
        # Assertions
        self.assertEqual(initial_result, optimized_result)
        self.assertIsNotNone(optimized_workflow)

if __name__ == '__main__':
    unittest.main()