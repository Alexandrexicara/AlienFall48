import os

base_path = "e:\\AlienFall48"

# Arquivos antigos para remover
old_files = [
    "assets/player/warrior.png",
    "assets/player/soldier.png",
    "assets/player/sniper.png",
    "assets/player/medic.png",
    "assets/player/engineer.png",
    "assets/player/samurai.png",
    "assets/enemies/alien01.png"
]

for file_path in old_files:
    full_path = os.path.join(base_path, file_path)
    if os.path.exists(full_path):
        os.remove(full_path)
        print(f"Removido: {file_path}")

print("Limpeza concluída!")
