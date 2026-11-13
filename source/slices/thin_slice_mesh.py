"""Thin variant of the game's watermelon slice mesh, for dried fruit slices.

Usage: python source/slices/thin_slice_mesh.py [out_media_folder] [ratio]
Copies media/models_X/WorldItems/WaterMelonSlice.fbx (read only) and scales the thickness axis (geometry Z,
from 0 to 2.887) of its 8 vertices by `ratio` (default 0.4), in place: the vertex array is stored raw
(encoding 0), so the file keeps the same size and every node transform (Lcl Scaling 0.028, pre/geometric
rotations) stays untouched, so the game sizes and places it like the original.
Writes models_X/WorldItems/FDX_FruitSliceDried.fbx.
"""
import os
import struct
import sys

PZ_MEDIA = os.environ.get("PZ_MEDIA", r"D:\SteamLibrary\steamapps\common\ProjectZomboid\media")
SRC = os.path.join(PZ_MEDIA, "models_X", "WorldItems", "WaterMelonSlice.fbx")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(__file__), "..", "..", "Contents", "mods", "batman_FoodDryingExtended", "42.21", "media")
RATIO = float(sys.argv[2]) if len(sys.argv) > 2 else 0.4


def main():
    data = bytearray(open(SRC, "rb").read())
    name = b"\x08Vertices"
    at = data.find(name)
    assert at > 0 and data.find(name, at + 1) == -1, "expected exactly one Vertices array"
    pos = at + len(name)
    assert chr(data[pos]) == "d", "Vertices must be a double array"
    count, encoding, length = struct.unpack_from("<III", data, pos + 1)
    assert encoding == 0 and length == count * 8, "Vertices must be stored raw (encoding 0)"
    start = pos + 13
    values = list(struct.unpack_from("<%dd" % count, data, start))
    for i in range(2, count, 3):
        values[i] *= RATIO
    struct.pack_into("<%dd" % count, data, start, *values)
    path = os.path.join(OUT, "models_X", "WorldItems", "FDX_FruitSliceDried.fbx")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data)
    print("written", path, "thickness ratio", RATIO)


main()
