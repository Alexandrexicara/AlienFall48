import pygame
import sys
import asyncio
import math
import random

from config import *
from player import Player
from camera import Camera
from map import GameMap
from alien import Alien
from weapon import Weapon
from hud import HUD
from menu import Menu
from character_select import CharacterSelect

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# ── Estados ────────────────────────────────────────────────────────────────
MENU_STATE     = 0
CHAR_SELECT    = 1
GAME_STATE     = 2

state = MENU_STATE

# ── Objetos de UI ──────────────────────────────────────────────────────────
menu             = Menu(screen)
character_select = CharacterSelect(screen)
hud              = HUD()
weapon           = Weapon("rifle")

player           = None
camera           = None
world            = None
aliens           = []
bullets          = []
wave             = 1
wave_timer       = 0.0
WAVE_INTERVAL    = 15.0   # segundos entre ondas

# ── Controles mobile ───────────────────────────────────────────────────────
JOYSTICK_CENTER  = (120, HEIGHT - 120)
JOYSTICK_RADIUS  = 80
FIRE_BTN         = (WIDTH - 100, HEIGHT - 120)
FIRE_BTN_R       = 60
RELOAD_BTN       = (WIDTH - 220, HEIGHT - 80)
RELOAD_BTN_R     = 40

touch_joy_id     = None   # id do toque no joystick
touch_joy_pos    = JOYSTICK_CENTER
touch_fire_id    = None
touch_fire_pos   = None
show_mobile_ui   = False   # ligado se houver toque


def start_game(character):
    global player, camera, world, aliens, bullets, wave, wave_timer, weapon

    bg_map = {
        "Soldado":         "city.png",
        "Sniper":          "forest.png",
        "Guerreiro":       "base.png",
        "Samurai Futurista":"alien_planet.png",
    }.get(character.name, "alien_planet.png")

    player     = Player(2500, 2500, character)
    camera     = Camera(world.width if world else 5000, world.height if world else 5000)
    world      = GameMap(bg_map)
    camera     = Camera(world.width, world.height)
    weapon     = Weapon("rifle")
    aliens     = _spawn_wave(wave, player)
    bullets    = []
    wave_timer = WAVE_INTERVAL


def _spawn_wave(wave_num, player):
    count = 3 + wave_num * 2
    enemy_pool = ["drone", "spider", "parasite"]
    if wave_num >= 2: enemy_pool.append("brute")
    if wave_num >= 4: enemy_pool.append("queen")
    if wave_num >= 6: enemy_pool.append("boss")

    spawned = []
    for _ in range(count):
        # Spawn em torno do jogador (longe o suficiente)
        angle  = random.uniform(0, math.pi * 2)
        dist   = random.uniform(600, 1000)
        sx     = player.rect.centerx + math.cos(angle) * dist
        sy     = player.rect.centery + math.sin(angle) * dist
        sx     = max(100, min(4900, sx))
        sy     = max(100, min(4900, sy))
        etype  = random.choice(enemy_pool)
        spawned.append(Alien(sx, sy, etype))
    return spawned


def _joystick_vector():
    """Retorna (jx, jy) normalizado [-1..1] do joystick virtual."""
    dx = touch_joy_pos[0] - JOYSTICK_CENTER[0]
    dy = touch_joy_pos[1] - JOYSTICK_CENTER[1]
    dist = math.hypot(dx, dy)
    if dist < 10:
        return 0.0, 0.0
    dist = min(dist, JOYSTICK_RADIUS)
    return dx / JOYSTICK_RADIUS, dy / JOYSTICK_RADIUS


def _draw_mobile_ui(surface):
    """Desenha joystick e botões de tiro na tela."""
    # Joystick base
    s = pygame.Surface((JOYSTICK_RADIUS * 2 + 20, JOYSTICK_RADIUS * 2 + 20), pygame.SRCALPHA)
    pygame.draw.circle(s, (255,255,255,40),
                       (JOYSTICK_RADIUS + 10, JOYSTICK_RADIUS + 10), JOYSTICK_RADIUS)
    pygame.draw.circle(s, (255,255,255,80),
                       (JOYSTICK_RADIUS + 10, JOYSTICK_RADIUS + 10), JOYSTICK_RADIUS, 2)
    surface.blit(s, (JOYSTICK_CENTER[0] - JOYSTICK_RADIUS - 10,
                     JOYSTICK_CENTER[1] - JOYSTICK_RADIUS - 10))

    # Joystick knob
    kx = touch_joy_pos[0]
    ky = touch_joy_pos[1]
    pygame.draw.circle(surface, (255,255,255,120), (kx, ky), 30)
    pygame.draw.circle(surface, (255,255,255,200), (kx, ky), 30, 3)

    # Botão de tiro
    fire_s = pygame.Surface((FIRE_BTN_R * 2, FIRE_BTN_R * 2), pygame.SRCALPHA)
    color  = (255, 80, 80, 180) if touch_fire_id else (255, 80, 80, 100)
    pygame.draw.circle(fire_s, color, (FIRE_BTN_R, FIRE_BTN_R), FIRE_BTN_R)
    pygame.draw.circle(fire_s, (255,120,120,200), (FIRE_BTN_R, FIRE_BTN_R), FIRE_BTN_R, 3)
    surface.blit(fire_s, (FIRE_BTN[0] - FIRE_BTN_R, FIRE_BTN[1] - FIRE_BTN_R))
    font_s = pygame.font.SysFont("Arial", 18, True)
    lbl = font_s.render("FIRE", True, (255, 255, 255))
    surface.blit(lbl, (FIRE_BTN[0] - lbl.get_width()//2, FIRE_BTN[1] - lbl.get_height()//2))

    # Botão reload
    rel_s = pygame.Surface((RELOAD_BTN_R * 2, RELOAD_BTN_R * 2), pygame.SRCALPHA)
    pygame.draw.circle(rel_s, (100,200,255,100), (RELOAD_BTN_R, RELOAD_BTN_R), RELOAD_BTN_R)
    pygame.draw.circle(rel_s, (150,220,255,180), (RELOAD_BTN_R, RELOAD_BTN_R), RELOAD_BTN_R, 2)
    surface.blit(rel_s, (RELOAD_BTN[0] - RELOAD_BTN_R, RELOAD_BTN[1] - RELOAD_BTN_R))
    lbl2 = font_s.render("R", True, (255, 255, 255))
    surface.blit(lbl2, (RELOAD_BTN[0] - lbl2.get_width()//2, RELOAD_BTN[1] - lbl2.get_height()//2))


async def main():
    global state, player, camera, world, aliens, bullets, weapon
    global wave, wave_timer
    global touch_joy_id, touch_joy_pos, touch_fire_id, touch_fire_pos, show_mobile_ui

    running = True

    while running:
        dt = min(clock.tick(FPS) / 1000.0, 0.05)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # ── MENU ───────────────────────────────────────────────────
            if state == MENU_STATE:
                result = menu.update(event)
                if result == "NOVO JOGO":
                    state = CHAR_SELECT
                elif result == "SAIR":
                    running = False

            # ── SELEÇÃO DE PERSONAGEM ──────────────────────────────────
            elif state == CHAR_SELECT:
                result = character_select.update(event)
                if result:
                    start_game(result)
                    state = GAME_STATE

            # ── JOGO ───────────────────────────────────────────────────
            elif state == GAME_STATE:

                # Teclado — tiro e reload
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        weapon.reload()

                # Mouse — tiro
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = pygame.mouse.get_pos()
                    wx = mx - camera.camera.x
                    wy = my - camera.camera.y
                    new_bullets = weapon.shoot(player.rect.centerx,
                                               player.rect.centery, wx, wy)
                    if new_bullets:
                        bullets.extend(new_bullets)
                        player.trigger_attack()

                # Touch
                if event.type == pygame.FINGERDOWN:
                    show_mobile_ui = True
                    tx = int(event.x * WIDTH)
                    ty = int(event.y * HEIGHT)
                    # Joystick?
                    if math.hypot(tx - JOYSTICK_CENTER[0], ty - JOYSTICK_CENTER[1]) <= JOYSTICK_RADIUS + 40:
                        touch_joy_id  = event.finger_id
                        touch_joy_pos = (tx, ty)
                    # Fire?
                    elif math.hypot(tx - FIRE_BTN[0], ty - FIRE_BTN[1]) <= FIRE_BTN_R + 20:
                        touch_fire_id  = event.finger_id
                        touch_fire_pos = (tx, ty)
                    # Reload?
                    elif math.hypot(tx - RELOAD_BTN[0], ty - RELOAD_BTN[1]) <= RELOAD_BTN_R + 20:
                        weapon.reload()

                if event.type == pygame.FINGERMOTION:
                    tx = int(event.x * WIDTH)
                    ty = int(event.y * HEIGHT)
                    if event.finger_id == touch_joy_id:
                        # Limitar ao raio do joystick
                        ddx = tx - JOYSTICK_CENTER[0]
                        ddy = ty - JOYSTICK_CENTER[1]
                        d   = math.hypot(ddx, ddy)
                        if d > JOYSTICK_RADIUS:
                            ddx = ddx / d * JOYSTICK_RADIUS
                            ddy = ddy / d * JOYSTICK_RADIUS
                        touch_joy_pos = (int(JOYSTICK_CENTER[0] + ddx),
                                         int(JOYSTICK_CENTER[1] + ddy))

                if event.type == pygame.FINGERUP:
                    if event.finger_id == touch_joy_id:
                        touch_joy_id  = None
                        touch_joy_pos = JOYSTICK_CENTER
                    if event.finger_id == touch_fire_id:
                        touch_fire_id  = None
                        touch_fire_pos = None

        # ── LÓGICA DO JOGO ─────────────────────────────────────────────
        if state == GAME_STATE and player:

            # Mover via teclado ou joystick touch
            keys = pygame.key.get_pressed()
            if touch_joy_id is not None:
                jx, jy = _joystick_vector()
                player.update_touch(jx, jy, dt)
            else:
                player.update(keys, dt)

            # Atirar contínuo no touch (fire button pressionado)
            if touch_fire_id is not None:
                # Mirar para o inimigo mais próximo ou para frente
                if aliens:
                    nearest = min(aliens, key=lambda a: math.hypot(
                        a.rect.centerx - player.rect.centerx,
                        a.rect.centery - player.rect.centery))
                    wx, wy = nearest.rect.centerx, nearest.rect.centery
                else:
                    wx = player.rect.centerx + (1 if not player.facing_left else -1) * 200
                    wy = player.rect.centery
                new_bullets = weapon.shoot(player.rect.centerx,
                                           player.rect.centery, wx, wy)
                if new_bullets:
                    bullets.extend(new_bullets)
                    player.trigger_attack()

            weapon.update(dt)

            for alien in aliens:
                alien.update(player, dt)
                # Dano de contato com alien
                if alien.rect.colliderect(player.rect) and not alien.is_dying:
                    player.health -= alien.damage * dt * 0.5
                    player.trigger_damage()
                    if player.health < 0:
                        player.health = 0

            for bullet in bullets:
                bullet.update(dt)
                bullet.check_collision(aliens)

            bullets = [b for b in bullets if b.alive]
            aliens  = [a for a in aliens if not a.dead()]

            camera.update(player)

            # Ângulo da arma para o mouse (desktop)
            if touch_joy_id is None:
                mx, my = pygame.mouse.get_pos()
                px_screen = player.rect.centerx + camera.camera.x
                py_screen = player.rect.centery + camera.camera.y
                weapon.angle = math.degrees(math.atan2(-(my - py_screen), mx - px_screen))

            # Nova onda
            wave_timer -= dt
            if not aliens and wave_timer <= 0:
                wave += 1
                wave_timer = WAVE_INTERVAL
                aliens = _spawn_wave(wave, player)

        # ── DESENHAR ───────────────────────────────────────────────────
        if state == MENU_STATE:
            menu.draw()

        elif state == CHAR_SELECT:
            character_select.draw()

        elif state == GAME_STATE and player:
            screen.fill(BLACK)
            world.draw(screen, camera)

            for alien in aliens:
                alien.draw(screen, camera)

            for bullet in bullets:
                bullet.draw(screen, camera)

            # Desenhar arma ANTES do jogador (na mão)
            p_rect = camera.apply(player)
            weapon.draw_on_player(screen, p_rect, player.facing_left)

            player.draw(screen, camera)

            hud.draw(screen, player, weapon)

            # Info de onda
            font_w = pygame.font.SysFont("Arial", 22, True)
            wt = font_w.render(f"ONDA {wave}  |  Inimigos: {len(aliens)}", True, (255, 200, 0))
            screen.blit(wt, (WIDTH // 2 - wt.get_width() // 2, 12))

            # UI mobile
            if show_mobile_ui:
                _draw_mobile_ui(screen)

        pygame.display.flip()
        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())
