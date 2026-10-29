"""Prepara LOD0/LOD1 de Aypate desde el high-poly v0.4.

Uso:
  blender --background blender/aypate/aypate_highpoly_v0.4.blend \
    --python scripts/build_aypate_lod.py -- --lod 0 \
    --out-blend blender/aypate/aypate_lod0.blend
"""

import argparse
import os
import sys

import bpy

LAYERS = ("City", "Terrain", "Props", "Reference")
DECIMATE = {"City": 0.25, "Terrain": 0.28, "Props": 0.30, "Reference": 1.0}


def parse_args():
    argv = sys.argv
    argv = argv[argv.index("--") + 1 :] if "--" in argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--lod", choices=("0", "1"), required=True)
    parser.add_argument("--out-blend", required=True)
    return parser.parse_args(argv)


def activate(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def triangles(obj):
    obj.data.calc_loop_triangles()
    return len(obj.data.loop_triangles)


def join_layer(name, objects, lod):
    bpy.ops.object.select_all(action="DESELECT")
    for obj in objects:
        obj.hide_set(False)
        obj.hide_render = False
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.object.duplicate(linked=False)
    duplicates = [obj for obj in bpy.context.selected_objects if obj.type == "MESH"]
    bpy.ops.object.select_all(action="DESELECT")
    for obj in duplicates:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = duplicates[0]
    bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")
    bpy.ops.object.convert(target="MESH")
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.join()
    joined = bpy.context.object
    joined.name = f"GEO-Aypate_LOD{lod}_{name}"
    joined.data.name = f"MESH-Aypate_LOD{lod}_{name}"
    joined["layer"] = name.lower()
    joined["lod"] = int(lod)
    joined["units"] = "meters"
    joined["source"] = "aypate_highpoly_v0.4"
    joined["evidence"] = "documentado + inferido"
    if lod == "1":
        ratio = DECIMATE[name]
        if ratio < 1.0:
            mod = joined.modifiers.new("LODDecimate", "DECIMATE")
            mod.decimate_type = "COLLAPSE"
            mod.ratio = ratio
            activate(joined)
            bpy.ops.object.modifier_apply(modifier=mod.name)
    print(f"AYPATE_LOD{lod}_{name.upper()} tris={triangles(joined)}")
    return joined


def main():
    args = parse_args()
    out = os.path.abspath(args.out_blend)
    lod = args.lod
    target = bpy.data.collections.new(f"COL-Aypate_LOD{lod}_Export")
    bpy.context.scene.collection.children.link(target)
    groups = {name: [] for name in LAYERS}
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        if lod == "1" and obj.get("lod1_exclude"):
            continue
        layer = obj.get("layer", "city").title()
        if layer not in groups:
            layer = "Props"
        groups[layer].append(obj)
    for name in LAYERS:
        if not groups[name]:
            continue
        joined = join_layer(name, groups[name], lod)
        for col in list(joined.users_collection):
            col.objects.unlink(joined)
        target.objects.link(joined)
    for obj in list(bpy.data.objects):
        if obj.type == "MESH" and not any(col == target for col in obj.users_collection):
            bpy.data.objects.remove(obj, do_unlink=True)
    bpy.ops.wm.save_as_mainfile(filepath=out)
    total = sum(triangles(obj) for obj in target.objects if obj.type == "MESH")
    print(f"AYPATE_LOD{lod}_SAVED {out} meshes={len(target.objects)} tris={total}")


if __name__ == "__main__":
    main()
