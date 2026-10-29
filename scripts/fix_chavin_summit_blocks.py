"""Integra los remates de cima de Chavín en la arquitectura de piedra.

Uso:
  blender --background blender/chavin/chavin_highpoly_v0.4.blend \
    --python scripts/fix_chavin_summit_blocks.py -- \
    --out-blend blender/chavin/chavin_highpoly_v0.5.blend

Sustituye el plaster blanco por piedra, hunde los remates 0,02 m en su
terraza y añade una basa perimetral. No inventa techos ni recintos.
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


def make_plinth(name, base_obj, height, base_z, stone):
    x0, x1, y0, y1, _, _ = bbox(base_obj)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy, base_z + height / 2 - 0.02))
    plinth = bpy.context.object
    plinth.name = name
    plinth.data.name = f"MESH-{name}"
    plinth.dimensions = ((x1 - x0) + 0.40, (y1 - y0) + 0.40, height)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    plinth.data.materials.append(stone)
    collection = base_obj.users_collection[0]
    for owner in list(plinth.users_collection):
        owner.objects.unlink(plinth)
    collection.objects.link(plinth)
    return plinth


def main():
    args = parse_args()
    out = os.path.abspath(args.out_blend)
    stone = bpy.data.materials.get("MAT-Chavin_Stone_Tiled")
    if stone is None:
        raise RuntimeError("Falta MAT-Chavin_Stone_Tiled")
    for name, plinth_name, height in (
        ("GEO-Chavin_EdificioA_Summit", "GEO-Chavin_EdificioA_Summit_Plinth", 0.35),
        ("GEO-Chavin_EdificioB_Summit", "GEO-Chavin_EdificioB_Summit_Plinth", 0.30),
    ):
        obj = bpy.data.objects.get(name)
        if obj is None:
            raise RuntimeError(f"Falta {name}")
        _, _, _, _, base_z, _ = bbox(obj)
        make_plinth(plinth_name, obj, height, base_z, stone)
        obj.data.materials.clear()
        obj.data.materials.append(stone)
        obj.location.z += height - 0.02
        print("CHAVIN_SUMMIT_FIXED", name, round(base_z, 2), round(obj.location.z, 2))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=out)
    print("CHAVIN_SUMMIT_OK", out)


if __name__ == "__main__":
    main()
