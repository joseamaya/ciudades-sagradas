"""Ensambla el LOD0 de Caral v2: high-poly por región + infraestructura fusionada.

Uso:
  blender --background blender/caral/caral_remaster_v2.blend \
    --python scripts/assemble_caral_lod0.py -- \
    --out-blend blender/caral/caral_lod0.blend

No modifica caral_remaster_v2.blend ni public/.
"""

import argparse
import os
import sys

import bpy

REGIONS = {
    "Mayor": ("COL-Caral_HighPoly_Mayor", "mayor", "UNESCO 1269 p. 351"),
    "PlazaMayor": ("COL-Caral_HighPoly_PlazaMayor", "plaza-mayor", "UNESCO 1269 p. 351"),
    "Anfiteatro": ("COL-Caral_HighPoly_Anfiteatro", "anfiteatro", "UNESCO 1269 p. 358"),
    "AltarCircular": ("COL-Caral_HighPoly_AltarCircular", "altar-circular", "UNESCO 1269 p. 359"),
}
INFRA_GROUPS = {
    "Terrain": ("COL-Caral_Terrain", "terrain"),
    "LowerHalf": ("COL-Caral_LowerHalf", "city"),
    "UpperHalf": ("COL-Caral_UpperHalf", "city"),
    "Residential": ("COL-Caral_Residential", "city"),
    "Props": ("COL-Caral_Props", "props"),
    "Reference": ("COL-Caral_Reference", "reference"),
}
HERO_NAME = "COL-Caral_LOD0_Hero"
INFRA_NAME = "COL-Caral_LOD0_Infra"


def parse_args():
    argv = sys.argv
    argv = argv[argv.index("--") + 1 :] if "--" in argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-blend", required=True)
    return parser.parse_args(argv)


def tris(obj):
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
        obj.select_set(True)
    if objects:
        bpy.context.view_layer.objects.active = objects[0]


def remove_collection(name):
    collection = bpy.data.collections.get(name)
    if not collection:
        return
    for obj in list(collection.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    bpy.data.collections.remove(collection)


def normalize_uvs(obj):
    if not obj.data.uv_layers:
        return
    for index, layer in enumerate(obj.data.uv_layers):
        layer.name = "UVMap" if index == 0 else f"UVMap_{index}"
    obj.data.uv_layers.active_index = 0


def duplicate_objects(objects):
    select_only(objects)
    bpy.ops.object.duplicate(linked=False)
    duplicates = [obj for obj in bpy.context.selected_objects if obj.type == "MESH"]
    if not duplicates:
        return []
    select_only(duplicates)
    bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")
    bpy.ops.object.convert(target="MESH")
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    for obj in duplicates:
        normalize_uvs(obj)
    return duplicates


def move_to_collection(objects, collection):
    for obj in objects:
        for owner in list(obj.users_collection):
            owner.objects.unlink(obj)
        collection.objects.link(obj)


def merge_region(collection, name, sublayer, source):
    if not collection:
        print(f"LOD0_REGION_SKIP {name} missing")
        return None
    collection.hide_viewport = False
    collection.hide_render = False
    sources = [obj for obj in collection.objects if obj.type == "MESH"]
    duplicates = duplicate_objects(sources)
    if not duplicates:
        print(f"LOD0_REGION_SKIP {name} empty")
        return None
    move_to_collection(duplicates, HERO)
    select_only(duplicates)
    bpy.ops.object.join()
    joined = bpy.context.view_layer.objects.active
    joined.name = f"GEO-Caral_LOD0_{name}"
    joined.data.name = f"MESH-Caral_LOD0_{name}"
    joined.hide_set(False)
    joined.hide_render = False
    joined["layer"] = "city"
    joined["sublayer"] = sublayer
    joined["lod"] = 0
    joined["units"] = "meters"
    joined["source"] = source
    joined["evidence"] = "inferido"
    collection.hide_viewport = True
    collection.hide_render = True
    materials = sorted({slot.material.name for slot in joined.material_slots if slot.material})
    print(f"LOD0_REGION {name} src={len(sources)} tris={tris(joined)} materials={len(materials)}")
    return joined


def merge_infra(collection, name, layer):
    if not collection:
        print(f"LOD0_INFRA_SKIP {name} missing")
        return None
    collection.hide_viewport = False
    collection.hide_render = False
    sources = [obj for obj in collection.objects if obj.type == "MESH"]
    duplicates = duplicate_objects(sources)
    if not duplicates:
        print(f"LOD0_INFRA_SKIP {name} empty")
        return None
    move_to_collection(duplicates, INFRA_COLLECTION)
    select_only(duplicates)
    bpy.ops.object.join()
    joined = bpy.context.view_layer.objects.active
    joined.name = f"GEO-Caral_LOD0_Infra_{name}"
    joined.data.name = f"MESH-Caral_LOD0_Infra_{name}"
    joined.hide_set(False)
    joined.hide_render = False
    joined["layer"] = layer
    joined["sublayer"] = "infra"
    joined["lod"] = 0
    joined["units"] = "meters"
    joined["source"] = "caral_remaster_v2"
    joined["evidence"] = "inferido"
    collection.hide_viewport = True
    collection.hide_render = True
    materials = sorted({slot.material.name for slot in joined.material_slots if slot.material})
    print(f"LOD0_INFRA {name} src={len(sources)} tris={tris(joined)} materials={len(materials)}")
    return joined


def main():
    args = parse_args()
    out_blend = os.path.abspath(args.out_blend)
    remove_collection(HERO_NAME)
    remove_collection(INFRA_NAME)
    global HERO, INFRA_COLLECTION
    HERO = bpy.data.collections.new(HERO_NAME)
    INFRA_COLLECTION = bpy.data.collections.new(INFRA_NAME)
    bpy.context.scene.collection.children.link(HERO)
    bpy.context.scene.collection.children.link(INFRA_COLLECTION)
    HERO.hide_viewport = False
    HERO.hide_render = False
    INFRA_COLLECTION.hide_viewport = False
    INFRA_COLLECTION.hide_render = False

    for name, (collection_name, sublayer, source) in REGIONS.items():
        merge_region(bpy.data.collections.get(collection_name), name, sublayer, source)
    for name, (collection_name, layer) in INFRA_GROUPS.items():
        merge_infra(bpy.data.collections.get(collection_name), name, layer)

    hero_tris = sum(tris(obj) for obj in HERO.objects if obj.type == "MESH")
    infra_tris = sum(tris(obj) for obj in INFRA_COLLECTION.objects if obj.type == "MESH")
    print(f"LOD0_TOTAL hero={len(HERO.objects)} infra={len(INFRA_COLLECTION.objects)} tris={hero_tris + infra_tris}")
    bpy.ops.wm.save_as_mainfile(filepath=out_blend)


if __name__ == "__main__":
    main()
