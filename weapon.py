import pygame
from bullet import Bullet

class Weapon:

    def __init__(self):

        self.fire_rate = 0.15      # segundos entre disparos
        self.damage = 10
        self.magazine = 30
        self.max_magazine = 30

        self.reload_time = 2.0
        self.reload_timer = 0

        self.cooldown = 0

    def update(self, dt):

        if self.cooldown > 0:
            self.cooldown -= dt

        if self.reload_timer > 0:

            self.reload_timer -= dt

            if self.reload_timer <= 0:
                self.magazine = self.max_magazine

    def reload(self):

        if self.magazine < self.max_magazine:
            self.reload_timer = self.reload_time

    def shoot(self, x, y, target_x, target_y):

        if self.reload_timer > 0:
            return None

        if self.cooldown > 0:
            return None

        if self.magazine <= 0:
            return None

        self.magazine -= 1

        self.cooldown = self.fire_rate

        return Bullet(
            x,
            y,
            target_x,
            target_y
        )
