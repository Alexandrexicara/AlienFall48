import pygame

from config import *


class HUD:

    def __init__(self):

        self.font = pygame.font.SysFont(
            "Arial",
            22
        )

    def draw_bar(self, screen, x, y, value, maximum, color):

        width = 220
        height = 20

        # fundo
        pygame.draw.rect(
            screen,
            DARKGRAY,
            (
                x,
                y,
                width,
                height
            )
        )

        # valor atual
        pygame.draw.rect(
            screen,
            color,
            (
                x,
                y,
                width * (value / maximum),
                height
            )
        )


    def draw(self, screen, player, weapon=None):

        # Nome do personagem
        name_text = self.font.render(
            f"{player.name}",
            True,
            (255, 200, 0)
        )
        screen.blit(name_text, (20, HEIGHT - 90))

        # Habilidade do personagem
        skill_text = self.font.render(
            f"Habilidade: {player.skill}",
            True,
            (0, 200, 255)
        )
        screen.blit(skill_text, (20, HEIGHT - 115))

        # Vida

        self.draw_bar(
            screen,
            20,
            HEIGHT - 60,
            player.health,
            player.max_health,
            RED
        )


        # Energia

        self.draw_bar(
            screen,
            20,
            HEIGHT - 35,
            player.energy,
            PLAYER_MAX_ENERGY,
            BLUE
        )


        # Texto

        life_text = self.font.render(
            f"HP: {player.health}/{player.max_health}",
            True,
            WHITE
        )


        energy_text = self.font.render(
            f"ENERGIA: {player.energy}/{PLAYER_MAX_ENERGY}",
            True,
            WHITE
        )


        screen.blit(
            life_text,
            (250, HEIGHT - 60)
        )


        screen.blit(
            energy_text,
            (250, HEIGHT - 35)
        )

        # Munição da arma
        if weapon is not None:
            if weapon.reload_timer > 0:
                ammo_label = "RECARREGANDO..."
                ammo_color = ORANGE
            else:
                ammo_label = f"MUNICAO: {weapon.magazine}/{weapon.max_magazine}"
                ammo_color = WHITE

            ammo_text = self.font.render(ammo_label, True, ammo_color)
            screen.blit(ammo_text, (WIDTH - ammo_text.get_width() - 20, HEIGHT - 40))
