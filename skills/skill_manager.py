class SkillManager:
    def __init__(self):
        self.skills = {}

    def add_skill(self, skill_name, skill_object):
        self.skills[skill_name] = skill_object

    def remove_skill(self, skill_name):
        if skill_name in self.skills:
            del self.skills[skill_name]

    def get_skill(self, skill_name):
        return self.skills.get(skill_name)

    def list_skills(self):
        return list(self.skills.keys())

    def use_skill(self, skill_name, *args, **kwargs):
        skill = self.get_skill(skill_name)
        if skill:
            return skill.use(*args, **kwargs)
        else:
            raise ValueError(f"Skill not found: {skill_name}")