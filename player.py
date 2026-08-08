import pygame
import os
from config import *

class Player:

    def __init__(self, x, y, character=None):

        self.x = float(x)
        self.y = float(y)

        # Tamanho do sprite exibido
        self.width  = 64
        self.height = 64

        if character:
            self.speed     = character.speed
            self.health    = character.health
            self.max_health= character.health
            self.damage    = character.damage
            self.skill     = character.skill
            self.name      = character.name
            self.character = character
        else:
            self.speed      = PLAYER_SPEED
            self.health     = PLAYER_MAX_HEALTH
            self.max_health = PLAYER_MAX_HEALTH
            self.damage     = 20
            self.skill      = "Ataque básico"
            self.name       = "Jogador"
            self.character  = None

        self.energy = PLAYER_MAX_ENERGY
        self.color  = (40, 120, 255)

        # Animação
        self.anim_state  = "idle"
        self.anim_frame  = 0.0
        self.anim_speed  = 8.0   # frames/s
        self.facing_left = False

        # Propriedade image para compatibilidade
        self.image = self._get_frame()

        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    # ── helpers de sprite ──────────────────────────────────────────────
    def _sprites(self):
        if self.character:
            return self.character.animations
        return {}

    def _get_frame(self):
        anims = self._sprites()
        if not anims:
            surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.rect(surf, self.color, surf.get_rect(), border_radius=8)
            return surf

        state = self.anim_state
        if state not in anims:
            state = "idle"
        frames = anims[state]
        if not frames:
            state = "idle"
            frames = anims.get("idle", [])
        if not frames:
            surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.rect(surf, self.color, surf.get_rect(), border_radius=8)
            return surf

        idx = int(self.anim_frame) % len(frames)
        img = pygame.transform.scale(frames[idx], (self.width, self.height))
        if self.facing_left:
            img = pygame.transform.flip(img, True, False)
        return img

    # ── update ─────────────────────────────────────────────────────────
    def update(self, keys, dt):

        speed = self.speed if hasattr(self, 'speed') else PLAYER_SPEED
        if keys[pygame.K_LSHIFT]:
            speed = PLAYER_RUN_SPEED

        dx = dy = 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:    dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  dy += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  dx -= 1; self.facing_left = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx += 1; self.facing_left = False

        # Normalizar diagonal
        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        moving = dx != 0 or dy != 0
        if moving:
            self.anim_state = "walk_01"
        else:
            self.anim_state = "idle"

        self.x += dx * speed * dt
        self.y += dy * speed * dt

        # Limites do mundo
        MAP_W = MAP_H = 5000
        self.x = max(0, min(self.x, MAP_W - self.width))
        self.y = max(0, min(self.y, MAP_H - self.height))

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # Avançar frame de animação
        self.anim_frame += self.anim_speed * dt
        self.image = self._get_frame()

    def update_touch(self, jx, jy, dt):
        """Mover usando joystick virtual (valores -1..1)."""
        speed = self.speed if hasattr(self, 'speed') else PLAYER_SPEED
        threshold = 0.15

        if abs(jx) > threshold or abs(jy) > threshold:
            if jx < -threshold: self.facing_left = True
            if jx >  threshold: self.facing_left = False
            self.anim_state = "walk_01"
        else:
            jx = jy = 0
            self.anim_state = "idle"

        self.x += jx * speed * dt
        self.y += jy * speed * dt

        MAP_W = MAP_H = 5000
        self.x = max(0, min(self.x, MAP_W - self.width))
        self.y = max(0, min(self.y, MAP_H - self.height))

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        self.anim_frame += self.anim_speed * dt
        self.image = self._get_frame()

    # ── draw ───────────────────────────────────────────────────────────
    def draw(self, screen, camera):
        pos = camera.apply(self)
        screen.blit(self.image, pos)

        # Sombra leve no chão
        shadow = pygame.Surface((self.width, 10), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 60), shadow.get_rect())
        screen.blit(shadow, (pos.x, pos.y + self.height - 4))
