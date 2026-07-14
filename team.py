class Team:


    def __init__(self, name):

        self.name = name

        self.members = []

        self.max_members = 4



    def add_player(self, player):

        if len(self.members) < self.max_members:

            self.members.append(
                player
            )

            return True


        return False



    def remove_player(self, player):

        if player in self.members:

            self.members.remove(
                player
            )



    def get_members(self):

        return self.members



    def size(self):

        return len(
            self.members
        )



    def clear(self):

        self.members.clear()



class TeamManager:


    def __init__(self):

        self.teams = []



    def create_team(self, name):

        team = Team(
            name
        )

        self.teams.append(
            team
        )

        return team



    def merge_teams(self, team1, team2):

        new_team = Team(

            team1.name +
            " + " +
            team2.name

        )


        for player in team1.members:

            new_team.add_player(
                player
            )


        for player in team2.members:

            new_team.add_player(
                player
            )


        return new_team
