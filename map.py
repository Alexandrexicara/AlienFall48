import pygame
import os
from config import *

class GameMap:

    def __init__(self, background_name="city.png"):

        self.width  = 5000
        self.height = 5000
        self.tile_size = TILESIZE

        self.background = self._load_bg(background_name)
        self.surface = pygame.Surface((self.width, self.height))
        self._build()

    def _load_bg(self, name):
        # Tentar JPEG primeiro (menor), depois PNG
        base = name.replace(".png", "")
        for ext in [".jpg", ".png"]:
            path = os.path.join("assets", "backgrounds", base + ext)
            if os.path.exists(path):
                try:
                    return pygame.image.load(path).convert()
                except Exception:
                    pass
        return None

    def _build(self):
        if self.background:
            # Esticar a imagem de fundo para cobrir o mapa inteiro — sem tiles duplicados
            scaled_bg = pygame.transform.scale(self.background, (self.width, self.height))
            self.surface.blit(scaled_bg, (0, 0))
        else:
            # Fallback: chão com grade de ruas
            ground1  = (55, 60, 70)
            ground2  = (65, 70, 80)
            road     = (28, 28, 34)
            building = (38, 38, 48)

            for ty in range(0, self.height, self.tile_size):
                for tx in range(0, self.width, self.tile_size):
                    gx = tx // self.tile_size
                    gy = ty // self.tile_size
                    if gx % 8 == 0 or gy % 8 == 0:
                        color = road
                    elif (gx + gy) % 2 == 0:
                        color = ground1
                    else:
                        color = ground2
                    pygame.draw.rect(self.surface, color,
                                     (tx, ty, self.tile_size, self.tile_size))

            # Alguns prédios
            for i in range(60):
                bx = (i * 83)  % (self.width  - 200) + 100
                by = (i * 127) % (self.height - 200) + 100
                w  = 60 + (i % 5) * 20
                h  = 80 + (i % 4) * 30
                pygame.draw.rect(self.surface, building, (bx, by, w, h))
                # Janelas
                for wy in range(by + 10, by + h - 10, 20):
                    for wx in range(bx + 8, bx + w - 8, 16):
                        c = (80, 80, 50) if (wy + wx) % 3 == 0 else (40, 40, 30)
                        pygame.draw.rect(self.surface, c, (wx, wy, 8, 10))

    def draw(self, screen, camera):
        screen.blit(self.surface, camera.camera.topleft)
