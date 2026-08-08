import pygame
import os
from config import *

class GameMap:

    def __init__(self, background_name="city.png"):

        self.width = 5000
        self.height = 5000

        self.tile_size = TILESIZE

        # Carregar background
        self.background = self.load_background(background_name)

        self.surface = pygame.Surface((self.width, self.height))

        self.create_map()

    def load_background(self, background_name):
        """Carrega o background da pasta assets/backgrounds/"""
        try:
            background_path = os.path.join("assets", "backgrounds", background_name)
            if os.path.exists(background_path):
                background = pygame.image.load(background_path).convert()
                return background
            else:
                return None
        except Exception as e:
            return None

    def create_map(self):

        if self.background:
            # Usar o background carregado apenas uma vez, centralizado
            bg_width, bg_height = self.background.get_size()
            
            # Centralizar o background no mapa
            x = (self.width - bg_width) // 2
            y = (self.height - bg_height) // 2
            
            self.surface.blit(self.background, (x, y))
            
            # Preencher o resto com cor sólida
            self.surface.fill((30, 30, 40), (0, 0, x, self.height))  # Esquerda
            self.surface.fill((30, 30, 40), (x + bg_width, 0, self.width - (x + bg_width), self.height))  # Direita
            self.surface.fill((30, 30, 40), (x, 0, bg_width, y))  # Topo
            self.surface.fill((30, 30, 40), (x, y + bg_height, bg_width, self.height - (y + bg_height)))  # Fundo
        else:
            # Fallback: criar mapa de cidade destruída
            ground1 = (60, 60, 70)
            ground2 = (70, 70, 80)
            building = (40, 40, 50)
            road = (30, 30, 35)

            for y in range(0, self.height, self.tile_size):

                for x in range(0, self.width, self.tile_size):

                    # Criar ruas
                    if (x // self.tile_size) % 8 == 0 or (y // self.tile_size) % 8 == 0:
                        color = road
                    else:
                        # Alternar cores do chão
                        if (x//self.tile_size + y//self.tile_size) % 2 == 0:
                            color = ground1
                        else:
                            color = ground2

                    pygame.draw.rect(
                        self.surface,
                        color,
                        (
                            x,
                            y,
                            self.tile_size,
                            self.tile_size
                        )
                    )

            # Adicionar alguns blocos de prédios
            for i in range(0, 50):
                bx = (i * 100) % (self.width - 200) + 100
                by = (i * 150) % (self.height - 200) + 100
                pygame.draw.rect(
                    self.surface,
                    building,
                    (bx, by, 80, 120)
                )

    def draw(self, screen, camera):
        # Desenhar apenas a parte visível do mapa
        screen.blit(
            self.surface,
            camera.camera.topleft
        )
