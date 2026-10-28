"""Prepara los LOD de Chavín desde la fuente high-poly v0.1.

Uso:
  blender --background blender/chavin/chavin_highpoly_v0.1.blend \
    --python scripts/build_chavin_lod.py -- --lod 0 \
    --out-blend blender/chavin/chavin_lod0.blend

El LOD1 elimina los detalles marcados con lod1_exclude y se exporta después con
texturas 1K. No modifica la escena fuente.
"""

import argparse
import os
import sys

import bpy

CITY_COLLECTIONS = {
    "COL-Chavin_Architecture",
    "COL-Chavin_Plazas",
    "COL-Chavin_Portada",
}
TERRAIN_COLLECTIONS = {"COL-Chavin_Terrain"}
REFERENCE_COLLECTIONS = {"COL-Chavin_Reference"}
CITY_SPECIAL = {
    "GEO-Chavin_PlazaCircular_Altar",
    "GEO-Chavin_Gallery_Niche",
}
PROPS_SPECIAL = {
    "GEO-Chavin_Lanzon",
}
TERRAIN_SPECIAL = {
    "GEO-Chavin_Path_Ramp_N",
    "GEO-Chavin_Path_Terrace_N",
}
LOD1_EXCLUDE = ("_Eye", "_Fang", "_Serpent")
# Los detalles del pase high-poly se omiten en móvil mediante su propiedad
# lod1_exclude. La base de la Portada y el Lanzón permanecen.


MATERIAL_FALLBACK = {
    "MAT-Chavin_Earth": ((0.34, 0.27, 0.18, 1.0), 0.96),
    "MAT-Chavin_Path": ((0.47, 0.39, 0.29, 1.0), 0.92),
    "MAT-Chavin_Plaster": ((0.62, 0.57, 0.48, 1.0), 0.78),
    "MAT-Chavin_Water": ((0.06, 0.18, 0.24, 1.0), 0.30),
    "MAT-Chavin_Vegetation": ((0.14, 0.23, 0.10, 1.0), 0.88),
    "MAT-Chavin_Lanzon": ((0.50, 0.46, 0.38, 1.0), 0.80),
    "MAT-Chavin_GalleryDark": ((0.008, 0.010, 0.008, 1.0), 0.92),
    "MAT-Chavin_Reference": ((0.40, 0.24, 0.16, 1.0), 0.82),
}


def parse_args():
    argv = sys.argv
    argv = argv[argv.index("--") + 1 :] if "--" in argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--lod", choices=("0", "1"), required=True)
    parser.add_argument("--out-blend", required=True)
    return parser.parse_args(argv)


def layer_for(obj):
    if obj.name in TERRAIN_SPECIAL or any(c.name in TERRAIN_COLLECTIONS for c in obj.users_collection):
        return "terrain"
    if obj.name.startswith("GEO-Chavin_HumanScale") or obj.name.startswith("GEO-Chavin_HumanScale_Head"):
        return "reference"
    if any(c.name in REFERENCE_COLLECTIONS for c in obj.users_collection):
        return "reference"
    if obj.name in PROPS_SPECIAL or obj.name.startswith("GEO-Chavin_Shrub"):
        return "props"
    if obj.name in CITY_SPECIAL or any(c.name in CITY_COLLECTIONS for c in obj.users_collection):
        return "city"
    return "props"


def apply_material_fallbacks():
    for name, (color, roughness) in MATERIAL_FALLBACK.items():
        material = bpy.data.materials.get(name)
        if material is None or not material.use_nodes:
            continue
        bsdf = next((node for node in material.node_tree.nodes if node.type == "BSDF_PRINCIPLED"), None)
        if bsdf is None:
            continue
        base = bsdf.inputs["Base Color"]
        for link in list(base.links):
            material.node_tree.links.remove(link)
        base.default_value = color
        bsdf.inputs["Roughness"].default_value = roughness
        material.diffuse_color = color
        print(f"MATERIAL_FALLBACK {name} {color[:3]} r={roughness}")


def apply_earth_texture():
    root = bpy.path.abspath("//../textures/chavin/")
    earth = bpy.data.materials.get("MAT-Chavin_Earth")
    if earth is None or not earth.use_nodes:
        return
    paths = {
        "diffuse": root + "chavin_terrain_v1_diffuse.jpg",
        "roughness": root + "chavin_terrain_v1_roughness.jpg",
        "normal": root + "chavin_terrain_v1_normal.png",
    }
    images = {}
    for key, path in paths.items():
        image = bpy.data.images.get("chavin_terrain_v1_" + key)
        if image is None:
            image = bpy.data.images.load(path, check_existing=True)
            image.name = "chavin_terrain_v1_" + key
        if key != "diffuse":
            image.colorspace_settings.name = "Non-Color"
        if image.packed_file is None:
            image.pack()
        images[key] = image
    nodes = earth.node_tree.nodes
    links = earth.node_tree.links
    bsdf = next((node for node in nodes if node.type == "BSDF_PRINCIPLED"), None)
    if bsdf is None:
        return
    for socket_name in ("Base Color", "Roughness", "Normal"):
        for link in list(bsdf.inputs[socket_name].links):
            links.remove(link)
    diffuse = nodes.new("ShaderNodeTexImage")
    diffuse.name = "TerrainDiffuse"
    diffuse.image = images["diffuse"]
    diffuse.location = (-620, 240)
    roughness = nodes.new("ShaderNodeTexImage")
    roughness.name = "TerrainRoughness"
    roughness.image = images["roughness"]
    roughness.location = (-620, 0)
    normal = nodes.new("ShaderNodeTexImage")
    normal.name = "TerrainNormal"
    normal.image = images["normal"]
    normal.location = (-620, -240)
    normal_map = nodes.new("ShaderNodeNormalMap")
    normal_map.name = "TerrainNormalMap"
    normal_map.location = (-300, -240)
    normal_map.inputs["Strength"].default_value = 0.8
    links.new(diffuse.outputs["Color"], bsdf.inputs["Base Color"])
    links.new(roughness.outputs["Color"], bsdf.inputs["Roughness"])
    links.new(normal.outputs["Color"], normal_map.inputs["Color"])
    links.new(normal_map.outputs["Normal"], bsdf.inputs["Normal"])
    earth["chavin:source"] = "scripts/make_chavin_terrain_materials.py"


def scale_earth_uvs(obj, scale):
    mesh = obj.data
    if not mesh.uv_layers:
        return
    index = next((i for i, material in enumerate(mesh.materials) if material and material.name == "MAT-Chavin_Earth"), None)
    if index is None:
        return
    uv_data = mesh.uv_layers.active.data
    for polygon in mesh.polygons:
        if polygon.material_index != index:
            continue
        for loop_index in polygon.loop_indices:
            uv = uv_data[loop_index].uv
            uv.x *= scale
            uv.y *= scale


def triangle_count(obj):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh()
    mesh.calc_loop_triangles()
    count = len(mesh.loop_triangles)
    evaluated.to_mesh_clear()
    return count


def select_only(objects):
    bpy.ops.object.select_all(action="DESELECT")
    for obj in objects:
        obj.hide_set(False)
        obj.hide_render = False
        obj.select_set(True)
    if objects:
        bpy.context.view_layer.objects.active = objects[0]


def remove_collection(name):
    collection = bpy.data.collections.get(name)
    if collection is None:
        return
    for obj in list(collection.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    bpy.data.collections.remove(collection)


def export_collection(lod):
    name = f"COL-Chavin_LOD{lod}_Export"
    remove_collection(name)
    collection = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(collection)
    return collection


def merge_layer(objects, layer, collection, lod):
    select_only(objects)
    bpy.ops.object.duplicate(linked=False)
    duplicates = [obj for obj in bpy.context.selected_objects if obj.type == "MESH"]
    select_only(duplicates)
    bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")
    bpy.ops.object.convert(target="MESH")
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    for obj in list(bpy.context.selected_objects):
        if obj.type == "MESH":
            for owner in list(obj.users_collection):
                owner.objects.unlink(obj)
            collection.objects.link(obj)
    select_only(duplicates)
    bpy.ops.object.join()
    joined = bpy.context.view_layer.objects.active
    joined.name = f"GEO-Chavin_LOD{lod}_{layer.title()}"
    joined.data.name = f"MESH-Chavin_LOD{lod}_{layer.title()}"
    joined["layer"] = layer
    joined["lod"] = int(lod)
    joined["units"] = "meters"
    joined["source"] = "chavin_highpoly_v0.1"
    joined["evidence"] = "documentado + inferido"
    joined.hide_set(False)
    joined.hide_render = False
    print(
        f"CHAVIN_LOD{lod}_{layer.upper()} "
        f"tris={triangle_count(joined)} materials={len(joined.material_slots)}"
    )
    return joined


def main():
    args = parse_args()
    lod = args.lod
    out = os.path.abspath(args.out_blend)
    bpy.context.scene.camera = bpy.data.objects.get("CAM-Chavin_Hero")
    apply_material_fallbacks()
    apply_earth_texture()
    for obj in bpy.data.objects:
        if obj.type == "MESH":
            obj["layer"] = layer_for(obj)
            obj["lod"] = int(lod)
            obj["units"] = "meters"
    if lod == "1":
        for obj in list(bpy.data.objects):
            if obj.type != "MESH":
                continue
            if any(token in obj.name for token in LOD1_EXCLUDE) or obj.get("lod1_exclude"):
                bpy.data.objects.remove(obj, do_unlink=True)
    groups = {layer: [] for layer in ("city", "terrain", "props", "reference")}
    for obj in bpy.data.objects:
        if obj.type == "MESH":
            groups[layer_for(obj)].append(obj)
    target = export_collection(lod)
    for layer in ("city", "terrain", "props", "reference"):
        objs = groups[layer]
        if not objs:
            continue
        merged = merge_layer(objs, layer, target, lod)
        if layer == "terrain" and merged is not None:
            scale_earth_uvs(merged, 8.0)
    for obj in list(bpy.data.objects):
        if obj.type == "MESH" and not any(c == target for c in obj.users_collection):
            bpy.data.objects.remove(obj, do_unlink=True)
    bpy.ops.wm.save_as_mainfile(filepath=out)
    total = sum(triangle_count(obj) for obj in target.objects if obj.type == "MESH")
    print(f"CHAVIN_LOD{lod}_SAVED {out} meshes={len(target.objects)} tris={total}")


if __name__ == "__main__":
    main()
