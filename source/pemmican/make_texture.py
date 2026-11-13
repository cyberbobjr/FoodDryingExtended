"""Texture of the pemmican bar (model: the game's WorldItems/GranolaBar mesh, read only).

Usage: python source/pemmican/make_texture.py [out_media_folder]
Writes textures/WorldItems/FDX_Pemmican.png (64x64): pounded dried meat (dark brown, grainy),
pale flecks of fat and dark red bits of dried berries. Uniform pattern, so the mesh UV layout
(made for the granola wrapper) does not matter. Fixed seed: same pixels at every run.
"""
import os
import random
import sys

from PIL import Image

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(__file__), "..", "..", "Contents", "mods", "batman_FoodDryingExtended", "42.21", "media")
SIZE = 64
MEAT = (118, 76, 48)
FAT = (196, 172, 132)
BERRY = (112, 22, 34)


def shade(color, k):
    return tuple(max(0, min(255, int(c * k))) for c in color)


def main():
    rnd = random.Random(1842)
    img = Image.new("RGB", (SIZE, SIZE))
    px = img.load()
    for y in range(SIZE):
        for x in range(SIZE):
            px[x, y] = shade(MEAT, rnd.uniform(0.78, 1.12))
    # fat flecks (1 px) and berry bits (2x2)
    for _ in range(110):
        x, y = rnd.randrange(SIZE), rnd.randrange(SIZE)
        px[x, y] = shade(FAT, rnd.uniform(0.9, 1.05))
    for _ in range(26):
        x, y = rnd.randrange(SIZE - 1), rnd.randrange(SIZE - 1)
        k = rnd.uniform(0.85, 1.1)
        for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
            if dx + dy < 2 or rnd.random() < 0.5:
                px[x + dx, y + dy] = shade(BERRY, k)
    path = os.path.join(OUT, "textures", "WorldItems", "FDX_Pemmican.png")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)
    print("written", path)


main()
