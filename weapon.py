import pygame
import math
import os

from config import *
from bullet import Bullet

WEAPON_SPRITES = {
    "pistol":   {"color": (200, 200, 200), "fire_rate": 0.25, "damage": 15, "mag": 12, "reload": 1.5, "bullet_speed": 700,  "bullet_color": (255, 255, 100)},
    "rifle":    {"color": (100, 200, 100), "fire_rate": 0.12, "damage": 12, "mag": 30, "reload": 2.0, "bullet_speed": 900,  "bullet_color": (100, 255, 100)},
    "shotgun":  {"color": (200, 140,  80), "fire_rate": 0.80, "damage": 8,  "mag":  6, "reload": 2.5, "bullet_speed": 600,  "bullet_color": (255, 180,  80), "pellets": 5},
    "sniper":   {"color": ( 80, 160, 255), "fire_rate": 1.20, "damage": 90, "mag":  5, "reload": 3.0, "bullet_speed": 1400, "bullet_color": ( 80, 200, 255)},
}

class Weapon:

    def __init__(self, weapon_type="rifle"):
        cfg = WEAPON_SPRITES.get(weapon_type, WEAPON_SPRITES["rifle"])
        self.weapon_type   = weapon_type
        self.color         = cfg["color"]
        self.fire_rate     = cfg["fire_rate"]
        self.damage        = cfg["damage"]
        self.max_magazine  = cfg["mag"]
        self.magazine      = cfg["mag"]
        self.reload_time   = cfg["reload"]
        self.reload_timer  = 0
        self.cooldown      = 0
        self.bullet_speed  = cfg["bullet_speed"]
        self.bullet_color  = cfg["bullet_color"]
        self.pellets       = cfg.get("pellets", 1)

        # Ângulo atual da arma (graus, aponta para o mouse/toque)
        self.angle = 0

    def update(self, dt):
        if self.cooldown > 0:
            self.cooldown -= dt

        if self.reload_timer > 0:
            self.reload_timer -= dt
            if self.reload_timer <= 0:
                self.magazine = self.max_magazine

    def reload(self):
        if self.magazine < self.max_magazine and self.reload_timer <= 0:
            self.reload_timer = self.reload_time

    def shoot(self, px, py, tx, ty):
        """Retorna lista de balas ou [] se não puder atirar."""
        if self.reload_timer > 0 or self.cooldown > 0 or self.magazine <= 0:
            return []

        self.magazine -= 1
        self.cooldown  = self.fire_rate

        dx = tx - px
        dy = ty - py
        self.angle = math.degrees(math.atan2(-dy, dx))

        bullets = []
        for i in range(self.pellets):
            spread = 0
            if self.pellets > 1:
                spread = math.radians(-12 + i * (24 / (self.pellets - 1)))
            b = Bullet(px, py, tx, ty,
                       speed=self.bullet_speed,
                       damage=self.damage,
                       color=self.bullet_color,
                       spread=spread)
            bullets.append(b)

        return bullets

    def draw_on_player(self, screen, player_screen_rect, facing_left):
        """Desenha a arma na mão do jogador."""
        cx = player_screen_rect.centerx
        cy = player_screen_rect.centery + 8

        gun_len = 22
        gun_w   = 7
        angle_r = math.radians(self.angle)

        tip_x = cx + math.cos(angle_r) * gun_len
        tip_y = cy - math.sin(angle_r) * gun_len

        pygame.draw.line(screen, (30, 30, 30),   (cx, cy), (int(tip_x), int(tip_y)), gun_w + 2)
        pygame.draw.line(screen, self.color,      (cx, cy), (int(tip_x), int(tip_y)), gun_w)
        pygame.draw.circle(screen, (50, 50, 50),  (int(tip_x), int(tip_y)), 3)
