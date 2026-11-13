"""Pemmican bar: mesh, world model FBX and inventory icon.

Usage (headless): blender -b --factory-startup -P source/pemmican/build_pemmican.py -- <media_folder> [icon_size]
Needs <media_folder>/textures/WorldItems/FDX_Pemmican.png (make_texture.py).
Writes <media_folder>/models_X/WorldItems/FDX_Pemmican.fbx and <media_folder>/textures/Item_FDX_Pemmican.png.
Works in its own scene "FDX_Pemmican" (safe to run inside an open Blender through the MCP: call run(media)).

Mesh: hand-pressed block of 10 x 4.5 x 2.2 cm, bevelled, small fixed jitter. Exported in metres
(apply_unit_scale, no baked space transform): Lcl Scaling 100, so the model script uses scale = 0.01.
"""
import math
import os
import random
import sys

import bmesh
import bpy
from mathutils import Vector

SCENE = "FDX_Pemmican"
SIZE_M = (0.10, 0.045, 0.022)


def scene():
    sc = bpy.data.scenes.get(SCENE) or bpy.data.scenes.new(SCENE)
    for o in list(sc.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    if not bpy.app.background:
        bpy.context.window.scene = sc
    sc.render.engine = "BLENDER_WORKBENCH"
    sh = sc.display.shading
    sh.light, sh.color_type, sh.show_shadows, sh.show_cavity = "STUDIO", "TEXTURE", False, False
    sc.view_settings.view_transform = "Standard"
    sc.render.film_transparent = True
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    return sc


def build(sc, media):
    me = bpy.data.meshes.new("FDX_Pemmican")
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Vector((v.co.x * SIZE_M[0], v.co.y * SIZE_M[1], (v.co.z + 0.5) * SIZE_M[2]))
    bmesh.ops.bevel(bm, geom=list(bm.edges), offset=0.004, segments=2, affect="EDGES")
    rnd = random.Random(1842)
    for v in bm.verts:
        if v.co.z > 0.001:  # bottom stays flat on the ground
            v.co += Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1))) * 0.0012
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new("FDX_Pemmican", me)
    sc.collection.objects.link(obj)
    for p in me.polygons:
        p.use_smooth = False
    # box projection of the uniform texture
    uv = me.uv_layers.new(name="UVMap")
    for poly in me.polygons:
        n = poly.normal
        axes = (1, 2) if abs(n.x) >= max(abs(n.y), abs(n.z)) else (0, 2) if abs(n.y) >= abs(n.z) else (0, 1)
        for li in poly.loop_indices:
            co = me.vertices[me.loops[li].vertex_index].co
            uv.data[li].uv = (co[axes[0]] / 0.1 + 0.5, co[axes[1]] / 0.1 + 0.5)
    mat = bpy.data.materials.new("FDX_Pemmican")
    mat.use_nodes = True
    tex = mat.node_tree.nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(os.path.join(media, "textures", "WorldItems", "FDX_Pemmican.png"), check_existing=False)
    tex.interpolation = "Closest"
    mat.node_tree.links.new(tex.outputs["Color"], mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"])
    me.materials.append(mat)
    return obj


def export(sc, obj, media):
    path = os.path.join(media, "models_X", "WorldItems", "FDX_Pemmican.fbx")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with bpy.context.temp_override(scene=sc, selected_objects=[obj], active_object=obj):
        bpy.ops.export_scene.fbx(filepath=path, use_selection=True, object_types={"MESH"}, apply_unit_scale=True,
                                 bake_space_transform=False, mesh_smooth_type="FACE", add_leaf_bones=False)
    return path


def render_icon(sc, obj, out, size):
    lo = Vector([min(c[i] for c in obj.bound_box) for i in range(3)])
    hi = Vector([max(c[i] for c in obj.bound_box) for i in range(3)])
    center, radius = (lo + hi) / 2, (hi - lo).length / 2
    cd = bpy.data.cameras.new("pem_cam")
    cd.type, cd.ortho_scale = "ORTHO", radius * 1.75
    cam = bpy.data.objects.new("pem_cam", cd)
    sc.collection.objects.link(cam)
    d = Vector((math.cos(math.radians(-45)), math.sin(math.radians(-45)), 0.9)).normalized()
    cam.location = center + d * radius * 4
    cam.rotation_euler = (center - cam.location).to_track_quat("-Z", "Y").to_euler()
    sc.camera = cam
    sc.render.resolution_x = sc.render.resolution_y = size
    sc.render.filepath = out
    with bpy.context.temp_override(scene=sc):
        bpy.ops.render.render(write_still=True, scene=sc.name)


def run(media, size=64, icon=None, do_export=True):
    sc = scene()
    obj = build(sc, media)
    if do_export:
        print("written", export(sc, obj, media))
    out = icon or os.path.join(media, "textures", "Item_FDX_Pemmican.png")
    render_icon(sc, obj, out, size)
    print("rendered", out)


if __name__ == "__main__" and "--" in sys.argv:
    argv = sys.argv[sys.argv.index("--") + 1:]
    run(argv[0], int(argv[1]) if len(argv) > 1 else 64)
