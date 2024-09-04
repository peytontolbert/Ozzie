import time
from base.base_workflow import BaseWorkflow
from concurrent.futures import ThreadPoolExecutor, as_completed

class WorkflowOptimizer:
    def __init__(self, workflow_engine):
        self.workflow_engine = workflow_engine

    def optimize_workflow(self, workflow):
        if not isinstance(workflow, BaseWorkflow):
            raise ValueError(f"Expected BaseWorkflow, got {type(workflow)}")

        optimized_steps = []
        step_times = []

        for step in workflow.steps:
            start_time = time.time()
            try:
                step()
            except Exception as e:
                print(f"Error executing step: {e}")
                continue
            end_time = time.time()
            step_times.append((step, end_time - start_time))

        # Sort steps by execution time (ascending)
        sorted_steps = sorted(step_times, key=lambda x: x[1])

        # Attempt to parallelize or optimize steps
        for step, _ in sorted_steps:
            if self.can_parallelize(step, optimized_steps):
                optimized_steps.append((step, "parallel"))
            else:
                optimized_steps.append((step, "sequential"))

        return self.create_optimized_workflow(workflow.name, optimized_steps)

    def can_parallelize(self, step, existing_steps):
        # This is a simplified check. In a real system, you'd need to analyze
        # dependencies between steps to determine if they can run in parallel.
        return len(existing_steps) > 0 and existing_steps[-1][1] == "sequential"

    def create_optimized_workflow(self, original_name, optimized_steps):
        class OptimizedWorkflow(BaseWorkflow):
            def __init__(self, name, steps):
                super().__init__(name)
                self.steps = steps

            def execute(self):
                results = []
                parallel_steps = []

                with ThreadPoolExecutor() as executor:
                    futures = []
                    for step, execution_type in self.steps:
                        if execution_type == "parallel":
                            parallel_steps.append(step)
                        else:
                            if parallel_steps:
                                # Execute parallel steps
                                futures.extend([executor.submit(s) for s in parallel_steps])
                                parallel_steps = []
                            futures.append(executor.submit(step))

                    # Execute any remaining parallel steps
                    if parallel_steps:
                        futures.extend([executor.submit(s) for s in parallel_steps])

                    # Collect results
                    for future in as_completed(futures):
                        try:
                            result = future.result()
                            results.append(result)
                        except Exception as e:
                            results.append(f"Error: {str(e)}")

                return results

        return OptimizedWorkflow(f"{original_name}_optimized", [s[0] for s in optimized_steps])