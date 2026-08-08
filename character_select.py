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
        self.characters = None
        self.selected = 0
        # Touch/scroll support
        self._touch_start = None

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

    # ── Helpers ──────────────────────────────────────────────────────────────

    def _card_rects(self, W, H):
        """Retorna lista de pygame.Rect para cada card de personagem."""
        n = len(self.characters)
        # Layout: 3 colunas × 2 linhas se landscape, 2 colunas × 3 linhas se portrait
        cols = 3 if W >= H else 2
        rows = (n + cols - 1) // cols

        margin = int(min(W, H) * 0.03)
        header_h = int(H * 0.22)   # espaço para título + instruções
        footer_h = int(H * 0.18)   # espaço para info do personagem

        grid_w = W - margin * 2
        grid_h = H - header_h - footer_h - margin * 2

        card_w = (grid_w - margin * (cols - 1)) // cols
        card_h = (grid_h - margin * (rows - 1)) // rows

        rects = []
        for i in range(n):
            col = i % cols
            row = i // cols
            x = margin + col * (card_w + margin)
            y = header_h + margin + row * (card_h + margin)
            rects.append(pygame.Rect(x, y, card_w, card_h))
        return rects

    # ── Update ───────────────────────────────────────────────────────────────

    def update(self, event):
        self.init_characters()
        W, H = self.screen.get_size()
        rects = self._card_rects(W, H)

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RIGHT, pygame.K_DOWN):
                self.selected = (self.selected + 1) % len(self.characters)
            elif event.key in (pygame.K_LEFT, pygame.K_UP):
                self.selected = (self.selected - 1) % len(self.characters)
            elif event.key == pygame.K_RETURN:
                return self.characters[self.selected]

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            for i, rect in enumerate(rects):
                if rect.collidepoint(mx, my):
                    if self.selected == i:
                        # Segundo clique = confirmar
                        return self.characters[i]
                    self.selected = i

            # Botão CONFIRMAR (footer)
            btn = self._confirm_btn_rect(W, H)
            if btn.collidepoint(mx, my):
                return self.characters[self.selected]

        elif event.type == pygame.FINGERDOWN:
            W, H = self.screen.get_size()
            tx, ty = int(event.x * W), int(event.y * H)
            self._touch_start = (tx, ty, self.selected)

        elif event.type == pygame.FINGERUP:
            if self._touch_start:
                W, H = self.screen.get_size()
                tx, ty = int(event.x * W), int(event.y * H)
                sx, sy, _ = self._touch_start
                # Tap (não deslize)
                if abs(tx - sx) < 20 and abs(ty - sy) < 20:
                    rects = self._card_rects(W, H)
                    for i, rect in enumerate(rects):
                        if rect.collidepoint(tx, ty):
                            if self.selected == i:
                                self._touch_start = None
                                return self.characters[i]
                            self.selected = i
                    btn = self._confirm_btn_rect(W, H)
                    if btn.collidepoint(tx, ty):
                        self._touch_start = None
                        return self.characters[self.selected]
                self._touch_start = None

        return None

    # ── Layout helpers ────────────────────────────────────────────────────────

    def _confirm_btn_rect(self, W, H):
        btn_w = min(int(W * 0.45), 320)
        btn_h = int(H * 0.07)
        return pygame.Rect(W // 2 - btn_w // 2, H - btn_h - int(H * 0.03), btn_w, btn_h)

    # ── Draw ─────────────────────────────────────────────────────────────────

    def draw(self):
        self.init_characters()
        W, H = self.screen.get_size()
        self.screen.fill((10, 10, 22))

        # ── Fundo gradiente simples
        for y in range(0, H, 4):
            alpha = int(30 * (1 - y / H))
            pygame.draw.line(self.screen, (20, 10, 40 + alpha), (0, y), (W, y))

        # ── Título
        font_title_sz = max(22, min(int(H * 0.055), 52))
        font_title = pygame.font.SysFont("Arial", font_title_sz, True)
        title = font_title.render("ESCOLHA SEU GUERREIRO", True, (255, 200, 0))
        self.screen.blit(title, (W // 2 - title.get_width() // 2, int(H * 0.03)))

        # ── Instruções (2 linhas se portrait)
        font_hint_sz = max(13, min(int(H * 0.026), 22))
        font_hint = pygame.font.SysFont("Arial", font_hint_sz)
        if W < H:
            # portrait: 2 linhas
            h1 = font_hint.render("Toque para selecionar  |  Toque 2x para jogar", True, (180, 180, 220))
            self.screen.blit(h1, (W // 2 - h1.get_width() // 2, int(H * 0.10)))
        else:
            hint = font_hint.render("Toque num personagem para selecionar  |  Toque 2x ou CONFIRMAR para jogar", True, (180, 180, 220))
            self.screen.blit(hint, (W // 2 - hint.get_width() // 2, int(H * 0.11)))

        # ── Cards
        rects = self._card_rects(W, H)
        font_name_sz = max(13, min(int(H * 0.032), 28))
        font_name = pygame.font.SysFont("Arial", font_name_sz, True)
        font_stat_sz = max(11, min(int(H * 0.024), 20))
        font_stat = pygame.font.SysFont("Arial", font_stat_sz)

        for i, (char, rect) in enumerate(zip(self.characters, rects)):
            selected = (i == self.selected)

            # Fundo do card
            bg_color   = (30, 60, 100) if selected else (20, 25, 45)
            border_col = (255, 220, 0) if selected else (60, 80, 120)
            border_w   = 3 if selected else 1

            # Sombra suave
            shadow = pygame.Surface((rect.w + 4, rect.h + 4), pygame.SRCALPHA)
            pygame.draw.rect(shadow, (0, 0, 0, 80), shadow.get_rect(), border_radius=12)
            self.screen.blit(shadow, (rect.x + 2, rect.y + 2))

            card_surf = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
            pygame.draw.rect(card_surf, (*bg_color, 220), card_surf.get_rect(), border_radius=10)
            self.screen.blit(card_surf, rect.topleft)
            pygame.draw.rect(self.screen, border_col, rect, border_w, border_radius=10)

            # Sprite do personagem centrado no card
            sprite_area_h = int(rect.h * 0.60)
            sprite_sz = min(rect.w - 20, sprite_area_h)
            sprite_sz = max(sprite_sz, 32)
            try:
                spr = pygame.transform.scale(char.image, (sprite_sz, sprite_sz))
            except Exception:
                spr = pygame.Surface((sprite_sz, sprite_sz), pygame.SRCALPHA)
                pygame.draw.circle(spr, (180, 0, 200), (sprite_sz // 2, sprite_sz // 2), sprite_sz // 2)
            spr_x = rect.x + rect.w // 2 - sprite_sz // 2
            spr_y = rect.y + int(rect.h * 0.05)
            self.screen.blit(spr, (spr_x, spr_y))

            # Nome do personagem
            name_surf = font_name.render(char.name, True, (255, 255, 255) if selected else (200, 210, 230))
            nx = rect.x + rect.w // 2 - name_surf.get_width() // 2
            ny = spr_y + sprite_sz + int(rect.h * 0.04)
            self.screen.blit(name_surf, (nx, ny))

            # Stats compactos
            stat_line = f"❤{char.health}  ⚡{char.speed}  ⚔{char.damage}"
            stat_surf = font_stat.render(stat_line, True, (160, 220, 160) if selected else (120, 160, 120))
            sx2 = rect.x + rect.w // 2 - stat_surf.get_width() // 2
            sy2 = ny + name_surf.get_height() + 2
            self.screen.blit(stat_surf, (sx2, sy2))

        # ── Painel de info do selecionado (footer)
        sel = self.characters[self.selected]
        footer_y = int(H * 0.82)
        font_info = pygame.font.SysFont("Arial", font_stat_sz + 2)

        skill_surf = font_info.render(f"Habilidade: {sel.skill}", True, (80, 200, 255))
        self.screen.blit(skill_surf, (W // 2 - skill_surf.get_width() // 2, footer_y))

        # ── Botão CONFIRMAR
        btn = self._confirm_btn_rect(W, H)
        pygame.draw.rect(self.screen, (0, 180, 60), btn, border_radius=10)
        pygame.draw.rect(self.screen, (0, 255, 80), btn, 2, border_radius=10)
        font_btn = pygame.font.SysFont("Arial", max(16, min(int(H * 0.04), 34)), True)
        lbl = font_btn.render("▶  CONFIRMAR", True, (255, 255, 255))
        self.screen.blit(lbl, (btn.centerx - lbl.get_width() // 2, btn.centery - lbl.get_height() // 2))
