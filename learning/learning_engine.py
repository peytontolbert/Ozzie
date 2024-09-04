class LearningEngine:
    def __init__(self):
        self.experiences = []
        self.knowledge_base = {}

    def process_experience(self, experience):
        self.experiences.append(experience)
        # Implement logic to extract knowledge from experience
        self.update_knowledge_base(experience)

    def process_test_results(self, test_results):
        # Implement logic to learn from test results
        for result in test_results:
            self.update_knowledge_base(result)

    def update_knowledge_base(self, new_info):
        # Implement logic to update the knowledge base with new information
        # This is a simplified version; in a real system, this would be more complex
        if isinstance(new_info, dict):
            self.knowledge_base.update(new_info)
        else:
            self.knowledge_base[str(len(self.knowledge_base))] = new_info

    def get_relevant_knowledge(self, context):
        # Implement logic to retrieve relevant knowledge based on context
        # This is a simplified version; in a real system, this would use more advanced retrieval methods
        return {k: v for k, v in self.knowledge_base.items() if context in str(v)}