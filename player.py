import pygame
from config import *

class Player:

    def __init__(self, x, y, character=None):
        self.x = float(x)
        self.y = float(y)

        # 192x192 = 300% da sprite original 64x64
        self.width  = 192
        self.height = 192

        if character:
            self.speed      = character.speed
            self.health     = character.health
            self.max_health = character.health
            self.damage     = character.damage
            self.skill      = character.skill
            self.name       = character.name
            self.character  = character
        else:
            self.speed      = PLAYER_SPEED
            self.health     = PLAYER_MAX_HEALTH
            self.max_health = PLAYER_MAX_HEALTH
            self.damage     = 20
            self.skill      = "Ataque básico"
            self.name       = "Jogador"
            self.character  = None

        self.energy      = PLAYER_MAX_ENERGY
        self.color       = (40, 120, 255)
        self.facing_left = False

        # Estado de animação interno
        self._anim       = "idle"
        self._frame      = 0.0
        self._anim_spd   = 8.0    # frames por segundo
        self._attack_timer = 0.0  # quanto tempo ainda está na animação de ataque

        self.image = self._render()
        self.rect  = pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    # ── renderização ──────────────────────────────────────────────────────
    def _render(self):
        if not self.character:
            surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.rect(surf, self.color, surf.get_rect(), border_radius=8)
            return surf

        anims = self.character.animations
        state = self._anim

        # Mapear estado para chave de animação
        key_map = {
            "idle":     "idle",
            "walk":     "walk",
            "run":      "run",
            "attack":   "attack",
            "damage":   "damage",
            "death":    "death",
        }
        key = key_map.get(state, "idle")
        if key not in anims:
            key = "idle"

        frames = anims[key]
        if not frames:
            frames = anims["idle"]

        idx = int(self._frame) % len(frames)
        # Scale para 192x192 (300% do sprite 64x64 original)
        img = pygame.transform.scale(frames[idx], (self.width, self.height))
        if self.facing_left:
            img = pygame.transform.flip(img, True, False)
        return img

    # ── disparo de animação de ataque (chamado pelo main.py ao atirar) ───
    def trigger_attack(self):
        if self._anim not in ("attack", "death"):
            self._anim  = "attack"
            self._frame = 0.0
            self._attack_timer = 0.45  # duração total da animação de ataque (s)

    def trigger_damage(self):
        if self._anim not in ("death",):
            self._anim  = "damage"
            self._frame = 0.0

    # ── update teclado ────────────────────────────────────────────────────
    def update(self, keys, dt):
        speed = self.speed
        if keys[pygame.K_LSHIFT]:
            speed = PLAYER_RUN_SPEED

        dx = dy = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:    dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  dy += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  dx -= 1; self.facing_left = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx += 1; self.facing_left = False

        if dx != 0 and dy != 0:
            dx *= 0.7071; dy *= 0.7071

        self._move(dx * speed * dt, dy * speed * dt)
        self._update_anim(dx, dy, bool(keys[pygame.K_LSHIFT]), dt)

    # ── update touch ──────────────────────────────────────────────────────
    def update_touch(self, jx, jy, dt):
        speed  = self.speed
        thresh = 0.15
        if abs(jx) < thresh and abs(jy) < thresh:
            jx = jy = 0
        else:
            if jx < -thresh: self.facing_left = True
            if jx >  thresh: self.facing_left = False
        self._move(jx * speed * dt, jy * speed * dt)
        self._update_anim(jx, jy, False, dt)

    # ── helpers internos ──────────────────────────────────────────────────
    def _move(self, dx, dy):
        self.x += dx
        self.y += dy
        MAP = 5000
        self.x = max(0, min(self.x, MAP - self.width))
        self.y = max(0, min(self.y, MAP - self.height))
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def _update_anim(self, dx, dy, running, dt):
        moving = abs(dx) > 0.01 or abs(dy) > 0.01

        # Decrementar timer de ataque
        if self._attack_timer > 0:
            self._attack_timer -= dt
            if self._attack_timer <= 0:
                self._anim = "walk" if moving else "idle"
        elif self._anim not in ("death", "damage"):
            if moving:
                self._anim = "run" if running else "walk"
            else:
                self._anim = "idle"

        # Voltar de damage para idle/walk
        if self._anim == "damage":
            self._attack_timer = max(self._attack_timer, 0.2)

        # Avançar frame
        self._frame += self._anim_spd * dt
        self.image = self._render()

    # ── draw ──────────────────────────────────────────────────────────────
    def draw(self, screen, camera):
        pos = camera.apply(self)
        # Sombra
        shadow = pygame.Surface((self.width, 10), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 50), shadow.get_rect())
        screen.blit(shadow, (pos.x, pos.y + self.height - 4))
        screen.blit(self.image, pos)
