class Skill:
    def __init__(self, name, execute_func):
        self.name = name
        self.execute_func = execute_func

    def execute(self):
        return self.execute_func()

class SkillSystem:
    def __init__(self):
        self.skills = {}

    def add_skill(self, skill):
        self.skills[skill.name] = skill

    def get_skill(self, skill_name):
        return self.skills.get(skill_name)

    def learn_from_experience(self, experience):
        # Simplified learning logic
        if "action" in experience and "outcome" in experience:
            self.add_skill(Skill(experience["action"], lambda: experience["outcome"]))

    def get_all_skills(self):
        return list(self.skills.keys())

class MemorySystem:
    def __init__(self):
        self.memories = []

    def store(self, memory):
        self.memories.append(memory)

    def retrieve(self, query):
        # Simplified retrieval logic
        return [m for m in self.memories if query in str(m)]

    def get_size(self):
        return len(self.memories)

class GoalSystem:
    def __init__(self):
        self.goals = []

    def set_goals(self, goals):
        self.goals = goals

    def update_from_experience(self, experience):
        # Simplified goal updating logic
        if "outcome" in experience and experience["outcome"] == "success":
            self.goals.append(f"Repeat {experience['action']}")

    def get_current_goals(self):
        return self.goals