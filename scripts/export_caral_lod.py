"""Exporta un LOD de Caral desde su blend ensamblado.

Uso:
  blender --background blender/caral/caral_lod0.blend \
    --python scripts/export_caral_lod.py -- --lod 0 --out public/cities/caral/model_lod0.glb

  # LOD1 móvil: texturas 1K
  blender --background blender/caral/caral_lod1.blend \
    --python scripts/export_caral_lod.py -- --lod 1 --max-texture-size 1024 \
    --out public/cities/caral/model_lod1.glb

No modifica la escena ni public/ salvo el archivo de salida indicado.
"""

import argparse
import os
import sys

import bpy

PREFIXES = {"0": "COL-Caral_LOD0_", "1": "COL-Caral_LOD1_"}

DOUBLE_SIDED_MATERIALS = {
    "MAT-Caral_Fire",
    "MAT-Caral_Cotton",
    "MAT-Caral_Remaster_Thatch",
    "MAT-Caral_Remaster_Leaves",
    "MAT-Caral_Remaster_Grass",
}


def optimize_materials():
    """Alinea el GLB con el visor: culling en sólidos y agua sin transmisión."""
    for material in bpy.data.materials:
        if material.users == 0:
            continue
        key = material.name.split(".")[0]
        material.use_backface_culling = key not in DOUBLE_SIDED_MATERIALS
        if key == "MAT-Caral_Water" and material.use_nodes:
            for node in material.node_tree.nodes:
                if node.type != "BSDF_PRINCIPLED":
                    continue
                for socket_name in ("Transmission Weight", "Transmission"):
                    if socket_name in node.inputs:
                        node.inputs[socket_name].default_value = 0.0


def limit_textures(max_size):
    """Escala en memoria las texturas por encima de max_size, sin tocar el .blend."""
    if not max_size:
        return
    for image in bpy.data.images:
        if image.users == 0 or image.type not in {"IMAGE"}:
            continue
        width, height = image.size
        if max(width, height) <= max_size:
            continue
        scale = max_size / max(width, height)
        new_width = max(1, round(width * scale))
        new_height = max(1, round(height * scale))
        image.scale(new_width, new_height)
        image.pack()
        print(f"TEXTURE_SCALED {image.name} {width}x{height} -> {new_width}x{new_height}")


def parse_args():
    argv = sys.argv
    argv = argv[argv.index("--") + 1 :] if "--" in argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--lod", choices=sorted(PREFIXES), required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--no-draco", dest="draco", action="store_false", default=True)
    parser.add_argument("--keep-materials", action="store_true")
    parser.add_argument("--max-texture-size", type=int, default=0)
    return parser.parse_args(argv)


def included(obj, prefix):
    return obj.type == "MESH" and any(c.name.startswith(prefix) for c in obj.users_collection)


def main():
    args = parse_args()
    prefix = PREFIXES[args.lod]
    out = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if not args.keep_materials:
        optimize_materials()
    if args.lod == "1" and not args.max_texture_size:
        print("WARN LOD1 sin --max-texture-size; se exportarán las texturas originales")
    limit_textures(args.max_texture_size)
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
        export_draco_mesh_compression_enable=args.draco,
        export_draco_mesh_compression_level=6,
        export_draco_position_quantization=14,
        export_draco_normal_quantization=10,
        export_draco_texcoord_quantization=12,
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
        f"TRIS {triangles} BYTES {os.path.getsize(out)} DRACO {args.draco} "
        f"MAX_TEX {args.max_texture_size or 'orig'}"
    )


if __name__ == "__main__":
    main()
