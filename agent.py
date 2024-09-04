from agent_systems import MemorySystem, SkillSystem, GoalSystem

class Agent:
    def __init__(self, name):
        self.name = name
        self.memory = MemorySystem()
        self.skills = SkillSystem()
        self.goals = GoalSystem()

    def perform_action(self, action):
        # Implement action execution logic
        print(f"Agent {self.name} performing action: {action}")
        skill = self.skills.get_skill(action)
        if skill:
            return skill.execute()
        else:
            return f"Action {action} not supported"

    def learn(self, experience):
        # Process and integrate new experience
        self.memory.store(experience)
        self.skills.learn_from_experience(experience)
        self.goals.update_from_experience(experience)

    def update_goals(self, new_goals):
        self.goals.set_goals(new_goals)

    def get_status(self):
        return {
            "name": self.name,
            "skills": self.skills.get_all_skills(),
            "goals": self.goals.get_current_goals(),
            "memory_size": self.memory.get_size()
        }