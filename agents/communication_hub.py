class CommunicationHub:
    def __init__(self):
        self.agents = {}

    def register_agent(self, agent):
        self.agents[agent.name] = agent

    def send_message(self, message, sender, recipients):
        for recipient in recipients:
            if recipient in self.agents:
                self.agents[recipient].receive_message(message, sender)
            else:
                print(f"Warning: Agent {recipient} not found.")

    def broadcast_message(self, message, sender):
        for agent_name, agent in self.agents.items():
            if agent_name != sender:
                agent.receive_message(message, sender)