import os

base_path = "e:\\AlienFall48"

# Criar estrutura completa de pastas
folders = [
    "assets/backgrounds",
    "assets/player/warrior",
    "assets/player/soldier",
    "assets/player/sniper",
    "assets/player/medic",
    "assets/player/engineer",
    "assets/player/samurai",
    "assets/enemies/alien01",
    "assets/enemies/alien_brute",
    "assets/enemies/alien_spider",
    "assets/enemies/alien_parasite",
    "assets/enemies/alien_sniper",
    "assets/enemies/alien_robot",
    "assets/enemies/alien_flying",
    "assets/enemies/alien_tank",
    "assets/enemies/alien_queen",
    "assets/bosses/queen",
    "assets/bosses/titan",
    "assets/bosses/overlord",
    "assets/bosses/emperor",
    "assets/weapons",
    "assets/bullets",
    "assets/items",
    "assets/vehicles",
    "assets/ui",
    "assets/effects/explosion",
    "assets/effects/fire",
    "assets/effects/smoke",
    "assets/effects/blood",
    "assets/effects/laser",
    "assets/effects/electric",
    "assets/sounds/weapons",
    "assets/sounds/aliens",
    "assets/sounds/player",
    "assets/sounds/ui",
    "assets/sounds/ambient",
    "assets/music",
    "assets/fonts",
    "saves",
    "docs"
]

for folder in folders:
    full_path = os.path.join(base_path, folder)
    os.makedirs(full_path, exist_ok=True)
    print(f"Criado: {folder}")

print("Estrutura de pastas criada com sucesso!")
