"""Primer pase de terreno para el remaster de Caral.

Uso:
    blender --background blender/caral/caral_art.blend \
      --python scripts/remaster_caral_terrain.py -- \
      --out blender/caral/caral_remaster.blend \
      --render /tmp/caral_terrain.png

No modifica caral_art.blend: guarda una copia de trabajo.
"""

import argparse
import math
import os
import sys

import bpy


def parse_args():
    argv = sys.argv
    argv = argv[argv.index("--") + 1 :] if "--" in argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="blender/caral/caral_remaster.blend")
    parser.add_argument("--render", default="")
    return parser.parse_args(argv)


def clear_remaster_modifiers(obj):
    for modifier in list(obj.modifiers):
        if modifier.name.startswith(("SUB-Remaster", "DSP-Remaster")):
            obj.modifiers.remove(modifier)
    group = obj.vertex_groups.get("VG-RemasterMask")
    if group:
        obj.vertex_groups.remove(group)


def radial_mask(obj, inner, outer):
    name = "VG-RemasterMask"
    group = obj.vertex_groups.get(name) or obj.vertex_groups.new(name=name)
    for vertex in obj.data.vertices:
        point = obj.matrix_world @ vertex.co
        distance = math.hypot(point.x, point.y)
        if distance <= inner:
            weight = 0.0
        elif distance >= outer:
            weight = 1.0
        else:
            weight = (distance - inner) / (outer - inner)
        group.add([vertex.index], weight, "REPLACE")
    return name


def noise_texture(name, scale, depth):
    texture = bpy.data.textures.get(name) or bpy.data.textures.new(name, type="CLOUDS")
    texture.noise_scale = scale
    texture.noise_depth = depth
    return texture


def detail(obj, levels, scale, strength, depth=3, mask=None):
    clear_remaster_modifiers(obj)
    subdivision = obj.modifiers.new("SUB-Remaster", "SUBSURF")
    subdivision.subdivision_type = "SIMPLE"
    subdivision.levels = levels
    subdivision.render_levels = levels
    displacement = obj.modifiers.new("DSP-Remaster", "DISPLACE")
    displacement.texture = noise_texture(f"TEX-Remaster-{obj.name}", scale, depth)
    displacement.strength = strength
    displacement.mid_level = 0.5
    displacement.texture_coords = "GLOBAL"
    if mask:
        displacement.vertex_group = mask


def main():
    args = parse_args()
    base = bpy.data.objects.get("GEO-Caral_Terrain_Base")
    apron = bpy.data.objects.get("GEO-Caral_SiteApron")
    hills = [obj for obj in bpy.data.objects if obj.name.startswith("GEO-Caral_Hill_")]

    if base:
        clear_remaster_modifiers(base)
    if apron:
        clear_remaster_modifiers(apron)
    for hill in hills:
        detail(hill, 3, 38, 7.0, 3)

    bpy.context.preferences.filepaths.save_version = 0
    out = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=out)
    print(f"SAVED {out}")

    if args.render:
        scene = bpy.context.scene
        scene.camera = bpy.data.objects.get("CAM-Caral_RTS_Hero")
        scene.render.resolution_x = 1600
        scene.render.resolution_y = 900
        scene.render.resolution_percentage = 100
        scene.render.image_settings.file_format = "PNG"
        scene.render.filepath = os.path.abspath(args.render)
        bpy.ops.render.render(write_still=True)
        print(f"RENDERED {scene.render.filepath}")


if __name__ == "__main__":
    main()
