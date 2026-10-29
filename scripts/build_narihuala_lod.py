"""Prepara LOD0/LOD1 de Narihualá desde el high-poly v0.2.

Uso:
  blender --background blender/narihuala/narihuala_highpoly_v0.2.blend \
    --python scripts/build_narihuala_lod.py -- --lod 0 \
    --out-blend blender/narihuala/narihuala_lod0.blend
"""

import argparse
import os
import sys

import bpy

LAYERS = ("city", "terrain", "props", "reference", "later")
DECIMATE = {"city": 0.26, "terrain": 0.26, "props": 0.26, "reference": 1.0, "later": 0.5}


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
    joined.name = f"GEO-Narihuala_LOD{lod}_{name.title()}"
    joined.data.name = f"MESH-Narihuala_LOD{lod}_{name.title()}"
    joined["layer"] = name
    joined["lod"] = int(lod)
    joined["units"] = "meters"
    joined["source"] = "narihuala_highpoly_v0.2"
    joined["evidence"] = "SIGRID 2018 + inferencia documentada"
    if lod == "1":
        ratio = DECIMATE[name]
        if ratio < 1.0:
            mod = joined.modifiers.new("LODDecimate", "DECIMATE")
            mod.decimate_type = "COLLAPSE"
            mod.ratio = ratio
            activate(joined)
            bpy.ops.object.modifier_apply(modifier=mod.name)
    print(f"NARIHUALA_LOD{lod}_{name.upper()} tris={triangles(joined)}")
    return joined


def main():
    args = parse_args()
    out = os.path.abspath(args.out_blend)
    lod = args.lod
    target = bpy.data.collections.new(f"COL-Narihuala_LOD{lod}_Export")
    bpy.context.scene.collection.children.link(target)
    for col in bpy.data.collections:
        col.hide_viewport = False
        col.hide_render = False
    groups = {name: [] for name in LAYERS}
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        if lod == "1" and obj.get("lod1_exclude"):
            continue
        layer = obj.get("layer", "city")
        if layer == "later" and lod == "1":
            continue
        if layer not in groups:
            layer = "props"
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
    print(f"NARIHUALA_LOD{lod}_SAVED {out} meshes={len(target.objects)} tris={total}")


if __name__ == "__main__":
    main()
