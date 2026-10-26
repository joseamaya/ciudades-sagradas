"""Exporta un LOD de Caral desde su blend ensamblado.

Uso:
  blender --background blender/caral/caral_lod0.blend \
    --python scripts/export_caral_lod.py -- --lod 0 --out public/cities/caral/model_lod0.glb

No modifica la escena ni public/ salvo el archivo de salida indicado.
"""

import argparse
import os
import sys

import bpy

PREFIXES = {"0": "COL-Caral_LOD0_", "1": "COL-Caral_LOD1_"}


def parse_args():
    argv = sys.argv
    argv = argv[argv.index("--") + 1 :] if "--" in argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--lod", choices=sorted(PREFIXES), required=True)
    parser.add_argument("--out", required=True)
    return parser.parse_args(argv)


def included(obj, prefix):
    return obj.type == "MESH" and any(c.name.startswith(prefix) for c in obj.users_collection)


def main():
    args = parse_args()
    prefix = PREFIXES[args.lod]
    out = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    bpy.ops.object.select_all(action="DESELECT")
    selected = [obj for obj in bpy.data.objects if included(obj, prefix)]
    for obj in selected:
        obj.hide_set(False)
        obj.select_set(True)
    if selected:
        bpy.context.view_layer.objects.active = selected[0]

    bpy.ops.export_scene.gltf(
        use_selection=True,
        filepath=out,
        export_format="GLB",
        export_apply=True,
        export_yup=True,
        export_cameras=False,
        export_lights=False,
        export_animations=False,
        export_materials="EXPORT",
        export_image_format="WEBP",
        export_image_quality=80,
        export_normals=True,
        export_texcoords=True,
        export_extras=True,
    )
    depsgraph = bpy.context.evaluated_depsgraph_get()
    triangles = 0
    for obj in selected:
        evaluated = obj.evaluated_get(depsgraph)
        mesh = evaluated.to_mesh()
        mesh.calc_loop_triangles()
        triangles += len(mesh.loop_triangles)
        evaluated.to_mesh_clear()
    print(
        f"CARAL_LOD{args.lod}_EXPORT_OK {out} MESHES {len(selected)} "
        f"TRIS {triangles} BYTES {os.path.getsize(out)}"
    )


if __name__ == "__main__":
    main()
