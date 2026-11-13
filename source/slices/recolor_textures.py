"""Textures of the large fruit slices, recoloured from the game's watermelon slice.

Usage: python source/slices/recolor_textures.py [out_media_folder]
Reads (read only) the vanilla watermelon slice textures and writes, for pineapple, mango and grapefruit,
a fresh and a dried texture for the world model (WorldItems/WaterMelonSlice mesh) and for the hand model
(MelonSlice mesh). Each pixel keeps its brightness relative to its zone (flesh, light rind, rind, seeds),
so the game's grain stays; the dried version is darker, browner and less saturated.
"""
import colorsys
import os
import sys

from PIL import Image

PZ_MEDIA = os.environ.get("PZ_MEDIA", r"D:\SteamLibrary\steamapps\common\ProjectZomboid\media")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(__file__), "..", "..", "Contents", "mods", "batman_FoodDryingExtended", "42.21", "media")

# zone -> colour (r, g, b); seeds: None = same as flesh (no seeds)
FRUITS = {
    "Pineapple": {"flesh": (240, 205, 75), "lightrind": (250, 232, 160), "rind": (150, 112, 42), "seed": None},
    "Mango": {"flesh": (250, 162, 38), "lightrind": (255, 205, 95), "rind": (112, 140, 52), "seed": None},
    "Grapefruit": {"flesh": (236, 98, 92), "lightrind": (250, 236, 216), "rind": (240, 182, 62), "seed": (245, 226, 190)},
}
SOURCES = {
    # vanilla texture -> output name pattern
    os.path.join("textures", "WorldItems", "WaterMelonSliceChunks.png"): os.path.join("textures", "WorldItems", "FDX_{fruit}Slice{state}.png"),
    os.path.join("textures", "MelonSlice.png"): os.path.join("textures", "FDX_{fruit}SliceHand{state}.png"),
}


def zone(rgb):
    r, g, b = rgb
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    if r > g + 30:
        return "flesh"
    if s < 0.25:
        return "seed"
    return "lightrind" if v > 0.7 else "rind"


def luminance(rgb):
    r, g, b = rgb
    return 0.299 * r + 0.587 * g + 0.114 * b


def dry(rgb):
    """Dried look: toward brown, less saturated, darker."""
    r, g, b = (c / 255 for c in rgb)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    r, g, b = colorsys.hsv_to_rgb(h, s * 0.8, v * 0.72)
    brown = (0.45, 0.27, 0.12)
    mix = 0.25
    return tuple(int(255 * ((1 - mix) * c + mix * bc)) for c, bc in zip((r, g, b), brown))


def recolor(src, palette, dried):
    im = Image.open(src).convert("RGB")
    pixels = list(im.get_flattened_data()) if hasattr(im, "get_flattened_data") else list(im.getdata())
    zones = [zone(p) for p in pixels]
    mean = {}
    for z in set(zones):
        values = [luminance(p) for p, zz in zip(pixels, zones) if zz == z]
        mean[z] = sum(values) / len(values)
    out = []
    for p, z in zip(pixels, zones):
        target = palette[z] or palette["flesh"]
        # no seeds in this fruit: seed pixels take the plain flesh colour (no dark spots)
        ratio = 1.0 if palette[z] is None else (luminance(p) / mean[z] if mean[z] else 1.0)
        ratio = max(0.6, min(1.4, ratio))
        color = tuple(max(0, min(255, int(c * ratio))) for c in target)
        out.append(dry(color) if dried else color)
    res = Image.new("RGB", im.size)
    res.putdata(out)
    return res


def main():
    for src, pattern in SOURCES.items():
        for fruit, palette in FRUITS.items():
            for state, dried in (("", False), ("Dried", True)):
                # dried slices are held with their own thin world mesh: no dried hand texture
                if dried and "Hand" in pattern:
                    continue
                path = os.path.join(OUT, pattern.format(fruit=fruit, state=state))
                os.makedirs(os.path.dirname(path), exist_ok=True)
                recolor(os.path.join(PZ_MEDIA, src), palette, dried).save(path)
                print("written", os.path.relpath(path, OUT))


main()
