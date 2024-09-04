import numpy as np
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class SelfOrganizationSimulator:
    def __init__(self, num_agents, environment_size):
        self.logger = Logger("SelfOrganizationSimulator")
        self.error_handler = ErrorHandler()
        self.num_agents = num_agents
        self.environment_size = environment_size
        self.agents = np.random.rand(num_agents, 2) * environment_size
        self.agent_properties = np.random.rand(num_agents)

    def update_agents(self):
        try:
            for i in range(self.num_agents):
                # Simple flocking behavior
                neighbors = self.find_neighbors(i)
                if len(neighbors) > 0:
                    center = np.mean(self.agents[neighbors], axis=0)
                    direction = center - self.agents[i]
                    self.agents[i] += direction * 0.01
                
                # Add some random movement
                self.agents[i] += np.random.randn(2) * 0.1
                
                # Ensure agents stay within the environment
                self.agents[i] = np.clip(self.agents[i], 0, self.environment_size)
        except Exception as e:
            self.error_handler.handle_error(e, "Error updating agents")

    def find_neighbors(self, agent_index, radius=1.0):
        try:
            distances = np.linalg.norm(self.agents - self.agents[agent_index], axis=1)
            return np.where((distances < radius) & (distances > 0))[0]
        except Exception as e:
            self.error_handler.handle_error(e, "Error finding neighbors")
            return []

    def simulate(self, num_steps):
        try:
            for _ in range(num_steps):
                self.update_agents()
            self.logger.info(f"Completed {num_steps} simulation steps")
        except Exception as e:
            self.error_handler.handle_error(e, "Error during simulation")

    def calculate_order_parameter(self):
        try:
            velocities = np.diff(self.agents, axis=0)
            avg_velocity = np.mean(velocities, axis=0)
            order = np.linalg.norm(avg_velocity) / np.mean(np.linalg.norm(velocities, axis=1))
            return order
        except Exception as e:
            self.error_handler.handle_error(e, "Error calculating order parameter")
            return None

    def detect_clusters(self, threshold=1.0):
        try:
            clusters = []
            unassigned = set(range(self.num_agents))
            while unassigned:
                current = unassigned.pop()
                cluster = {current}
                to_check = self.find_neighbors(current, threshold)
                while to_check:
                    neighbor = to_check.pop()
                    if neighbor in unassigned:
                        unassigned.remove(neighbor)
                        cluster.add(neighbor)
                        to_check.extend(self.find_neighbors(neighbor, threshold))
                clusters.append(cluster)
            return clusters
        except Exception as e:
            self.error_handler.handle_error(e, "Error detecting clusters")
            return []

    def analyze_emergent_behavior(self):
        try:
            order = self.calculate_order_parameter()
            clusters = self.detect_clusters()
            avg_cluster_size = np.mean([len(c) for c in clusters]) if clusters else 0
            
            return {
                'order_parameter': order,
                'num_clusters': len(clusters),
                'avg_cluster_size': avg_cluster_size
            }
        except Exception as e:
            self.error_handler.handle_error(e, "Error analyzing emergent behavior")
            return {}