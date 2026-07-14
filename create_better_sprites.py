import pygame
import os

# Criar sprites detalhados para os personagens
os.makedirs("assets/player", exist_ok=True)

# Configurações dos sprites
sprite_size = 64

def create_warrior():
    surface = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
    
    # Armadura pesada (vermelho escuro)
    pygame.draw.rect(surface, (100, 30, 30), (12, 18, 40, 46), border_radius=4)
    
    # Detalhes da armadura
    pygame.draw.rect(surface, (80, 20, 20), (14, 20, 36, 20), border_radius=2)
    pygame.draw.line(surface, (150, 50, 50), (32, 20), (32, 40), 2)
    
    # Capacete
    pygame.draw.rect(surface, (120, 40, 40), (16, 4, 32, 16), border_radius=4)
    pygame.draw.rect(surface, (100, 30, 30), (18, 6, 28, 12), border_radius=2)
    
    # Visor
    pygame.draw.rect(surface, (50, 50, 50), (22, 8, 20, 6))
    
    # Espada nas costas
    pygame.draw.rect(surface, (180, 180, 200), (44, 10, 4, 30))
    pygame.draw.rect(surface, (139, 69, 19), (42, 38, 8, 4))
    
    # Braços com proteção
    pygame.draw.rect(surface, (100, 30, 30), (6, 22, 6, 20), border_radius=2)
    pygame.draw.rect(surface, (100, 30, 30), (52, 22, 6, 20), border_radius=2)
    
    # Pernas com armadura
    pygame.draw.rect(surface, (80, 20, 20), (18, 60, 10, 12), border_radius=2)
    pygame.draw.rect(surface, (80, 20, 20), (36, 60, 10, 12), border_radius=2)
    
    return surface

def create_soldier():
    surface = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
    
    # Uniforme militar (azul)
    pygame.draw.rect(surface, (50, 80, 150), (14, 18, 36, 46), border_radius=3)
    
    # Colete tático
    pygame.draw.rect(surface, (40, 60, 120), (16, 20, 32, 24), border_radius=2)
    pygame.draw.rect(surface, (30, 50, 100), (18, 22, 28, 20), border_radius=1)
    
    # Bolsos no colete
    pygame.draw.rect(surface, (60, 90, 160), (20, 26, 10, 8), border_radius=1)
    pygame.draw.rect(surface, (60, 90, 160), (34, 26, 10, 8), border_radius=1)
    
    # Capacete militar
    pygame.draw.ellipse(surface, (60, 90, 160), (16, 2, 32, 18))
    pygame.draw.ellipse(surface, (40, 70, 140), (18, 4, 28, 14))
    
    # Óculos de proteção
    pygame.draw.rect(surface, (30, 30, 30), (22, 8, 20, 6), border_radius=1)
    
    # Rádio no ombro
    pygame.draw.rect(surface, (40, 40, 40), (48, 20, 8, 12), border_radius=1)
    pygame.draw.line(surface, (20, 20, 20), (52, 20), (52, 28), 1)
    
    # Braços
    pygame.draw.rect(surface, (50, 80, 150), (8, 22, 6, 20), border_radius=2)
    pygame.draw.rect(surface, (50, 80, 150), (50, 22, 6, 20), border_radius=2)
    
    # Calças
    pygame.draw.rect(surface, (40, 70, 140), (18, 60, 10, 12), border_radius=2)
    pygame.draw.rect(surface, (40, 70, 140), (36, 60, 10, 12), border_radius=2)
    
    return surface

def create_sniper():
    surface = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
    
    # Roupa de camuflagem (verde)
    pygame.draw.rect(surface, (40, 80, 40), (14, 18, 36, 46), border_radius=3)
    
    # Padrão de camuflagem
    pygame.draw.rect(surface, (30, 60, 30), (16, 20, 8, 10), border_radius=1)
    pygame.draw.rect(surface, (30, 60, 30), (40, 30, 8, 12), border_radius=1)
    pygame.draw.rect(surface, (50, 90, 50), (24, 40, 12, 8), border_radius=1)
    
    # Gorro
    pygame.draw.ellipse(surface, (35, 65, 35), (18, 4, 28, 14))
    
    # Óculos de mira
    pygame.draw.rect(surface, (20, 20, 20), (24, 8, 16, 6), border_radius=1)
    pygame.draw.circle(surface, (40, 40, 40), (32, 11), 2)
    
    # Rifle sniper
    pygame.draw.rect(surface, (60, 50, 40), (44, 24, 6, 32), border_radius=1)
    pygame.draw.rect(surface, (40, 30, 20), (46, 20, 4, 8))
    pygame.draw.line(surface, (30, 30, 30), (47, 22), (47, 54), 1)
    
    # Braços
    pygame.draw.rect(surface, (40, 80, 40), (8, 22, 6, 20), border_radius=2)
    pygame.draw.rect(surface, (40, 80, 40), (50, 22, 6, 20), border_radius=2)
    
    # Pernas
    pygame.draw.rect(surface, (35, 65, 35), (18, 60, 10, 12), border_radius=2)
    pygame.draw.rect(surface, (35, 65, 35), (36, 60, 10, 12), border_radius=2)
    
    return surface

def create_medic():
    surface = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
    
    # Uniforme médico (branco com detalhes vermelhos)
    pygame.draw.rect(surface, (220, 220, 220), (14, 18, 36, 46), border_radius=3)
    
    # Cruz vermelha no peito
    pygame.draw.rect(surface, (200, 50, 50), (28, 24, 8, 20), border_radius=1)
    pygame.draw.rect(surface, (200, 50, 50), (24, 28, 16, 12), border_radius=1)
    
    # Boné médico
    pygame.draw.ellipse(surface, (200, 50, 50), (18, 4, 28, 12))
    pygame.draw.ellipse(surface, (180, 40, 40), (20, 6, 24, 8))
    
    # Cruz no boné
    pygame.draw.rect(surface, (255, 255, 255), (30, 6, 4, 6))
    pygame.draw.rect(surface, (255, 255, 255), (28, 8, 8, 2))
    
    # Maletinha médica
    pygame.draw.rect(surface, (180, 180, 180), (48, 30, 10, 14), border_radius=2)
    pygame.draw.rect(surface, (200, 50, 50), (50, 34, 6, 6), border_radius=1)
    
    # Braços
    pygame.draw.rect(surface, (220, 220, 220), (8, 22, 6, 20), border_radius=2)
    pygame.draw.rect(surface, (220, 220, 220), (50, 22, 6, 20), border_radius=2)
    
    # Pernas
    pygame.draw.rect(surface, (200, 200, 200), (18, 60, 10, 12), border_radius=2)
    pygame.draw.rect(surface, (200, 200, 200), (36, 60, 10, 12), border_radius=2)
    
    return surface

def create_engineer():
    surface = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
    
    # Uniforme de engenheiro (roxo escuro)
    pygame.draw.rect(surface, (80, 40, 120), (14, 18, 36, 46), border_radius=3)
    
    # Cinto com ferramentas
    pygame.draw.rect(surface, (60, 30, 100), (14, 38, 36, 6), border_radius=1)
    pygame.draw.rect(surface, (100, 100, 100), (18, 40, 8, 4), border_radius=1)
    pygame.draw.rect(surface, (100, 100, 100), (38, 40, 8, 4), border_radius=1)
    
    # Capacete de engenheiro
    pygame.draw.rect(surface, (100, 50, 150), (16, 4, 32, 14), border_radius=3)
    pygame.draw.rect(surface, (80, 40, 120), (18, 6, 28, 10), border_radius=2)
    
    # Lanterna no capacete
    pygame.draw.circle(surface, (255, 255, 200), (44, 10), 3)
    
    # Chave inglesa
    pygame.draw.rect(surface, (150, 150, 150), (48, 22, 8, 16), border_radius=1)
    pygame.draw.circle(surface, (130, 130, 130), (52, 26), 3)
    
    # Braços
    pygame.draw.rect(surface, (80, 40, 120), (8, 22, 6, 20), border_radius=2)
    pygame.draw.rect(surface, (80, 40, 120), (50, 22, 6, 20), border_radius=2)
    
    # Pernas
    pygame.draw.rect(surface, (70, 35, 110), (18, 60, 10, 12), border_radius=2)
    pygame.draw.rect(surface, (70, 35, 110), (36, 60, 10, 12), border_radius=2)
    
    return surface

def create_samurai():
    surface = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
    
    # Armadura de samurai (laranja/dourado)
    pygame.draw.rect(surface, (180, 100, 30), (12, 18, 40, 46), border_radius=3)
    
    # Detalhes da armadura
    pygame.draw.rect(surface, (150, 80, 20), (14, 20, 36, 20), border_radius=2)
    pygame.draw.line(surface, (200, 120, 50), (32, 20), (32, 40), 2)
    
    # Elmo de samurai
    pygame.draw.polygon(surface, (200, 120, 50), [(16, 8), (32, 2), (48, 8), (48, 16), (16, 16)])
    pygame.draw.polygon(surface, (180, 100, 30), [(18, 10), (32, 4), (46, 10), (46, 14), (18, 14)])
    
    # Máscara facial
    pygame.draw.rect(surface, (150, 80, 20), (22, 14, 20, 8), border_radius=2)
    
    # Katana nas costas
    pygame.draw.rect(surface, (180, 180, 200), (44, 8, 3, 36))
    pygame.draw.rect(surface, (139, 69, 19), (42, 42, 7, 4))
    pygame.draw.circle(surface, (200, 180, 50), (45, 46), 2)
    
    # Braços com proteção
    pygame.draw.rect(surface, (180, 100, 30), (6, 22, 6, 20), border_radius=2)
    pygame.draw.rect(surface, (180, 100, 30), (52, 22, 6, 20), border_radius=2)
    
    # Pernas
    pygame.draw.rect(surface, (150, 80, 20), (18, 60, 10, 12), border_radius=2)
    pygame.draw.rect(surface, (150, 80, 20), (36, 60, 10, 12), border_radius=2)
    
    return surface

# Criar todos os sprites
sprites = {
    "warrior.png": create_warrior(),
    "soldier.png": create_soldier(),
    "sniper.png": create_sniper(),
    "medic.png": create_medic(),
    "engineer.png": create_engineer(),
    "samurai.png": create_samurai()
}

for filename, surface in sprites.items():
    pygame.image.save(surface, os.path.join("assets/player", filename))
    print(f"Sprite criado: {filename}")

print("Todos os sprites detalhados foram criados com sucesso!")
