import pygame
import os

# Criar sprites temporários para os personagens
os.makedirs("assets/player", exist_ok=True)

# Configurações dos sprites
sprite_size = 64

# Cores para cada personagem
character_colors = {
    "warrior.png": (150, 50, 50),      # Vermelho escuro
    "soldier.png": (50, 100, 200),     # Azul
    "sniper.png": (50, 150, 50),       # Verde
    "medic.png": (200, 200, 50),       # Amarelo
    "engineer.png": (150, 50, 150),    # Roxo
    "samurai.png": (200, 100, 50)      # Laranja
}

for filename, color in character_colors.items():
    surface = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
    
    # Desenhar corpo do personagem
    pygame.draw.rect(surface, color, (16, 20, 32, 44))
    
    # Desenhar cabeça
    pygame.draw.circle(surface, (255, 220, 180), (32, 12), 10)
    
    # Desenhar olhos
    pygame.draw.circle(surface, (0, 0, 0), (28, 10), 2)
    pygame.draw.circle(surface, (0, 0, 0), (36, 10), 2)
    
    # Desenhar braços
    pygame.draw.rect(surface, color, (8, 24, 8, 20))
    pygame.draw.rect(surface, color, (48, 24, 8, 20))
    
    # Desenhar pernas
    pygame.draw.rect(surface, (100, 100, 100), (20, 60, 8, 12))
    pygame.draw.rect(surface, (100, 100, 100), (36, 60, 8, 12))
    
    # Salvar sprite
    pygame.image.save(surface, os.path.join("assets/player", filename))
    print(f"Sprite criado: {filename}")

print("Todos os sprites foram criados com sucesso!")
