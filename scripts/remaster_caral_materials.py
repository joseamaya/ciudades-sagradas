"""Pase de materiales procedurales para Caral.

Uso:
    blender --background blender/caral/caral_remaster.blend \
      --python scripts/remaster_caral_materials.py -- \
      --out blender/caral/caral_remaster.blend \
      --hero /tmp/caral_materials_hero.png \
      --close /tmp/caral_materials_close.png \
      --scope all
"""

import argparse
import os
import sys

import bpy


def parse_args():
    argv = sys.argv
    argv = argv[argv.index("--") + 1 :] if "--" in argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="blender/caral/caral_remaster.blend")
    parser.add_argument("--hero", default="")
    parser.add_argument("--close", default="")
    parser.add_argument("--scope", choices=("mayor", "all"), default="all")
    return parser.parse_args(argv)


def image_node(nodes, path, non_color=False):
    image = bpy.data.images.load(os.path.abspath(path), check_existing=True)
    image.filepath = bpy.path.relpath(os.path.abspath(path))
    image.reload()
    image.colorspace_settings.name = "Non-Color" if non_color else "sRGB"
    node = nodes.new("ShaderNodeTexImage")
    node.image = image
    node.interpolation = "Linear"
    node.extension = "REPEAT"
    return node


def make_material(name, diffuse, normal, roughness, normal_strength=1.0):
    material = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    material.use_nodes = True
    material.metallic = 0.0
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    nodes.clear()

    output = nodes.new("ShaderNodeOutputMaterial")
    output.location = (520, 0)
    principled = nodes.new("ShaderNodeBsdfPrincipled")
    principled.location = (240, 0)
    principled.inputs["Metallic"].default_value = 0.0

    base = image_node(nodes, diffuse)
    base.location = (-420, 180)
    links.new(base.outputs["Color"], principled.inputs["Base Color"])

    rough = image_node(nodes, roughness, non_color=True)
    rough.location = (-420, -40)
    links.new(rough.outputs["Color"], principled.inputs["Roughness"])

    normal_tex = image_node(nodes, normal, non_color=True)
    normal_tex.location = (-420, -260)
    normal_map = nodes.new("ShaderNodeNormalMap")
    normal_map.location = (-120, -260)
    normal_map.inputs["Strength"].default_value = normal_strength
    links.new(normal_tex.outputs["Color"], normal_map.inputs["Color"])
    links.new(normal_map.outputs["Normal"], principled.inputs["Normal"])
    links.new(principled.outputs["BSDF"], output.inputs["Surface"])
    return material


def main():
    args = parse_args()
    root = "blender/textures/generated/remaster"
    white = make_material(
        "MAT-Caral_Remaster_Plaster_White",
        f"{root}/plaster_white_diffuse.jpg",
        f"{root}/plaster_white_normal.png",
        f"{root}/plaster_white_roughness.jpg",
        1.3,
    )
    yellow = make_material(
        "MAT-Caral_Remaster_Plaster_Yellow",
        f"{root}/plaster_yellow_diffuse.jpg",
        f"{root}/plaster_white_normal.png",
        f"{root}/plaster_white_roughness.jpg",
        1.3,
    )
    red = make_material(
        "MAT-Caral_Remaster_Plaster_Red",
        f"{root}/plaster_red_diffuse.jpg",
        f"{root}/plaster_white_normal.png",
        f"{root}/plaster_white_roughness.jpg",
        1.3,
    )
    cut = make_material(
        "MAT-Caral_Remaster_Stone_Cut",
        f"{root}/stone_cut_diffuse.jpg",
        f"{root}/stone_cut_normal.png",
        f"{root}/stone_cut_roughness.jpg",
        1.4,
    )
    field = make_material(
        "MAT-Caral_Remaster_Stone_Field",
        f"{root}/stone_field_diffuse.jpg",
        f"{root}/stone_field_normal.png",
        f"{root}/stone_field_roughness.jpg",
        1.2,
    )
    sand = make_material(
        "MAT-Caral_Remaster_Sand",
        f"{root}/ground_sand_diffuse.jpg",
        f"{root}/ground_normal.png",
        f"{root}/ground_roughness.jpg",
        0.9,
    )
    earth = make_material(
        "MAT-Caral_Remaster_Earth",
        f"{root}/ground_earth_diffuse.jpg",
        f"{root}/ground_normal.png",
        f"{root}/ground_roughness.jpg",
        0.9,
    )
    terrain = make_material(
        "MAT-Caral_Remaster_Terrain",
        f"{root}/terrain_sand_diffuse.jpg",
        f"{root}/ground_normal.png",
        f"{root}/ground_roughness.jpg",
        0.9,
    )
    mapping = {
        "MAT-Caral_Plaster_White": white,
        "MAT-Caral_Plaster_Yellow": yellow,
        "MAT-Caral_Plaster_Red": red,
        "MAT-Caral_Stone_Cut": cut,
        "MAT-Caral_Stone_Field": field,
        "MAT-Caral_Sand": sand,
        "MAT-Sand_Desert": sand,
        "MAT-Caral_Dirt": earth,
        "MAT-Caral_Terrace": earth,
        "MAT-Caral_Path": sand,
    }

    changed = 0
    prefix = "GEO-Caral_PyramideMayor_" if args.scope == "mayor" else "GEO-Caral_"
    for obj in bpy.data.objects:
        if obj.type != "MESH" or not obj.name.startswith(prefix):
            continue
        for slot in obj.material_slots:
            if slot.material and slot.material.name in mapping:
                slot.material = mapping[slot.material.name]
                changed += 1

    if args.scope == "all":
        terrain_uv = {
            "GEO-Caral_SiteApron": 0.05,
            "GEO-Caral_Terrain_Base": 0.02,
            "GEO-Caral_Terrain_Shore": 0.02,
            "GEO-Caral_Terrain_DryRavine": 0.05,
        }
        for obj in bpy.data.objects:
            if obj.type != "MESH":
                continue
            if obj.name in terrain_uv:
                for slot in obj.material_slots:
                    if slot.material and slot.material.name == "MAT-Caral_Remaster_Sand":
                        slot.material = terrain
                        changed += 1
                if not obj.get("caral_terrain_uv_scaled"):
                    uv = obj.data.uv_layers.active
                    if uv:
                        factor = terrain_uv[obj.name]
                        for datum in uv.data:
                            datum.uv *= factor
                        obj["caral_terrain_uv_scaled"] = True

    bpy.context.preferences.filepaths.save_version = 0
    out = os.path.abspath(args.out)
    bpy.ops.wm.save_as_mainfile(filepath=out)
    print(f"SAVED {out} SLOTS_CHANGED {changed}")

    scene = bpy.context.scene
    scene.render.resolution_x = 1600
    scene.render.resolution_y = 900
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    for camera_name, output in (
        ("CAM-Caral_RTS_Hero", args.hero),
        ("CAM-Caral_MayorClose", args.close),
    ):
        if not output:
            continue
        scene.camera = bpy.data.objects.get(camera_name)
        scene.render.filepath = os.path.abspath(output)
        bpy.ops.render.render(write_still=True)
        print(f"RENDERED {camera_name} {scene.render.filepath}")


if __name__ == "__main__":
    main()
