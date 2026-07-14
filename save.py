from database import Database


class SaveSystem:


    def __init__(self):

        self.db = Database()



    def new_game(self, player_name):

        # cria novo jogador

        self.db.create_player(
            player_name
        )


    def save_player(self, player):

        self.db.update_player(

            player.level,

            player.experience,

            player.health,

            player.energy

        )



    def load_player(self):

        data = self.db.get_player()

        return data



    def close(self):

        self.db.close()
