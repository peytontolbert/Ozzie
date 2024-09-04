import random
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class ConsciousnessSimulator:
    def __init__(self):
        self.logger = Logger("ConsciousnessSimulator")
        self.error_handler = ErrorHandler()
        self.attention_focus = None
        self.working_memory = []
        self.long_term_memory = {}
        self.emotional_state = "neutral"

    def set_attention(self, focus):
        try:
            self.attention_focus = focus
            self.logger.info(f"Attention set to: {focus}")
        except Exception as e:
            self.error_handler.handle_error(e, "Error setting attention")

    def update_working_memory(self, item):
        try:
            if len(self.working_memory) >= 7:  # Miller's Law: 7 ± 2 items
                self.working_memory.pop(0)
            self.working_memory.append(item)
        except Exception as e:
            self.error_handler.handle_error(e, "Error updating working memory")

    def store_in_long_term_memory(self, key, value):
        try:
            self.long_term_memory[key] = value
            self.logger.info(f"Stored in long-term memory: {key}")
        except Exception as e:
            self.error_handler.handle_error(e, f"Error storing in long-term memory: {key}")

    def retrieve_from_long_term_memory(self, key):
        try:
            return self.long_term_memory.get(key)
        except Exception as e:
            self.error_handler.handle_error(e, f"Error retrieving from long-term memory: {key}")
            return None

    def set_emotional_state(self, state):
        try:
            self.emotional_state = state
            self.logger.info(f"Emotional state set to: {state}")
        except Exception as e:
            self.error_handler.handle_error(e, "Error setting emotional state")

    def generate_thought(self):
        try:
            thought_sources = [self.attention_focus] + self.working_memory + list(self.long_term_memory.values())
            thought = f"Thinking about {random.choice(thought_sources)} with {self.emotional_state} emotion"
            return thought
        except Exception as e:
            self.error_handler.handle_error(e, "Error generating thought")
            return "Error in thought generation"

    def simulate_consciousness_stream(self, duration):
        try:
            consciousness_stream = []
            for _ in range(duration):
                thought = self.generate_thought()
                consciousness_stream.append(thought)
                self.update_working_memory(thought)
            return consciousness_stream
        except Exception as e:
            self.error_handler.handle_error(e, "Error simulating consciousness stream")
            return []