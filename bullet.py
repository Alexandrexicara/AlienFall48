import pygame
import math

from config import *

class Bullet:

    def __init__(self, x, y, target_x, target_y,
                 speed=None, damage=None, color=None, spread=0.0):

        self.x = float(x)
        self.y = float(y)

        self.radius = 5
        self.speed  = speed  if speed  is not None else BULLET_SPEED
        self.damage = damage if damage is not None else BULLET_DAMAGE
        self.color  = color  if color  is not None else YELLOW
        self.alive  = True

        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy) or 1

        # Aplicar spread (escopeta)
        base_angle = math.atan2(dy, dx) + spread
        self.vx = math.cos(base_angle) * self.speed
        self.vy = math.sin(base_angle) * self.speed

        self.rect = pygame.Rect(int(self.x) - self.radius,
                                int(self.y) - self.radius,
                                self.radius * 2, self.radius * 2)

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.rect.center = (int(self.x), int(self.y))

        if self.x < 0 or self.y < 0 or self.x > 5000 or self.y > 5000:
            self.alive = False

    def check_collision(self, enemies):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.hit(self.damage)
                self.alive = False
                return

    def draw(self, screen, camera):
        pos = camera.apply_rect(self.rect)
        # Rastro
        pygame.draw.circle(screen, (self.color[0]//3, self.color[1]//3, self.color[2]//3),
                           pos.center, self.radius + 2)
        pygame.draw.circle(screen, self.color, pos.center, self.radius)
