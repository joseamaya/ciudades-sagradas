"""Exporta la escena Caral a GLB para el visor web.

Uso:
    blender --background blender/caral/caral_art.blend \
      --python blender/caral/export.py -- \
      --out public/cities/caral/model.glb
"""

import argparse
import os
import sys

import bpy


def parse_args():
    argv = sys.argv
    argv = argv[argv.index("--") + 1 :] if "--" in argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="public/cities/caral/model.glb")
    return parser.parse_args(argv)


EXCLUDED_COLLECTIONS = {
    "COL-Caral_GameExport",
    "COL-Caral_ScenarioCityExport",
    "COL-Caral_Gameplay",
    "COL-Caral_Cameras",
    "COL-Caral_Lights",
}


def is_excluded(obj):
    return any(collection.name in EXCLUDED_COLLECTIONS for collection in obj.users_collection)


def main():
    args = parse_args()
    out = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)

    bpy.ops.object.select_all(action="DESELECT")
    selected = [
        obj
        for obj in bpy.data.objects
        if obj.type == "MESH" and not is_excluded(obj)
    ]
    for obj in selected:
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
        export_image_format="AUTO",
        export_normals=True,
        export_texcoords=True,
    )

    meshes = len(selected)
    triangles = 0
    for obj in selected:
        mesh = obj.data
        mesh.calc_loop_triangles()
        triangles += len(mesh.loop_triangles)

    size = os.path.getsize(out)
    print(f"EXPORT_OK {out}")
    print(f"OBJECTS {len(bpy.data.objects)} MESHES {meshes} TRIS {triangles} BYTES {size}")


if __name__ == "__main__":
    main()
