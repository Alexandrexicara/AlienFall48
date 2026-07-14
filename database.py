import sqlite3

from config import DATABASE


class Database:


    def __init__(self):

        self.connection = sqlite3.connect(
            DATABASE
        )

        self.cursor = self.connection.cursor()

        self.create_tables()



    def create_tables(self):


        # Jogador

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS player (

            id INTEGER PRIMARY KEY,

            name TEXT,

            level INTEGER DEFAULT 1,

            experience INTEGER DEFAULT 0,

            health INTEGER DEFAULT 100,

            energy INTEGER DEFAULT 100

        )
        """)



        # Inventário

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (

            id INTEGER PRIMARY KEY,

            player_id INTEGER,

            item TEXT,

            amount INTEGER DEFAULT 1

        )
        """)



        # Armas

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS weapons (

            id INTEGER PRIMARY KEY,

            player_id INTEGER,

            weapon TEXT,

            level INTEGER DEFAULT 1

        )
        """)



        # Missões

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS missions (

            id INTEGER PRIMARY KEY,

            player_id INTEGER,

            mission TEXT,

            completed INTEGER DEFAULT 0

        )
        """)



        self.connection.commit()



    def create_player(self,name):

        self.cursor.execute(
            """
            INSERT INTO player(name)
            VALUES(?)
            """,
            (name,)
        )


        self.connection.commit()



    def get_player(self):

        self.cursor.execute(
            """
            SELECT *
            FROM player
            LIMIT 1
            """
        )

        return self.cursor.fetchone()



    def update_player(
            self,
            level,
            experience,
            health,
            energy
        ):


        self.cursor.execute(
            """
            UPDATE player

            SET level=?,
                experience=?,
                health=?,
                energy=?

            WHERE id=1

            """,
            (
                level,
                experience,
                health,
                energy
            )
        )


        self.connection.commit()



    def close(self):

        self.connection.close()
