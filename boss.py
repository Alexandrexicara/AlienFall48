import pygame
import math

from config import *


class Boss:


    def __init__(self, x, y, name):

        self.x = float(x)
        self.y = float(y)

        self.name = name

        self.width = 120
        self.height = 120

        self.speed = 80

        self.health = 1000
        self.max_health = 1000

        self.damage = 25

        self.color = (150, 0, 150)

        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )


    def update(self, player, dt):

        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery

        distance = math.hypot(dx, dy)


        if distance > 0:

            dx /= distance
            dy /= distance

            self.x += dx * self.speed * dt
            self.y += dy * self.speed * dt


        self.rect.x = int(self.x)
        self.rect.y = int(self.y)



    def take_damage(self, damage):

        self.health -= damage



    def alive(self):

        return self.health > 0



    def draw(self, screen, camera):

        pos = camera.apply(self)


        # corpo do chefe

        pygame.draw.rect(

            screen,

            self.color,

            pos,

            border_radius=20

        )


        # barra de vida gigante

        bar_width = 400


        pygame.draw.rect(

            screen,

            RED,

            (
                WIDTH//2 - bar_width//2,
                30,
                bar_width,
                25
            )

        )


        pygame.draw.rect(

            screen,

            GREEN,

            (
                WIDTH//2 - bar_width//2,
                30,
                bar_width * (
                    self.health /
                    self.max_health
                ),
                25
            )

        )



# =========================
# CHEFES DO ALIEN FALL 48
# =========================


class AlienQueen(Boss):


    def __init__(self,x,y):

        super().__init__(
            x,
            y,
            "Rainha Alien"
        )

        self.health = 5000
        self.max_health = 5000

        self.damage = 60



class AlienTitan(Boss):


    def __init__(self,x,y):

        super().__init__(
            x,
            y,
            "Titã Alien"
        )

        self.health = 10000
        self.max_health = 10000

        self.width = 200
        self.height = 200

        self.damage = 100
