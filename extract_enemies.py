from PIL import Image, ImageDraw
import os
import numpy as np

img = Image.open("/home/ubuntu/workspace/project/attachements/WhatsApp Image 2026-08-04 at 18.54.21-1786219320501.jpeg")

def remove_bg_color(pil_img):
    """Remove background dark-blue color and JPEG compression artifacts near edges."""
    result = pil_img.convert("RGBA")
    arr = np.array(result, dtype=np.int32)
    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    # Primary background: very dark blue-black (R<30, G<45, B<60)
    is_bg = (r < 30) & (g < 45) & (b < 62)
    # Also remove near-background (JPEG artifact blends): pixels with low saturation
    # where saturation = max(rgb) - min(rgb) < 15 and brightness < 60
    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)
    sat = max_c - min_c
    is_artifact = (max_c < 65) & (sat < 20)
    is_bg = is_bg | is_artifact
    arr[is_bg] = [0, 0, 0, 0]
    return Image.fromarray(arr.astype(np.uint8), 'RGBA')


# Labels em Y (detectados por scan): header=65-71, idle_lbl=143, walk01_lbl=209-212,
# walk02_lbl=272-276, atk01_lbl=336-339, dmg_lbl=399-402, death_lbl=459-462
# Sprite de cada frame começa LOGO APÓS o label anterior:
#   idle:      Y=72-142   (após header Y=65-71, antes idle_lbl Y=143)
#   walk_01:   Y=163-208  (após idle_lbl+fundo Y=143-162, antes walk01_lbl Y=209)
#   walk_02:   Y=226-271  (após walk01_lbl+fundo Y=209-225, antes walk02_lbl Y=272)
#   attack_01: Y=290-335  (após walk02_lbl+fundo Y=272-289, antes atk01_lbl Y=336)
#   damage:    Y=355-398  (após atk01_lbl+fundo Y=336-354, antes dmg_lbl Y=399)
#   death:     Y=418-458  (após dmg_lbl+fundo Y=399-417, antes death_lbl Y=459)


# Label positions (from scan):
#   header:    Y=65-71   ("DRONE ALIEN" / "ALIEN BRUTE" etc.)
#   idle_lbl:  Y=143     ("idle.png")     → after: Y=148
#   walk01_lbl:Y=209-212 ("walk_01.png")  → after: Y=217
#   walk02_lbl:Y=272-276 ("walk_02.png")  → after: Y=281
#   atk01_lbl: Y=336-339 ("attack_01.png")→ after: Y=344
#   dmg_lbl:   Y=399-402 ("damage.png")   → after: Y=407
#   death_lbl: Y=459-462 ("death.png")
#
# Sprite region = [label_before_end+5 ... next_label_start-3]
#   idle:      Y=72  - 140  (header ends 71, next label starts 143)
#   walk_01:   Y=148 - 206  (idle_lbl ends 143, next label starts 209)
#   walk_02:   Y=217 - 269  (walk01_lbl ends 212, next label starts 272)
#   attack_01: Y=281 - 333  (walk02_lbl ends 276, next label starts 336)
#   damage:    Y=344 - 396  (atk01_lbl ends 339, next label starts 399)
#   death:     Y=407 - 456  (dmg_lbl ends 402, death_lbl starts 459)

ENEMY_SPEC = {
    "drone":    {"x": (855, 968),  "frames": [("idle",72,140),("walk_01",148,206),("walk_02",217,269),("attack_01",281,333),("damage",344,396),("death",407,456)]},
    "brute":    {"x": (968, 1082), "frames": [("idle",72,140),("walk_01",148,206),("walk_02",217,269),("attack_01",281,333),("damage",344,396),("death",407,456)]},
    "spider":   {"x": (1082,1195), "frames": [("idle",72,140),("walk_01",148,206),("walk_02",217,269),("attack_01",281,333),("damage",344,396),("death",407,456)]},
    "parasite": {"x": (1195,1309), "frames": [("idle",72,140),("walk_01",148,206),("walk_02",217,269),("attack_01",281,333),("damage",344,396),("death",407,456)]},
    "queen":    {"x": (1309,1422), "frames": [("idle",72,199),("walk_01",206,331),("attack_01",338,455)]},
    "boss":     {"x": (1422,1536), "frames": [("idle",72,197),("walk_01",204,323),("attack_01",330,455)]},
}

needed_frames = ["idle", "walk_01", "walk_02", "attack_01", "damage", "death"]
sub_map = {"walk_02": "walk_01", "damage": "attack_01", "death": "attack_01"}

ok = 0
for cname, spec in ENEMY_SPEC.items():
    out_dir = f"/home/ubuntu/workspace/alienfall48/assets/enemies/{cname}"
    os.makedirs(out_dir, exist_ok=True)
    x1, x2 = spec["x"]
    saved = {}
    for fname, y1, y2 in spec["frames"]:
        crop = img.crop((x1, y1, x2, y2))
        transparent = remove_bg_color(crop)
        final = transparent.resize((64, 64), Image.LANCZOS)
        final.save(f"{out_dir}/{fname}.png", "PNG")
        saved[fname] = final
        ok += 1
    for need in needed_frames:
        if need not in saved:
            src = sub_map.get(need, "idle")
            if src in saved:
                saved[src].save(f"{out_dir}/{need}.png", "PNG")
                ok += 1

print(f"OK {ok} sprites")

cell = 96
panel = Image.new("RGBA", (len(needed_frames)*(cell+4)+80, len(ENEMY_SPEC)*(cell+4)+30), (20,20,30,255))
draw = ImageDraw.Draw(panel)
for ri, cname in enumerate(ENEMY_SPEC.keys()):
    draw.text((2, 30+ri*(cell+4)+cell//2-5), cname[:7], fill=(100,200,255,255))
    for ci, fname in enumerate(needed_frames):
        p = f"/home/ubuntu/workspace/alienfall48/assets/enemies/{cname}/{fname}.png"
        if os.path.exists(p):
            sp = Image.open(p).convert("RGBA")
            bg = Image.new("RGBA", (cell,cell), (35,35,45,255))
            resized = sp.resize((cell,cell), Image.NEAREST)
            bg.paste(resized,(0,0),resized)
            panel.paste(bg, (80+ci*(cell+4), 30+ri*(cell+4)))
            if ri==0:
                draw.text((80+ci*(cell+4)+2, 5), fname[:8], fill=(200,255,100,255))
small = panel.resize((panel.width*2//3, panel.height*2//3), Image.LANCZOS)
small.save("/home/ubuntu/workspace/project/public/enemies_v7.png", optimize=True, quality=85)
print(f"Preview: {small.size}")
