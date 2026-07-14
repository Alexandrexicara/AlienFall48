import pygame
import os

# Criar sprite para o alienígena
os.makedirs("assets/enemies", exist_ok=True)

sprite_size = 128

def create_alien():
    surface = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
    
    # Corpo do alien (verde)
    pygame.draw.ellipse(surface, (50, 150, 50), (32, 32, 64, 64))
    
    # Cabeça maior
    pygame.draw.ellipse(surface, (40, 130, 40), (40, 16, 48, 48))
    
    # Olhos grandes e pretos
    pygame.draw.ellipse(surface, (20, 20, 20), (48, 24, 16, 20))
    pygame.draw.ellipse(surface, (20, 20, 20), (64, 24, 16, 20))
    
    # Brilho nos olhos
    pygame.draw.circle(surface, (100, 200, 100), (52, 28), 3)
    pygame.draw.circle(surface, (100, 200, 100), (68, 28), 3)
    
    # Boca pequena
    pygame.draw.ellipse(surface, (30, 100, 30), (56, 44, 16, 8))
    
    # Antenas
    pygame.draw.line(surface, (60, 160, 60), (52, 16), (44, 4), 3)
    pygame.draw.line(surface, (60, 160, 60), (76, 16), (84, 4), 3)
    pygame.draw.circle(surface, (80, 180, 80), (44, 4), 4)
    pygame.draw.circle(surface, (80, 180, 80), (84, 4), 4)
    
    # Braços longos
    pygame.draw.ellipse(surface, (45, 140, 45), (20, 40, 16, 40))
    pygame.draw.ellipse(surface, (45, 140, 45), (92, 40, 16, 40))
    
    # Mãos com garras
    pygame.draw.circle(surface, (40, 130, 40), (28, 76), 6)
    pygame.draw.circle(surface, (40, 130, 40), (100, 76), 6)
    
    # Pernas
    pygame.draw.ellipse(surface, (45, 140, 45), (40, 80, 16, 32))
    pygame.draw.ellipse(surface, (45, 140, 45), (72, 80, 16, 32))
    
    # Pés
    pygame.draw.ellipse(surface, (40, 130, 40), (36, 104, 20, 12))
    pygame.draw.ellipse(surface, (40, 130, 40), (72, 104, 20, 12))
    
    return surface

# Criar frames de animação (4 frames)
for i in range(4):
    surface = create_alien()
    
    # Adicionar pequena variação para animação
    offset_y = i * 2
    if i > 1:
        offset_y = (4 - i) * 2
    
    # Criar surface final com offset
    final_surface = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
    final_surface.blit(surface, (0, offset_y))
    
    pygame.image.save(final_surface, os.path.join("assets/enemies", f"alien_frame_{i}.png"))
    print(f"Frame {i} criado")

# Criar sprite sheet combinando os frames
sprite_sheet = pygame.Surface((128, 32), pygame.SRCALPHA)
for i in range(4):
    frame = pygame.image.load(os.path.join("assets/enemies", f"alien_frame_{i}.png"))
    frame_scaled = pygame.transform.scale(frame, (32, 32))
    sprite_sheet.blit(frame_scaled, (i * 32, 0))

pygame.image.save(sprite_sheet, os.path.join("assets/enemies", "alien01.png"))
print("Sprite sheet alien01.png criado com sucesso!")

# Limpar frames temporários
for i in range(4):
    os.remove(os.path.join("assets/enemies", f"alien_frame_{i}.png"))

print("Sprites do alienígena criados!")
