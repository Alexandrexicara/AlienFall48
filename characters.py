import pygame
import os


class Character:

    def __init__(self, name, character_folder, health, speed, damage, skill):
        self.name   = name
        self.health = health
        self.speed  = speed
        self.damage = damage
        self.skill  = skill

        # Sprite idle principal (usado como thumbnail)
        idle_path = os.path.join("assets", "player", character_folder, "idle.png")
        raw = pygame.image.load(idle_path).convert_alpha()
        # 200% scale para thumbnail também
        self.image = pygame.transform.scale(raw, (raw.get_width()*2, raw.get_height()*2))

        # 11 frames reais do asset pack (sem run_01/run_02 que não existem)
        self.animations = {
            "idle":   self._load_frames(character_folder, ["idle"]),
            "walk":   self._load_frames(character_folder, ["walk_01","walk_02","walk_03","walk_04"]),
            "attack": self._load_frames(character_folder, ["attack_01","attack_02","attack_03","attack_04"]),
            "damage": self._load_frames(character_folder, ["damage"]),
            "death":  self._load_frames(character_folder, ["death"]),
        }
        # run usa walk (não há run na sheet)
        self.animations["run"] = self.animations["walk"]

        self.current_animation = "idle"
        self.frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.12

    def _load_frames(self, folder, names):
        """Carrega frames; fallback para idle se arquivo não existir."""
        idle_path = os.path.join("assets", "player", folder, "idle.png")
        frames = []
        for name in names:
            path = os.path.join("assets", "player", folder, f"{name}.png")
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                frames.append(img)
        if not frames:
            frames = [pygame.image.load(idle_path).convert_alpha()]
        return frames

    def update_animation(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame += 1
            frames = self.animations[self.current_animation]
            if self.frame >= len(frames):
                self.frame = 0
                if self.current_animation in ("attack", "damage", "death"):
                    self.current_animation = "idle"

    def set_animation(self, animation_name):
        key = animation_name if animation_name in self.animations else "idle"
        if self.current_animation != key:
            self.current_animation = key
            self.frame = 0

    def get_current_frame(self):
        frames = self.animations[self.current_animation]
        return frames[self.frame % len(frames)]


# =========================
# PERSONAGENS
# =========================

class Warrior(Character):
    def __init__(self):
        super().__init__("Guerreiro",        "warrior",  200, 250, 30, "Ataque poderoso")

class Soldier(Character):
    def __init__(self):
        super().__init__("Soldado",          "soldier",  150, 280, 40, "Rajada de tiros")

class Sniper(Character):
    def __init__(self):
        super().__init__("Sniper",           "sniper",   100, 220, 90, "Tiro de precisão")

class Medic(Character):
    def __init__(self):
        super().__init__("Médico",           "medic",    130, 240, 20, "Cura aliados")

class Engineer(Character):
    def __init__(self):
        super().__init__("Engenheiro",       "engineer", 170, 230, 35, "Constrói equipamentos")

class Samurai(Character):
    def __init__(self):
        super().__init__("Samurai Futurista","samurai",  220, 260, 70, "Golpe de energia")
