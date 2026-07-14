import pygame

from config import *


class Menu:

    def __init__(self, screen):

        self.screen = screen

        self.font_big = pygame.font.SysFont(
            "Arial",
            60,
            True
        )

        self.font = pygame.font.SysFont(
            "Arial",
            35
        )


        self.options = [
            "NOVO JOGO",
            "CONTINUAR",
            "CONFIGURACOES",
            "SAIR"
        ]

        self.selected = 0


    def draw(self):

        self.screen.fill(
            BLACK
        )


        title = self.font_big.render(
            "ALIEN FALL 48",
            True,
            ORANGE
        )


        self.screen.blit(
            title,
            (
                WIDTH//2 - title.get_width()//2,
                100
            )
        )


        for i, option in enumerate(self.options):

            color = WHITE

            if i == self.selected:
                color = YELLOW


            text = self.font.render(
                option,
                True,
                color
            )


            self.screen.blit(
                text,
                (
                    WIDTH//2 - text.get_width()//2,
                    250 + i * 60
                )
            )


    def update(self, event):

        if event.type == pygame.KEYDOWN:


            if event.key == pygame.K_DOWN:

                self.selected += 1


                if self.selected >= len(self.options):
                    self.selected = 0



            if event.key == pygame.K_UP:

                self.selected -= 1


                if self.selected < 0:
                    self.selected = len(self.options)-1



            if event.key == pygame.K_RETURN:

                return self.options[self.selected]

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clique esquerdo
                mouse_pos = pygame.mouse.get_pos()
                for i, option in enumerate(self.options):
                    text = self.font.render(option, True, WHITE)
                    text_rect = pygame.Rect(
                        WIDTH//2 - text.get_width()//2,
                        250 + i * 60,
                        text.get_width(),
                        40
                    )
                    if text_rect.collidepoint(mouse_pos):
                        self.selected = i
                        return self.options[i]


        return None
