import numpy as np
from utils.logger import Logger
from utils.error_handler import ErrorHandler

class MultiModalProcessor:
    def __init__(self):
        self.logger = Logger("MultiModalProcessor")
        self.error_handler = ErrorHandler()
        self.modalities = {}

    def register_modality(self, modality_name, processing_function):
        try:
            self.modalities[modality_name] = processing_function
            self.logger.info(f"Registered modality: {modality_name}")
        except Exception as e:
            self.error_handler.handle_error(e, f"Error registering modality: {modality_name}")

    def process_input(self, modality, input_data):
        try:
            if modality not in self.modalities:
                raise ValueError(f"Unregistered modality: {modality}")
            
            processed_data = self.modalities[modality](input_data)
            return processed_data
        except Exception as e:
            self.error_handler.handle_error(e, f"Error processing input for modality: {modality}")
            return None

    def fuse_modalities(self, processed_inputs):
        try:
            # This is a simple fusion method. In a more advanced system, 
            # this could involve more sophisticated techniques like attention mechanisms.
            fused_representation = np.mean([input_data for input_data in processed_inputs if input_data is not None], axis=0)
            return fused_representation
        except Exception as e:
            self.error_handler.handle_error(e, "Error fusing modalities")
            return None

    def process_multi_modal_input(self, inputs):
        try:
            processed_inputs = {}
            for modality, input_data in inputs.items():
                processed_inputs[modality] = self.process_input(modality, input_data)
            
            fused_representation = self.fuse_modalities(processed_inputs.values())
            return fused_representation
        except Exception as e:
            self.error_handler.handle_error(e, "Error processing multi-modal input")
            return None