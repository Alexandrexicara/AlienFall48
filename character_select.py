import pygame

from config import *
from characters import (
    Warrior,
    Soldier,
    Sniper,
    Medic,
    Engineer,
    Samurai
)


class CharacterSelect:


    def __init__(self, screen):

        self.screen = screen

        self.font = pygame.font.SysFont(
            "Arial",
            35
        )


        self.characters = None  # Será inicializado depois
        self.selected = 0

    def init_characters(self):
        if self.characters is None:
            self.characters = [
                Warrior(),
                Soldier(),
                Sniper(),
                Medic(),
                Engineer(),
                Samurai()
            ]



    def update(self, event):

        self.init_characters()  # Garante que os personagens estão carregados

        if event.type == pygame.KEYDOWN:


            if event.key == pygame.K_RIGHT:

                self.selected += 1


                if self.selected >= len(self.characters):

                    self.selected = 0



            if event.key == pygame.K_LEFT:


                self.selected -= 1


                if self.selected < 0:

                    self.selected = len(self.characters)-1



            if event.key == pygame.K_RETURN:

                return self.characters[
                    self.selected
                ]

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clique esquerdo
                mouse_pos = pygame.mouse.get_pos()
                # Verificar clique nos nomes dos personagens
                for i, char in enumerate(self.characters):
                    text = self.font.render(char.name, True, WHITE)
                    text_rect = pygame.Rect(
                        400,
                        180 + i*50,
                        text.get_width(),
                        40
                    )
                    if text_rect.collidepoint(mouse_pos):
                        self.selected = i
                        return self.characters[i]


        return None



    def draw(self):

        self.init_characters()  # Garante que os personagens estão carregados

        self.screen.fill(
            (15,15,25)
        )


        title = self.font.render(

            "ESCOLHA SEU GUERREIRO",

            True,

            (255,200,0)

        )


        self.screen.blit(

            title,

            (350,80)

        )
        
        # Instruções
        instructions = self.font.render(
            "Use ← → para selecionar | ENTER para confirmar",
            True,
            (200, 200, 200)
        )
        
        self.screen.blit(
            instructions,
            (320, 130)
        )



        for i, char in enumerate(self.characters):


            color = (255,255,255)


            if i == self.selected:

                color = (255,255,0)

                # Desenhar sprite do personagem selecionado
                sprite_scaled = pygame.transform.scale(char.image, (128, 128))
                self.screen.blit(sprite_scaled, (550, 250))



            text = self.font.render(

                char.name,

                True,

                color

            )


            self.screen.blit(

                text,

                (400,180 + i*50)

            )



        selected = self.characters[
            self.selected
        ]



        info = self.font.render(

            f"Dano: {selected.damage}  Vida: {selected.health}",

            True,

            (0,255,0)

        )


        self.screen.blit(

            info,

            (300,550)

        )
        
        skill_text = self.font.render(
            f"Habilidade: {selected.skill}",
            True,
            (0,200,255)
        )
        
        self.screen.blit(
            skill_text,
            (300,600)
        )
