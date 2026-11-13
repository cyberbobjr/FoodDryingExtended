"""Poster of Food Drying Extended: original Food Drying artwork with a horizontal
ribbon at the bottom (25 % of the height) in the house colours: orange edges,
cream band, navy text.

Usage: python source/make_poster.py <out.png>   (Pillow)
"""
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

SRC = r"D:\SteamLibrary\steamapps\workshop\content\108600\3747396551\mods\FoodDrying\42\poster.png"
ORANGE = (255, 179, 29)
CREAM = (254, 247, 226)
NAVY = (8, 39, 65)
TEXT = "EXTENDED"


def make(out, height_ratio=0.25, edge_ratio=0.12):
    base = Image.open(SRC).convert("RGBA")
    W, H = base.size
    S = 4  # supersampling
    bh = int(H * height_ratio)
    band = Image.new("RGBA", (W * S, bh * S), CREAM + (255,))
    d = ImageDraw.Draw(band)
    e = int(bh * edge_ratio) * S
    d.rectangle([0, 0, W * S, e], fill=ORANGE)
    d.rectangle([0, bh * S - e, W * S, bh * S], fill=ORANGE)
    font = ImageFont.truetype(r"C:\Windows\Fonts\impact.ttf", int(bh * 0.52) * S)
    bb = d.textbbox((0, 0), TEXT, font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    d.text(((W * S - tw) // 2 - bb[0], (bh * S - th) // 2 - bb[1]), TEXT, font=font, fill=NAVY)
    band = band.resize((W, bh), Image.LANCZOS)

    y = H - bh
    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rectangle([0, y - 4, W, H], fill=(0, 0, 0, 150))
    base = Image.alpha_composite(base, shadow.filter(ImageFilter.GaussianBlur(6)))
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    layer.paste(band, (0, y))
    base = Image.alpha_composite(base, layer)
    base.convert("RGB").save(out)


make(sys.argv[1] if len(sys.argv) > 1 else "poster.png")
