class Mission:


    def __init__(self, name, description, reward):

        self.name = name

        self.description = description

        self.reward = reward

        self.completed = False



    def complete(self):

        self.completed = True



    def status(self):

        if self.completed:

            return "Concluída"

        return "Em andamento"



class MissionSystem:


    def __init__(self):

        self.missions = []



    def add_mission(self, mission):

        self.missions.append(
            mission
        )



    def complete_mission(self, name):

        for mission in self.missions:

            if mission.name == name:

                mission.complete()



    def get_active(self):

        active = []

        for mission in self.missions:

            if not mission.completed:

                active.append(
                    mission
                )

        return active



    def get_completed(self):

        completed = []

        for mission in self.missions:

            if mission.completed:

                completed.append(
                    mission
                )

        return completed



# ============================
# MISSÕES INICIAIS
# ============================


def create_first_missions():

    missions = MissionSystem()


    missions.add_mission(

        Mission(
            "Primeiro Contato",
            "Elimine 10 alienígenas que saíram da nave.",
            100
        )

    )


    missions.add_mission(

        Mission(
            "Sobrevivente",
            "Encontre sobreviventes na cidade destruída.",
            250
        )

    )


    missions.add_mission(

        Mission(
            "Tecnologia Perdida",
            "Recupere um chip alienígena.",
            500
        )

    )


    return missions
