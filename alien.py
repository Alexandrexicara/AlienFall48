import pygame
import math
import os

from config import *

class Alien:

    def __init__(self, x, y):

        self.x = float(x)
        self.y = float(y)

        self.speed = ALIEN_SPEED

        self.health = ALIEN_HEALTH

        self.width = 32
        self.height = 32

        # Carregar sprite diretamente
        self.image = pygame.image.load(
            os.path.join(
                "assets",
                "enemies",
                "alien01",
                "idle.png"
            )
        ).convert_alpha()
        
        # Escalar para o tamanho correto
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.animation_timer = 0
        self.animation_speed = 0.15

        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    def update(self, player, dt):

        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery

        dist = math.hypot(dx, dy)

        if dist > 0:

            dx /= dist
            dy /= dist

            self.x += dx * self.speed * dt
            self.y += dy * self.speed * dt

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def hit(self, damage):

        self.health -= damage

    def dead(self):

        return self.health <= 0

    def draw(self, screen, camera):

        screen.blit(
            self.image,
            camera.apply(self)
        )

        pygame.draw.rect(
            screen,
            RED,
            (
                camera.apply(self).x,
                camera.apply(self).y - 8,
                32,
                4
            )
        )

        pygame.draw.rect(
            screen,
            GREEN,
            (
                camera.apply(self).x,
                camera.apply(self).y - 8,
                max(0, 32 * (self.health / ALIEN_HEALTH)),
                4
            )
        )
