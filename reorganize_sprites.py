import pygame
import os
import shutil

base_path = "e:\\AlienFall48"

# Mover sprites existentes para as novas pastas
character_sprites = {
    "warrior.png": "assets/player/warrior/idle.png",
    "soldier.png": "assets/player/soldier/idle.png",
    "sniper.png": "assets/player/sniper/idle.png",
    "medic.png": "assets/player/medic/idle.png",
    "engineer.png": "assets/player/engineer/idle.png",
    "samurai.png": "assets/player/samurai/idle.png"
}

# Copiar sprites para as novas localizações
for old_name, new_path in character_sprites.items():
    old_path = os.path.join(base_path, "assets/player", old_name)
    new_full_path = os.path.join(base_path, new_path)
    
    if os.path.exists(old_path):
        shutil.copy(old_path, new_full_path)
        print(f"Copiado: {old_name} -> {new_path}")
        
        # Criar cópias para outras animações (usando o mesmo sprite por enquanto)
        base_dir = os.path.dirname(new_full_path)
        character_name = os.path.basename(base_dir)
        
        # Criar walk frames
        for i in range(1, 5):
            walk_path = os.path.join(base_dir, f"walk_0{i}.png")
            shutil.copy(old_path, walk_path)
            
        # Criar run frames
        for i in range(1, 3):
            run_path = os.path.join(base_dir, f"run_0{i}.png")
            shutil.copy(old_path, run_path)
            
        # Criar attack frames
        for i in range(1, 5):
            attack_path = os.path.join(base_dir, f"attack_0{i}.png")
            shutil.copy(old_path, attack_path)
            
        # Criar damage e death
        damage_path = os.path.join(base_dir, "damage.png")
        death_path = os.path.join(base_dir, "death.png")
        shutil.copy(old_path, damage_path)
        shutil.copy(old_path, death_path)
        
        print(f"  Criadas animações para {character_name}")

# Mover alien para nova estrutura
alien_old = os.path.join(base_path, "assets/enemies/alien01.png")
alien_new = os.path.join(base_path, "assets/enemies/alien01/idle.png")

if os.path.exists(alien_old):
    shutil.copy(alien_old, alien_new)
    print(f"Copiado: alien01.png -> assets/enemies/alien01/idle.png")

print("Reorganização completa!")
