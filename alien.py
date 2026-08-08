import pygame
import math
import os
import random

from config import *

# Tipos de inimigos disponíveis com suas configs
ENEMY_TYPES = {
    "drone":    {"folder": "drone",    "health": 30,  "speed": 160, "damage": 8,  "size": 48},
    "brute":    {"folder": "brute",    "health": 120, "speed": 80,  "damage": 20, "size": 64},
    "spider":   {"folder": "spider",   "health": 50,  "speed": 140, "damage": 12, "size": 48},
    "parasite": {"folder": "parasite", "health": 25,  "speed": 180, "damage": 6,  "size": 40},
    "queen":    {"folder": "queen",    "health": 300, "speed": 60,  "damage": 35, "size": 80},
    "boss":     {"folder": "boss",     "health": 600, "speed": 50,  "damage": 50, "size": 96},
}

def load_enemy_sprites(folder):
    """Carrega sprites de animação do inimigo."""
    base = os.path.join("assets", "enemies", folder)
    sprites = {}
    for anim in ["idle", "walk_01", "walk_02", "attack_01", "damage", "death"]:
        path = os.path.join(base, f"{anim}.png")
        if os.path.exists(path):
            sprites[anim] = pygame.image.load(path).convert_alpha()
    # fallback: idle como padrão
    if "idle" not in sprites:
        # gerar superfície colorida de fallback
        surf = pygame.Surface((64, 64), pygame.SRCALPHA)
        pygame.draw.circle(surf, (180, 0, 180), (32, 32), 28)
        sprites["idle"] = surf
    return sprites

class Alien:

    def __init__(self, x, y, enemy_type=None):
        self.x = float(x)
        self.y = float(y)

        # Escolher tipo aleatório se não especificado
        if enemy_type is None:
            # Excluir queen e boss do spawn aleatório normal
            normal_types = ["drone", "brute", "spider", "parasite"]
            enemy_type = random.choice(normal_types)

        cfg = ENEMY_TYPES.get(enemy_type, ENEMY_TYPES["drone"])
        self.enemy_type = enemy_type
        self.size = cfg["size"]
        self.width = self.size
        self.height = self.size
        self.speed = cfg["speed"]
        self.health = cfg["health"]
        self.max_health = cfg["health"]
        self.damage = cfg["damage"]

        # Carregar sprites
        self.sprites = load_enemy_sprites(cfg["folder"])

        # Estado de animação
        self.current_anim = "idle"
        self.anim_frame = 0.0
        self.anim_speed = 8.0  # frames por segundo
        self.is_dying = False
        self.death_done = False

        # Imagem atual
        self.image = self._get_frame()

        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def _get_frame(self):
        anim = self.current_anim
        if anim not in self.sprites:
            anim = "idle"
        img = self.sprites[anim]
        return pygame.transform.scale(img, (self.width, self.height))

    def update(self, player, dt):
        if self.is_dying:
            self.anim_frame += self.anim_speed * dt
            if self.anim_frame >= 1:
                self.death_done = True
            return

        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)

        if dist > 5:
            dx /= dist
            dy /= dist
            self.x += dx * self.speed * dt
            self.y += dy * self.speed * dt
            self.current_anim = "walk_01"
        else:
            self.current_anim = "idle"

        # Ciclo de animação walk
        self.anim_frame = (self.anim_frame + self.anim_speed * dt)
        walk_frames = [k for k in ["walk_01", "walk_02"] if k in self.sprites]
        if walk_frames and self.current_anim == "walk_01":
            idx = int(self.anim_frame) % len(walk_frames)
            self.current_anim = walk_frames[idx]

        self.image = self._get_frame()
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_dying = True
            self.current_anim = "death"
            self.anim_frame = 0.0
        else:
            self.current_anim = "damage"

    def dead(self):
        return self.death_done or (self.health <= 0 and not self.is_dying)

    def draw(self, screen, camera):
        pos = camera.apply(self)
        screen.blit(self.image, pos)

        # Barra de vida (só se não estiver morrendo)
        if not self.is_dying and self.health < self.max_health:
            bar_w = self.width
            pygame.draw.rect(screen, RED,   (pos.x, pos.y - 8, bar_w, 5))
            pygame.draw.rect(screen, GREEN, (pos.x, pos.y - 8, int(bar_w * self.health / self.max_health), 5))
