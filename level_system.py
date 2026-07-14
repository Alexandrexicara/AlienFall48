class LevelSystem:


    def __init__(self):

        self.level = 1

        self.experience = 0

        self.next_level_xp = 100



    def add_xp(self, amount):

        self.experience += amount


        if self.experience >= self.next_level_xp:

            self.level_up()



    def level_up(self):

        self.level += 1

        self.experience = 0

        self.next_level_xp += 150



    def get_level(self):

        return self.level



    def get_xp(self):

        return self.experience



    def get_next_xp(self):

        return self.next_level_xp



# =========================
# HABILIDADES
# =========================


class SkillTree:


    def __init__(self):

        self.skills = {


            "forca": 0,

            "velocidade": 0,

            "defesa": 0,

            "energia": 0,

            "tecnologia": 0

        }



    def upgrade(self, skill):


        if skill in self.skills:

            self.skills[skill] += 1



    def get_skills(self):

        return self.skills
