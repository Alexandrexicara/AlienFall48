import pygame
import os


class Alien:

    def __init__(
        self,
        name,
        image,
        health,
        speed,
        damage,
        ability
    ):

        self.name = name

        self.health = health

        self.speed = speed

        self.damage = damage

        self.ability = ability


        self.image = pygame.image.load(

            os.path.join(
                "assets",
                "enemies",
                image
            )

        ).convert_alpha()



# =========================
# ALIENÍGENAS
# =========================


class AlienDrone(Alien):

    def __init__(self):

        super().__init__(
            "Drone Alien",
            "alien_drone.png",
            80,
            350,
            15,
            "Ataque rápido"
        )



class AlienBrute(Alien):

    def __init__(self):

        super().__init__(
            "Alien Bruto",
            "alien_brute.png",
            800,
            90,
            80,
            "Golpe pesado"
        )



class AlienSpider(Alien):

    def __init__(self):

        super().__init__(
            "Aranha Alien",
            "alien_spider.png",
            250,
            220,
            40,
            "Escalar paredes"
        )



class AlienParasite(Alien):

    def __init__(self):

        super().__init__(
            "Parasita Alien",
            "alien_parasite.png",
            120,
            300,
            30,
            "Ataque surpresa"
        )



class AlienQueen(Alien):

    def __init__(self):

        super().__init__(
            "Rainha Alien",
            "alien_queen.png",
            10000,
            70,
            150,
            "Invoca tropas alienígenas"
        )
