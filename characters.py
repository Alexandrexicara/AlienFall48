import pygame
import os


class Character:

    def __init__(
        self,
        name,
        character_folder,
        health,
        speed,
        damage,
        skill
    ):

        self.name = name
        self.health = health
        self.speed = speed
        self.damage = damage
        self.skill = skill

        # Carregar sprite idle da nova estrutura
        self.image = pygame.image.load(
            os.path.join(
                "assets",
                "player",
                character_folder,
                "idle.png"
            )
        ).convert_alpha()
        
        # Carregar animações
        self.animations = {
            "idle": self.load_animation(character_folder, "idle.png"),
            "walk": self.load_walk_animation(character_folder),
            "run": self.load_run_animation(character_folder),
            "attack": self.load_attack_animation(character_folder),
            "damage": self.load_animation(character_folder, "damage.png"),
            "death": self.load_animation(character_folder, "death.png")
        }
        
        self.current_animation = "idle"
        self.frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.15

    def load_animation(self, character_folder, filename):
        return [pygame.image.load(
            os.path.join("assets", "player", character_folder, filename)
        ).convert_alpha()]

    def load_walk_animation(self, character_folder):
        idle_path = os.path.join("assets", "player", character_folder, "idle.png")
        frames = []
        for i in range(1, 5):
            path = os.path.join("assets", "player", character_folder, f"walk_0{i}.png")
            if os.path.exists(path):
                frames.append(pygame.image.load(path).convert_alpha())
            else:
                frames.append(pygame.image.load(idle_path).convert_alpha())
        return frames

    def load_run_animation(self, character_folder):
        idle_path = os.path.join("assets", "player", character_folder, "idle.png")
        frames = []
        for i in range(1, 3):
            path = os.path.join("assets", "player", character_folder, f"run_0{i}.png")
            if os.path.exists(path):
                frames.append(pygame.image.load(path).convert_alpha())
            else:
                frames.append(pygame.image.load(idle_path).convert_alpha())
        return frames

    def load_attack_animation(self, character_folder):
        idle_path = os.path.join("assets", "player", character_folder, "idle.png")
        frames = []
        for i in range(1, 5):
            path = os.path.join("assets", "player", character_folder, f"attack_0{i}.png")
            if os.path.exists(path):
                frames.append(pygame.image.load(path).convert_alpha())
            else:
                frames.append(pygame.image.load(idle_path).convert_alpha())
        return frames

    def update_animation(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame += 1
            frames = self.animations[self.current_animation]
            if self.frame >= len(frames):
                self.frame = 0
                if self.current_animation in ["attack", "damage", "death"]:
                    self.current_animation = "idle"

    def set_animation(self, animation_name):
        if animation_name in self.animations:
            self.current_animation = animation_name
            self.frame = 0

    def get_current_frame(self):
        frames = self.animations[self.current_animation]
        return frames[self.frame]



# =========================
# PERSONAGENS
# =========================


class Warrior(Character):

    def __init__(self):

        super().__init__(
            "Guerreiro",
            "warrior",
            200,
            250,
            30,
            "Ataque poderoso"
        )



class Soldier(Character):

    def __init__(self):

        super().__init__(
            "Soldado",
            "soldier",
            150,
            280,
            40,
            "Rajada de tiros"
        )



class Sniper(Character):

    def __init__(self):

        super().__init__(
            "Sniper",
            "sniper",
            100,
            220,
            90,
            "Tiro de precisão"
        )



class Medic(Character):

    def __init__(self):

        super().__init__(
            "Médico",
            "medic",
            130,
            240,
            20,
            "Cura aliados"
        )



class Engineer(Character):

    def __init__(self):

        super().__init__(
            "Engenheiro",
            "engineer",
            170,
            230,
            35,
            "Constrói equipamentos"
        )



class Samurai(Character):

    def __init__(self):

        super().__init__(
            "Samurai Futurista",
            "samurai",
            220,
            260,
            70,
            "Golpe de energia"
        )
