import pygame
import math

from config import *

class Bullet:

    def __init__(self, x, y, target_x, target_y):

        self.x = float(x)
        self.y = float(y)

        self.radius = 4

        self.speed = BULLET_SPEED

        self.damage = BULLET_DAMAGE

        dx = target_x - x
        dy = target_y - y

        dist = math.hypot(dx, dy)

        if dist == 0:
            dist = 1

        self.vx = (dx / dist) * self.speed
        self.vy = (dy / dist) * self.speed

        self.rect = pygame.Rect(
            int(self.x),
            int(self.y),
            self.radius * 2,
            self.radius * 2
        )

        self.alive = True

    def update(self, dt):

        self.x += self.vx * dt
        self.y += self.vy * dt

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if (
            self.x < 0 or
            self.y < 0 or
            self.x > 5000 or
            self.y > 5000
        ):
            self.alive = False

    def check_collision(self, enemies):

        for enemy in enemies:

            if self.rect.colliderect(enemy.rect):

                enemy.hit(self.damage)

                self.alive = False

                break

    def draw(self, screen, camera):

        pos = camera.apply_rect(self.rect)

        pygame.draw.circle(
            screen,
            YELLOW,
            pos.center,
            self.radius
        )
