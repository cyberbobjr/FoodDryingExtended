"""Renders the inventory icons of the large fruit slices with the game's own slice mesh.

Usage: blender -b --factory-startup -P source/slices/render_slices.py -- <media_folder> <out_folder> [size]
<media_folder> holds textures/WorldItems/FDX_<Fruit>Slice[Dried].png (recolor_textures.py).
Dried slices use <media_folder>/models_X/WorldItems/FDX_FruitSliceDried.fbx (thin_slice_mesh.py).
Writes <out_folder>/Item_FDX_<Fruit>Slice[Dried].png (size x size, transparent background, default 64).
Mesh: the game's WorldItems/WaterMelonSlice.fbx (read only). Workbench render, flat studio light, closest
texture filtering, Standard view transform (no AgX desaturation).
"""
import math
import os
import sys

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
MEDIA, OUT = argv[0], argv[1]
SIZE = int(argv[2]) if len(argv) > 2 else 64
PZ_MEDIA = os.environ.get("PZ_MEDIA", r"D:\SteamLibrary\steamapps\common\ProjectZomboid\media")
MESH = os.path.join(PZ_MEDIA, "models_X", "WorldItems", "WaterMelonSlice.fbx")
FRUITS = ["Pineapple", "Mango", "Grapefruit"]
# optional reference: the game's own watermelon slice texture, rendered the same way
REFERENCE = os.path.join(PZ_MEDIA, "textures", "WorldItems", "WaterMelonSliceChunks.png")


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.display.shading.light = "STUDIO"
    scene.display.shading.color_type = "TEXTURE"
    scene.display.shading.show_shadows = False
    scene.display.shading.show_cavity = False
    scene.view_settings.view_transform = "Standard"
    scene.render.film_transparent = True
    scene.render.resolution_x = scene.render.resolution_y = SIZE
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    return scene


def import_slice(path=MESH):
    bpy.ops.import_scene.fbx(filepath=path)
    meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    return meshes


def set_texture(meshes, path):
    mat = bpy.data.materials.new("slice")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    tex = nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(path)
    tex.interpolation = "Closest"
    mat.node_tree.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    for o in meshes:
        o.data.materials.clear()
        o.data.materials.append(mat)


def frame(scene, meshes):
    pts = [o.matrix_world @ Vector(c) for o in meshes for c in o.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    center = (lo + hi) / 2
    radius = (hi - lo).length / 2
    cam_data = bpy.data.cameras.new("cam")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = radius * 1.75
    cam = bpy.data.objects.new("cam", cam_data)
    scene.collection.objects.link(cam)
    # 3/4 view from above, like the game's item icons
    direction = Vector((math.cos(math.radians(-45)), math.sin(math.radians(-45)), 0.9)).normalized()
    cam.location = center + direction * radius * 4
    cam.rotation_euler = (center - cam.location).to_track_quat("-Z", "Y").to_euler()
    scene.camera = cam


def main():
    os.makedirs(OUT, exist_ok=True)
    if "--reference" in argv:
        scene = reset()
        meshes = import_slice()
        set_texture(meshes, REFERENCE)
        frame(scene, meshes)
        scene.render.filepath = os.path.join(OUT, "Reference_WatermelonSlice.png")
        bpy.ops.render.render(write_still=True)
    for fruit in FRUITS:
        for state in ("", "Dried"):
            scene = reset()
            # dried slices use the thin mesh of thin_slice_mesh.py
            mesh = os.path.join(MEDIA, "models_X", "WorldItems", "FDX_FruitSliceDried.fbx") if state else MESH
            meshes = import_slice(mesh)
            set_texture(meshes, os.path.join(MEDIA, "textures", "WorldItems", f"FDX_{fruit}Slice{state}.png"))
            frame(scene, meshes)
            scene.render.filepath = os.path.join(OUT, f"Item_FDX_{fruit}Slice{state}.png")
            bpy.ops.render.render(write_still=True)
            print("rendered", scene.render.filepath)


main()
