import pygame
import os

class SpriteSheet:

    def __init__(self, filename):

        self.sheet = pygame.image.load(filename).convert_alpha()

    def get_sprite(self, x, y, width, height):

        sprite = pygame.Surface((width, height), pygame.SRCALPHA)

        sprite.blit(
            self.sheet,
            (0, 0),
            (x, y, width, height)
        )

        return sprite
