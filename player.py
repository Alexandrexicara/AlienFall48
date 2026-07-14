import pygame
from config import *

class Player:

    def __init__(self, x, y, character=None):

        self.x = x
        self.y = y

        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT

        if character:
            self.speed = character.speed
            self.health = character.health
            self.max_health = character.health
            self.damage = character.damage
            self.skill = character.skill
            self.name = character.name
            self.image = character.image
        else:
            self.speed = PLAYER_SPEED
            self.health = PLAYER_MAX_HEALTH
            self.max_health = PLAYER_MAX_HEALTH
            self.damage = 20
            self.skill = "Ataque básico"
            self.name = "Jogador"
            self.image = None

        self.energy = PLAYER_MAX_ENERGY

        self.color = (40,120,255)

        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    def update(self, keys, dt):

        speed = PLAYER_SPEED

        if keys[pygame.K_LSHIFT]:
            speed = PLAYER_RUN_SPEED

        dx = 0
        dy = 0

        if keys[pygame.K_w]:
            dy -= speed * dt

        if keys[pygame.K_s]:
            dy += speed * dt

        if keys[pygame.K_a]:
            dx -= speed * dt

        if keys[pygame.K_d]:
            dx += speed * dt

        # Movimento diagonal normalizado
        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        self.x += dx
        self.y += dy

        # Limites da tela
        if self.x < 0:
            self.x = 0

        if self.y < 0:
            self.y = 0

        if self.x > WIDTH - self.width:
            self.x = WIDTH - self.width

        if self.y > HEIGHT - self.height:
            self.y = HEIGHT - self.height

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(self, screen, camera):

        if self.image:
            # Desenhar sprite do personagem
            sprite_scaled = pygame.transform.scale(self.image, (self.width, self.height))
            screen.blit(sprite_scaled, camera.apply(self))
        else:
            # Fallback para retângulo colorido
            pygame.draw.rect(
                screen,
                self.color,
                camera.apply(self),
                border_radius=6
            )
