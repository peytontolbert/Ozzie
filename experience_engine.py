from chat_with_ollama import ChatGPT
from utils.logger import Logger
from utils.error_handler import ErrorHandler
import json
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.feature_extraction.text import TfidfVectorizer
from advanced_learning_module import AdvancedLearningModule
import random
from typing import Dict, List
from generalized_simulated_environment import GeneralizedSimulatedEnvironment, Agent, Obstacle, Resource
from autonomous_application import AutonomousApplication
import asyncio

class ExperienceEngine:
    def __init__(self, query_engine):
        self.scenario_types = [
            "technological", "environmental", "social", "economic", "political"
        ]
        self.complexity_levels = ["low", "medium", "high", "very high"]
        self.advanced_learning_module = AdvancedLearningModule()
        self.last_scenario = None
        self.last_action = None
        self.last_outcome = None
        self.logger = Logger("ExperienceEngine")
        self.error_handler = ErrorHandler()
        self.multi_modal_processor = MultiModalProcessor()
        self.chat_gpt = ChatGPT()  # Ensure this is properly initialized
        self.simulated_environment = GeneralizedSimulatedEnvironment()
        self.autonomous_applications = {}
        self.query_engine = query_engine

    def initialize(self):
        # Any initialization logic for the ExperienceEngine
        pass

    async def generate_scenario(self) -> Dict:
        scenario_type = random.choice(self.scenario_types)
        complexity = random.choice(self.complexity_levels)
        
        # Reset the environment for a new scenario
        self.simulated_environment = GeneralizedSimulatedEnvironment()

        # Generate scenario based on type
        if scenario_type == "delivery":
            self._generate_delivery_scenario(complexity)
        elif scenario_type == "exploration":
            self._generate_exploration_scenario(complexity)
        elif scenario_type == "resource_management":
            self._generate_resource_management_scenario(complexity)
        else:
            # Default scenario generation if type is not recognized
            self._generate_default_scenario(complexity)

        scenario = {
            "type": scenario_type,
            "complexity": complexity,
            "description": await self._generate_description(scenario_type, complexity),
            "environment_state": self.simulated_environment.get_environment_state(),
            "time_pressure": random.choice([True, False]),
            "uncertainty_level": random.uniform(0, 1),
            "actors": await self._generate_actors(complexity),
            "constraints": await self._generate_constraints(complexity)
        }
        
        self.logger.debug(f"Generated scenario: {scenario}")
        # Add scenario to graph database
        self.query_engine.add_entity(f"Scenario_{scenario['type']}_{scenario['complexity']}", scenario)
        
        return scenario

    def _generate_delivery_scenario(self, complexity):
        num_agents = {"low": 1, "medium": 2, "high": 3, "very high": 5}[complexity]
        num_packages = {"low": 2, "medium": 5, "high": 10, "very high": 20}[complexity]
        num_obstacles = {"low": 5, "medium": 10, "high": 20, "very high": 30}[complexity]

        for i in range(num_agents):
            agent = Agent(f"agent_{i}", self._random_position())
            self.simulated_environment.add_entity(agent)

        for i in range(num_packages):
            package = Resource(f"package_{i}", self._random_position(), "package")
            self.simulated_environment.add_entity(package)

        for i in range(num_obstacles):
            obstacle = Obstacle(f"obstacle_{i}", self._random_position(), random.uniform(1, 5))
            self.simulated_environment.add_entity(obstacle)

        self.simulated_environment.set_global_property("weather", self._generate_weather())

    def _generate_exploration_scenario(self, complexity):
        # Implement exploration scenario generation
        pass

    def _generate_resource_management_scenario(self, complexity):
        # Implement resource management scenario generation
        pass

    def _generate_default_scenario(self, complexity):
        num_entities = {"low": 5, "medium": 10, "high": 20, "very high": 30}[complexity]
        for i in range(num_entities):
            entity_type = random.choice([Agent, Obstacle, Resource])
            if entity_type == Agent:
                entity = entity_type(f"entity_{i}", self._random_position())
            elif entity_type == Obstacle:
                entity = entity_type(f"entity_{i}", self._random_position(), random.uniform(1, 5))
            else:  # Resource
                entity = entity_type(f"entity_{i}", self._random_position(), "default")
            self.simulated_environment.add_entity(entity)

    def _random_position(self):
        return tuple(random.uniform(0, s) for s in self.simulated_environment.size)

    def _generate_weather(self):
        return {
            "wind_speed": random.uniform(0, 20),
            "wind_direction": random.uniform(0, 360),
            "precipitation": random.choice(["none", "light", "moderate", "heavy"]),
            "visibility": random.uniform(0, 10)
        }

    async def _generate_description(self, scenario_type, complexity):
        prompt = f"Generate a brief description for a {complexity} complexity {scenario_type} scenario."
        response = await self.chat_gpt.chat_with_ollama(prompt)
        if response.startswith("Error:"):
            self.logger.warning(f"Failed to generate description: {response}")
            return f"A {complexity} complexity {scenario_type} scenario requiring innovative solutions and careful consideration of multiple factors."
        return response

    async def _generate_actors(self, complexity: str) -> List[Dict]:
        num_actors = {"low": 2, "medium": 3, "high": 5, "very high": 7}[complexity]
        actors = []
        for i in range(num_actors):
            actors.append({
                "id": f"actor_{i}",
                "type": random.choice(["individual", "organization", "government"]),
                "goals": await self._generate_goals(),
                "resources": random.randint(1, 10)
            })
        return actors

    async def _generate_goals(self) -> List[str]:
        prompt = "Generate two brief, general goals for an actor in a scenario."
        response = await self.chat_gpt.chat_with_ollama(prompt)
        if response.startswith("Error:"):
            self.logger.warning(f"Failed to generate goals: {response}")
            return ["Achieve primary objective while minimizing risks", "Optimize resource utilization for long-term sustainability"]
        goals = response.strip().split('\n')
        return goals[:2]  # Ensure we only return two goals

    async def _generate_constraints(self, complexity: str) -> List[str]:
        num_constraints = {"low": 1, "medium": 2, "high": 3, "very high": 4}[complexity]
        prompt = f"Generate {num_constraints} brief constraints for a {complexity} complexity scenario."
        response = await self.chat_gpt.chat_with_ollama(prompt)
        if response.startswith("Error:"):
            self.logger.warning(f"Failed to generate constraints: {response}")
            return [f"Adhere to {complexity} complexity guidelines and regulatory requirements",
                    "Operate within budget and resource limitations",
                    "Ensure ethical and sustainable practices",
                    "Maintain stakeholder satisfaction and engagement"][:num_constraints]
        constraints = response.strip().split('\n')
        return constraints[:num_constraints]

    async def evaluate_outcome(self, action: Dict, scenario: Dict) -> Dict:
        entity_id = action.get("entity_id")
        action_type = action.get("type")
        
        entity = self.simulated_environment.get_entity(entity_id)
        if not entity:
            return {"success": False, "message": "Entity not found"}

        if action_type == "move":
            new_position = tuple(a + b for a, b in zip(entity.position, action.get("direction")))
            if self.simulated_environment.is_position_valid(new_position):
                entity.position = new_position
                result = {"success": True, "message": "Moved successfully"}
            else:
                result = {"success": False, "message": "Invalid move"}
        elif action_type == "interact":
            target_id = action.get("target_id")
            target = self.simulated_environment.get_entity(target_id)
            if target:
                # Implement interaction logic here
                result = {"success": True, "message": f"Interacted with {target_id}"}
            else:
                result = {"success": False, "message": "Target not found"}
        else:
            result = {"success": False, "message": "Invalid action type"}

        self.simulated_environment.update()

        # Add action and outcome to graph database
        self.query_engine.add_entity(f"Action_{action['type']}", action)
        self.query_engine.add_entity(f"Outcome_{result['success']}", result)
        self.query_engine.add_relationship(f"Scenario_{scenario['type']}_{scenario['complexity']}", 
                                           f"Action_{action['type']}", "RESULTED_IN")
        self.query_engine.add_relationship(f"Action_{action['type']}", 
                                           f"Outcome_{result['success']}", "PRODUCED")
        
        return {
            "success": result["success"],
            "message": result["message"],
            "environment_state": self.simulated_environment.get_environment_state()
        }

    def _calculate_impact(self, action: Dict, result: Dict) -> Dict:
        # Implement a more sophisticated impact calculation based on the action and result
        return {
            "efficiency": random.uniform(-1, 1),
            "safety": random.uniform(-1, 1),
            "customer_satisfaction": random.uniform(-1, 1)
        }

    def _parse_json_response(self, response):
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            self.logger.warning("Failed to parse JSON response, returning raw text")
            return {"raw_text": response}

    def process_experience(self, experience_data):
        self.advanced_learning_module.learn(experience_data)
        self.multi_modal_processor.process(experience_data)

    async def create_autonomous_application(self, name, purpose):
        app = AutonomousApplication(name, purpose)
        self.autonomous_applications[name] = app
        asyncio.create_task(app.run())
        return f"Created autonomous application: {name}"

    async def list_autonomous_applications(self):
        return list(self.autonomous_applications.keys())

    async def get_autonomous_application_state(self, name):
        if name in self.autonomous_applications:
            return self.autonomous_applications[name].state
        return f"Application {name} not found"

    async def ozzie_create_autonomous_agent(self):
        prompt = f"As Ozzie, an AGI system, create a new autonomous agent. Provide a name and purpose for this agent."
        response = await self.chat_gpt.chat_with_ollama(prompt)
        try:
            agent_info = json.loads(response)
            name = agent_info.get('name', f"Agent_{len(self.autonomous_applications)}")
            purpose = agent_info.get('purpose', 'General purpose autonomous agent')
            return await self.create_autonomous_application(name, purpose)
        except json.JSONDecodeError:
            self.logger.error(f"Failed to parse agent creation response: {response}")
            return "Failed to create agent due to parsing error"

    async def ozzie_manage_agents(self):
        await self.create_hierarchical_agents(2, 3)  # Create 2 managers, each with 3 workers
        while True:
            prompt = f"As Ozzie, analyze the current autonomous agents: {await self.list_autonomous_applications()}. Should I create a new agent, modify an existing one, or take no action? Provide reasoning."
            response = await self.chat_gpt.chat_with_ollama(prompt)
            action = self._parse_ozzie_decision(response)
            
            if action == 'create':
                await self.ozzie_create_autonomous_agent()
            elif action == 'modify':
                await self._modify_existing_agent()
            else:
                self.logger.info("Ozzie decided to take no action at this time.")
            
            await asyncio.sleep(60)  # Wait for a minute before next management cycle

    def _parse_ozzie_decision(self, response):
        # Implement logic to parse Ozzie's decision from the response
        if "create" in response.lower():
            return 'create'
        elif "modify" in response.lower():
            return 'modify'
        else:
            return 'no_action'

    async def _modify_existing_agent(self):
        # Implement logic for Ozzie to modify an existing agent
        pass

    async def create_hierarchical_agents(self, num_managers, num_workers_per_manager):
        for i in range(num_managers):
            manager_name = f"Manager_{i}"
            manager_purpose = f"Manage a team of workers to achieve optimal performance"
            manager = AutonomousApplication(manager_name, manager_purpose, role="Manager")
            self.autonomous_applications[manager_name] = manager
            asyncio.create_task(manager.run())

            for j in range(num_workers_per_manager):
                worker_name = f"Worker_{i}_{j}"
                worker_purpose = f"Perform tasks assigned by the manager efficiently"
                worker = AutonomousApplication(worker_name, worker_purpose, role="Worker")
                self.autonomous_applications[worker_name] = worker
                asyncio.create_task(worker.run())

                manager.add_subordinate(worker_name)
                worker.set_manager(manager_name)

        self.logger.info(f"Created {num_managers} managers, each with {num_workers_per_manager} workers")

# Add new classes for advanced functionality
class AdvancedLearningModule:
    def __init__(self):
        self.model = self._initialize_model()
        self.optimizer = self._initialize_optimizer()
        self.criterion = nn.MSELoss()
        self.vectorizer = TfidfVectorizer()

    def _initialize_model(self):
        return nn.Sequential(
            nn.Linear(1000, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, 128)
        )

    def _initialize_optimizer(self):
        return optim.Adam(self.model.parameters(), lr=0.001)

    def learn(self, experience_data):
        features = self._extract_features(experience_data)
        self._update_model(features)

    def _extract_features(self, experience_data):
        text_data = experience_data.get('description', '')
        if not text_data.strip():
            self.logger.warning("Empty text data received for feature extraction")
            return torch.zeros(1, 1000)  # Return a zero tensor of appropriate size
        try:
            vectorized = self.vectorizer.fit_transform([text_data]).toarray()
            if vectorized.shape[1] == 0:
                self.logger.warning("TfidfVectorizer produced empty features. Using default features.")
                return torch.zeros(1, 1000)  # Return a zero tensor of appropriate size
            return torch.FloatTensor(vectorized)
        except ValueError as e:
            self.logger.error(f"Error in feature extraction: {str(e)}")
            return torch.zeros(1, 1000)  # Return a zero tensor of appropriate size

    def _update_model(self, features):
        self.optimizer.zero_grad()
        output = self.model(features)
        loss = self.criterion(output, torch.zeros_like(output))  # Assuming we want to minimize the output
        loss.backward()
        self.optimizer.step()

class MultiModalProcessor:
    def __init__(self):
        self.text_processor = TextProcessor()
        self.image_processor = ImageProcessor()
        self.audio_processor = AudioProcessor()

    def process(self, data):
        results = {}
        if 'text' in data:
            results['text'] = self.text_processor.process(data['text'])
        if 'image' in data:
            results['image'] = self.image_processor.process(data['image'])
        if 'audio' in data:
            results['audio'] = self.audio_processor.process(data['audio'])
        return results

class TextProcessor:
    def process(self, text):
        # Implement text processing logic
        return len(text.split())  # Simple word count as an example

class ImageProcessor:
    def process(self, image):
        # Implement image processing logic
        return {"size": len(image), "format": image[-3:]}  # Simple size and format check

class AudioProcessor:
    def process(self, audio):
        # Implement audio processing logic
        return {"duration": len(audio) / 1000}  # Assuming audio length in milliseconds