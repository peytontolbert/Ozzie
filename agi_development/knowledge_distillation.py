import numpy as np
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class KnowledgeDistillation:
    def __init__(self):
        self.logger = Logger("KnowledgeDistillation")
        self.error_handler = ErrorHandler()

    def distill_knowledge(self, teacher_model, student_model, data, temperature=1.0):
        try:
            teacher_outputs = teacher_model.predict(data)
            soft_targets = self._soften_probabilities(teacher_outputs, temperature)
            student_model.fit(data, soft_targets)
            self.logger.info("Knowledge distillation completed")
            return student_model
        except Exception as e:
            self.error_handler.handle_error(e, "Error during knowledge distillation")
            return None

    def _soften_probabilities(self, probabilities, temperature):
        try:
            softened = np.exp(np.log(probabilities) / temperature)
            return softened / np.sum(softened, axis=1, keepdims=True)
        except Exception as e:
            self.error_handler.handle_error(e, "Error softening probabilities")
            return None

    def evaluate_distillation(self, teacher_model, student_model, test_data):
        try:
            teacher_accuracy = self._calculate_accuracy(teacher_model, test_data)
            student_accuracy = self._calculate_accuracy(student_model, test_data)
            relative_performance = student_accuracy / teacher_accuracy
            self.logger.info(f"Relative performance of student model: {relative_performance}")
            return relative_performance
        except Exception as e:
            self.error_handler.handle_error(e, "Error evaluating distillation")
            return None

    def _calculate_accuracy(self, model, data):
        try:
            predictions = model.predict(data)
            accuracy = np.mean(np.argmax(predictions, axis=1) == np.argmax(data, axis=1))
            return accuracy
        except Exception as e:
            self.error_handler.handle_error(e, "Error calculating accuracy")
            return None

    def progressive_distillation(self, teacher_model, student_model, data_generator, num_iterations):
        try:
            for i in range(num_iterations):
                batch = next(data_generator)
                self.distill_knowledge(teacher_model, student_model, batch)
                if (i + 1) % 10 == 0:  # Log every 10 iterations
                    self.logger.info(f"Completed {i + 1} iterations of progressive distillation")
            return student_model
        except Exception as e:
            self.error_handler.handle_error(e, "Error during progressive distillation")
            return None