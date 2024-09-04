from agents.ozzie import Ozzie

class AgentFactory:
    def __init__(self):
        self.agent_templates = {}

    def register_template(self, template_name, template_class):
        self.agent_templates[template_name] = template_class

    def create_agent(self, template_name, **kwargs):
        if template_name not in self.agent_templates:
            raise ValueError(f"Unknown agent template: {template_name}")
        
        agent_class = self.agent_templates[template_name]
        return agent_class(**kwargs)

    def create_ozzie(self):
        return Ozzie()

    def create_custom_agent(self, name, skills, goals):
        # Implement logic to create a custom agent with given parameters
        agent = Ozzie(name)  # For now, we're using Ozzie as a base
        for skill in skills:
            agent.add_skill(skill)
        agent.update_goals(goals)
        return agent