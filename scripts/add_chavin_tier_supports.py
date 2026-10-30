"""Añade apoyos visibles bajo las terrazas superiores de Chavín.

Uso:
  blender --background blender/chavin/chavin_highpoly_v0.5.blend \
    --python scripts/add_chavin_tier_supports.py -- \
    --out-blend blender/chavin/chavin_highpoly_v0.6.blend

A Tier_04 se rellena desde Tier_03 (z 15) hasta su base (z 21).
B Tier_02 recibe muros de apoyo perimetrales desde z 3 hasta z 9, dejando
libre la galería central. No se eliminan terrazas ni remates documentados.
"""

import argparse
import os
import sys

import bpy
from mathutils import Vector


def parse_args():
    argv = sys.argv
    argv = argv[argv.index("--") + 1 :] if "--" in argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-blend", required=True)
    return parser.parse_args(argv)


def bbox(obj):
    points = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    return (
        min(p.x for p in points),
        max(p.x for p in points),
        min(p.y for p in points),
        max(p.y for p in points),
        min(p.z for p in points),
        max(p.z for p in points),
    )


def box(name, center, size, material, source_obj):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=center)
    obj = bpy.context.object
    obj.name = name
    obj.data.name = f"MESH-{name}"
    obj.dimensions = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(material)
    collection = source_obj.users_collection[0]
    for owner in list(obj.users_collection):
        owner.objects.unlink(obj)
    collection.objects.link(obj)
    return obj


def main():
    args = parse_args()
    stone = bpy.data.materials.get("MAT-Chavin_StoneDark_Tiled")
    if stone is None:
        raise RuntimeError("Falta MAT-Chavin_StoneDark_Tiled")

    tier_a = bpy.data.objects["GEO-Chavin_EdificioA_Tier_04"]
    ax0, ax1, ay0, ay1, az0, _ = bbox(tier_a)
    box(
        "GEO-Chavin_EdificioA_Tier_04_Support",
        ((ax0 + ax1) / 2, (ay0 + ay1) / 2, (15.0 + az0) / 2),
        (ax1 - ax0 + 0.8, ay1 - ay0 + 0.8, az0 - 15.0),
        stone,
        tier_a,
    )
    print("CHAVIN_SUPPORT A", round(15.0, 2), round(az0, 2))

    tier_b = bpy.data.objects["GEO-Chavin_EdificioB_Tier_02"]
    bx0, bx1, by0, by1, bz0, _ = bbox(tier_b)
    height = bz0 - 3.0
    thickness = 0.8
    box("GEO-Chavin_EdificioB_Tier_02_Support_N", ((bx0 + bx1) / 2, by0 - 0.4, (3.0 + bz0) / 2), (bx1 - bx0 + 0.8, thickness, height), stone, tier_b)
    box("GEO-Chavin_EdificioB_Tier_02_Support_S", ((bx0 + bx1) / 2, by1 + 0.4, (3.0 + bz0) / 2), (bx1 - bx0 + 0.8, thickness, height), stone, tier_b)
    box("GEO-Chavin_EdificioB_Tier_02_Support_W", (bx0 - 0.4, (by0 + by1) / 2, (3.0 + bz0) / 2), (thickness, by1 - by0 + 0.8, height), stone, tier_b)
    box("GEO-Chavin_EdificioB_Tier_02_Support_E", (bx1 + 0.4, (by0 + by1) / 2, (3.0 + bz0) / 2), (thickness, by1 - by0 + 0.8, height), stone, tier_b)
    print("CHAVIN_SUPPORT B", round(3.0, 2), round(bz0, 2))

    out = os.path.abspath(args.out_blend)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=out)
    print("CHAVIN_TIER_SUPPORTS_OK", out)


if __name__ == "__main__":
    main()
