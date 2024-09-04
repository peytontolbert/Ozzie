import time
import statistics
from workflows.workflow_engine import WorkflowEngine
from knowledge_graph.graph_structure import GraphStructure
from cosmic_web.web_structure import WebStructure

def benchmark(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"{func.__name__} executed in {execution_time:.4f} seconds")
        return result, execution_time
    return wrapper

class PerformanceBenchmarks:
    def __init__(self):
        self.workflow_engine = WorkflowEngine()
        self.graph = GraphStructure("bolt://localhost:7687", "neo4j", "password")
        self.web = WebStructure(self.graph)

    @benchmark
    def benchmark_workflow_execution(self, workflow_name, num_executions=100):
        execution_times = []
        for _ in range(num_executions):
            _, execution_time = self.workflow_engine.execute_workflow(workflow_name)
            execution_times.append(execution_time)
        
        avg_time = statistics.mean(execution_times)
        print(f"Average execution time for {workflow_name}: {avg_time:.4f} seconds")
        return avg_time

    @benchmark
    def benchmark_knowledge_graph_query(self, query, num_executions=100):
        execution_times = []
        for _ in range(num_executions):
            _, execution_time = self.graph.execute_query(query)
            execution_times.append(execution_time)
        
        avg_time = statistics.mean(execution_times)
        print(f"Average query execution time: {avg_time:.4f} seconds")
        return avg_time

    @benchmark
    def benchmark_web_structure_operations(self, num_operations=1000):
        start_time = time.time()
        for i in range(num_operations):
            concept_id = self.web.add_concept(f"Concept{i}", {"prop": f"value{i}"})
            if i > 0:
                self.web.add_relationship(concept_id - 1, concept_id, "RELATED_TO")
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Web structure operations: {num_operations} in {total_time:.4f} seconds")
        return total_time

if __name__ == '__main__':
    benchmarks = PerformanceBenchmarks()
    
    # Example usage:
    benchmarks.benchmark_workflow_execution("SomeWorkflow")
    benchmarks.benchmark_knowledge_graph_query("MATCH (n) RETURN n LIMIT 100")
    benchmarks.benchmark_web_structure_operations()