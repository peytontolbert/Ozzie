from chat_with_ollama import ChatGPT
from utils.logger import Logger
from utils.error_handler import ErrorHandler
import json
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.feature_extraction.text import TfidfVectorizer
from advanced_learning_module import AdvancedLearningModule

class ExperienceEngine:
    def __init__(self):
        self.advanced_learning_module = AdvancedLearningModule()
        self.last_scenario = None
        self.last_action = None
        self.last_outcome = None
        self.logger = Logger("ExperienceEngine")
        self.error_handler = ErrorHandler()
        self.multi_modal_processor = MultiModalProcessor()
        self.chat_gpt = ChatGPT()  # Make sure this is properly initialized

    def initialize(self):
        # Any initialization logic for the ExperienceEngine
        pass

    async def generate_scenario(self):
        try:
            system_prompt = "You are an AI that generates challenging scenarios for AI agents. Generate a scenario in JSON format with 'description' and 'difficulty' fields."
            prompt = "Create a challenging scenario for an AI agent to solve."
            
            response = await self.chat_gpt.chat_with_ollama(system_prompt, prompt)
            self.last_scenario = self._parse_json_response(response)
            return self.last_scenario
        except Exception as e:
            self.error_handler.handle_error(e, "Error generating scenario")
            return None

    async def evaluate_outcome(self, action, scenario):
        try:
            self.last_action = action
            system_prompt = "You are an AI that evaluates outcomes of actions in given scenarios. Evaluate the following and respond in JSON format with 'outcome' and 'score' fields."
            prompt = f"Scenario: {scenario}\nAction: {action}\nEvaluate the outcome:"
            
            response = await self.chat_gpt.chat_with_ollama(system_prompt, prompt)
            self.last_outcome = self._parse_json_response(response)
            return self.last_outcome
        except Exception as e:
            self.error_handler.handle_error(e, "Error evaluating outcome")
            return None

    def _parse_json_response(self, response):
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            self.logger.warning("Failed to parse JSON response, returning raw text")
            return {"raw_text": response}

    def process_experience(self, experience_data):
        self.advanced_learning_module.learn(experience_data)
        self.multi_modal_processor.process(experience_data)

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