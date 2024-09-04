import random
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class IdeaGenerator:
    def __init__(self, knowledge_graph):
        self.knowledge_graph = knowledge_graph
        self.logger = Logger("IdeaGenerator")
        self.error_handler = ErrorHandler()

    def generate_random_idea(self):
        try:
            concepts = self.knowledge_graph.get_all_concepts()
            if not concepts:
                return "No concepts available to generate ideas."
            
            concept1, concept2 = random.sample(concepts, 2)
            return f"How about combining {concept1} with {concept2}?"
        except Exception as e:
            self.error_handler.handle_error(e, "Error generating random idea")
            return "Failed to generate idea."

    def generate_idea_from_topic(self, topic):
        try:
            related_concepts = self.knowledge_graph.get_related_concepts(topic)
            if not related_concepts:
                return f"No related concepts found for {topic}."
            
            random_concept = random.choice(related_concepts)
            return f"Consider exploring the relationship between {topic} and {random_concept}."
        except Exception as e:
            self.error_handler.handle_error(e, f"Error generating idea from topic: {topic}")
            return "Failed to generate idea from topic."

    def generate_innovative_workflow(self):
        try:
            all_steps = self.knowledge_graph.get_all_workflow_steps()
            if len(all_steps) < 3:
                return "Not enough workflow steps to generate an innovative workflow."
            
            selected_steps = random.sample(all_steps, 3)
            return f"Try creating a workflow with these steps: {' -> '.join(selected_steps)}"
        except Exception as e:
            self.error_handler.handle_error(e, "Error generating innovative workflow")
            return "Failed to generate innovative workflow."