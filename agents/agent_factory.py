from agents.ozzie import Ozzie

class AgentFactory:
    def __init__(self):
        self.agent_templates = {}

    def register_template(self, template_name, template_class):
        self.agent_templates[template_name] = template_class

    def create_agent(self, spec):
        agent_type = spec.get('type', 'generic')
        if agent_type == 'coding':
            return self.create_coding_agent(spec)
        elif agent_type == 'analysis':
            return self.create_analysis_agent(spec)
        else:
            return self.create_generic_agent(spec)

    def create_coding_agent(self, spec):
        return CodingAgent(spec['name'], spec['specialization'])

    def create_analysis_agent(self, spec):
        return AnalysisAgent(spec['name'], spec['specialization'])

    def create_generic_agent(self, spec):
        return GenericAgent(spec['name'])

    def create_ozzie(self):
        return Ozzie()

    def create_custom_agent(self, name, skills, goals):
        # Implement logic to create a custom agent with given parameters
        agent = Ozzie(name)  # For now, we're using Ozzie as a base
        for skill in skills:
            agent.add_skill(skill)
        agent.update_goals(goals)
        return agent

class BaseAgent:
    def __init__(self, name):
        self.name = name

    def receive_message(self, message, sender):
        print(f"{self.name} received message from {sender}: {message}")
        # Implement logic to process the message

class CodingAgent(BaseAgent):
    def __init__(self, name, specialization):
        super().__init__(name)
        self.specialization = specialization

class AnalysisAgent(BaseAgent):
    def __init__(self, name, specialization):
        super().__init__(name)
        self.specialization = specialization

class GenericAgent(BaseAgent):
    pass