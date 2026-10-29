"""Exporta un LOD de Narihualá con WebP 80, Draco y capas en extras.

Uso:
  blender --background blender/narihuala/narihuala_lod0.blend \
    --python scripts/export_narihuala_lod.py -- --out public/cities/narihuala/model_lod0.glb

  blender --background blender/narihuala/narihuala_lod1.blend \
    --python scripts/export_narihuala_lod.py -- --out public/cities/narihuala/model_lod1.glb \
    --max-texture-size 1024
"""

import argparse
import os
import sys

import bpy


def parse_args():
    argv = sys.argv
    argv = argv[argv.index("--") + 1 :] if "--" in argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    parser.add_argument("--max-texture-size", type=int, default=0)
    return parser.parse_args(argv)


def limit_textures(max_size):
    if not max_size:
        return
    for image in bpy.data.images:
        if image.users == 0 or image.type not in {"IMAGE"}:
            continue
        width, height = image.size
        if max(width, height) <= max_size:
            continue
        scale = max_size / max(width, height)
        image.scale(max(1, round(width * scale)), max(1, round(height * scale)))
        image.pack()
        print(f"TEXTURE_SCALED {image.name} {width}x{height} -> {image.size[0]}x{image.size[1]}")


def main():
    args = parse_args()
    out = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    limit_textures(args.max_texture_size)
    meshes = [obj for obj in bpy.data.objects if obj.type == "MESH"]
    bpy.ops.object.select_all(action="DESELECT")
    for obj in meshes:
        obj.hide_set(False)
        obj.hide_render = False
        obj.select_set(True)
    if meshes:
        bpy.context.view_layer.objects.active = meshes[0]
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
        export_draco_mesh_compression_enable=True,
        export_draco_mesh_compression_level=6,
        export_draco_position_quantization=14,
        export_draco_normal_quantization=10,
        export_draco_texcoord_quantization=12,
    )
    print(f"NARIHUALA_EXPORT_OK {out} MESHES {len(meshes)} BYTES {os.path.getsize(out)}")
    total = 0
    for obj in meshes:
        obj.data.calc_loop_triangles()
        total += len(obj.data.loop_triangles)
    print(f"NARIHUALA_EXPORT_TRIS {total}")


if __name__ == "__main__":
    main()
