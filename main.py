import pygame
import sys

from config import *

from player import Player
from camera import Camera
from map import GameMap

from alien import Alien
from bullet import Bullet
from weapon import Weapon

from hud import HUD
from menu import Menu
from character_select import CharacterSelect


pygame.init()


screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    TITLE
)


clock = pygame.time.Clock()


# =========================
# ESTADOS DO JOGO
# =========================

MENU = 0
CHARACTER_SELECT = 1
GAME = 2

state = MENU



# =========================
# OBJETOS
# =========================

menu = Menu(screen)
character_select = CharacterSelect(screen)

player = None
selected_character = None

camera = None

world = None

hud = HUD()

weapon = Weapon()


aliens = []

bullets = []



def start_game(character):

    global player
    global camera
    global world
    global aliens
    global selected_character

    selected_character = character

    player = Player(
        2500,
        2500,
        character
    )


    # Escolher background seguindo a ordem: alien_planet → city → forest → base
    background_map = "alien_planet.png"
    if character.name == "Soldado":
        background_map = "city.png"
    elif character.name == "Sniper":
        background_map = "forest.png"
    elif character.name == "Guerreiro":
        background_map = "base.png"

    world = GameMap(background_map)


    camera = Camera(
        world.width,
        world.height
    )


    aliens = [

        Alien(
            2700,
            2500
        ),

        Alien(
            3000,
            2600
        ),

        Alien(
            3200,
            2800
        )

    ]



running = True


while running:


    dt = clock.tick(FPS) / 1000



    for event in pygame.event.get():


        if event.type == pygame.QUIT:

            running = False



        # MENU

        if state == MENU:


            result = menu.update(
                event
            )


            if result == "NOVO JOGO":

                state = CHARACTER_SELECT



            if result == "SAIR":

                running = False

        # CHARACTER SELECT

        elif state == CHARACTER_SELECT:

            result = character_select.update(event)

            if result:

                start_game(result)

                state = GAME



        # JOGO

        elif state == GAME:


            if event.type == pygame.MOUSEBUTTONDOWN:


                if event.button == 1:


                    mouse = pygame.mouse.get_pos()


                    bullet = weapon.shoot(

                        player.rect.centerx,

                        player.rect.centery,

                        mouse[0] - camera.camera.x,

                        mouse[1] - camera.camera.y

                    )


                    if bullet:

                        bullets.append(
                            bullet
                        )



            if event.type == pygame.KEYDOWN:


                if event.key == pygame.K_r:

                    weapon.reload()



    # =========================
    # DESENHO MENU
    # =========================

    if state == MENU:


        menu.draw()

    # =========================
    # CHARACTER SELECT
    # =========================

    elif state == CHARACTER_SELECT:

        character_select.draw()

    # =========================
    # JOGO
    # =========================

    elif state == GAME:


        keys = pygame.key.get_pressed()


        player.update(
            keys,
            dt
        )


        weapon.update(
            dt
        )



        for alien in aliens:

            alien.update(
                player,
                dt
            )



        for bullet in bullets:

            bullet.update(
                dt
            )

            bullet.check_collision(
                aliens
            )


        bullets = [

            b for b in bullets

            if b.alive

        ]



        aliens = [

            a for a in aliens

            if not a.dead()

        ]



        camera.update(
            player
        )



        screen.fill(
            BLACK
        )



        world.draw(
            screen,
            camera
        )


        for alien in aliens:

            alien.draw(
                screen,
                camera
            )


        for bullet in bullets:

            bullet.draw(
                screen,
                camera
            )


        player.draw(
            screen,
            camera
        )


        hud.draw(
            screen,
            player
        )



    pygame.display.flip()



pygame.quit()

sys.exit()
