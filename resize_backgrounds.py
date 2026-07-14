import pygame
import os

base_path = "e:\\AlienFall48"
backgrounds_path = os.path.join(base_path, "assets", "backgrounds")

pygame.init()

# Redimensionar todos os backgrounds para um tamanho visível no mapa (aprox 25% do mapa)
target_width = 1280  # Largura da tela
target_height = 720  # Altura da tela

for filename in os.listdir(backgrounds_path):
    if filename.endswith('.png'):
        filepath = os.path.join(backgrounds_path, filename)
        
        try:
            # Carregar imagem original
            img = pygame.image.load(filepath)
            original_size = img.get_size()
            print(f"Processando {filename}: {original_size}")
            
            # Calcular novo tamanho (aprox tamanho da tela)
            new_size = (target_width, target_height)
            
            # Redimensionar
            resized_img = pygame.transform.scale(img, new_size)
            
            # Salvar versão redimensionada
            pygame.image.save(resized_img, filepath)
            print(f"  Redimensionado para: {new_size}")
            
        except Exception as e:
            print(f"Erro ao processar {filename}: {e}")

print("Redimensionamento concluído!")
