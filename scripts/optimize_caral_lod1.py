"""Fusiona la infraestructura del LOD1 de Caral por grupos para bajar draw calls.

Uso:
  blender --background blender/caral/caral_lod1.blend \
    --python scripts/optimize_caral_lod1.py
"""

import bpy

GROUPS = {
    "Terrain": ("COL-Caral_Terrain", "terrain"),
    "LowerHalf": ("COL-Caral_LowerHalf", "city"),
    "UpperHalf": ("COL-Caral_UpperHalf", "city"),
    "Residential": ("COL-Caral_Residential", "city"),
    "Props": ("COL-Caral_Props", "props"),
    "Reference": ("COL-Caral_Reference", "reference"),
}
INFRA_NAME = "COL-Caral_LOD1_Infra"


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


def remove_existing_infra():
    collection = bpy.data.collections.get(INFRA_NAME)
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


def merge_group(infra, group, collection_name, layer):
    collection = bpy.data.collections.get(collection_name)
    if not collection:
        print(f"LOD1_INFRA_SKIP {group} missing {collection_name}")
        return
    collection.hide_viewport = False
    collection.hide_render = False
    sources = [obj for obj in collection.objects if obj.type == "MESH"]
    if not sources:
        print(f"LOD1_INFRA_SKIP {group} empty")
        return

    select_only(sources)
    bpy.ops.object.duplicate(linked=False)
    duplicates = [obj for obj in bpy.context.selected_objects if obj.type == "MESH"]
    if not duplicates:
        print(f"LOD1_INFRA_SKIP {group} no duplicates")
        return

    select_only(duplicates)
    bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")
    bpy.ops.object.convert(target="MESH")
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    for obj in duplicates:
        normalize_uvs(obj)
        for owner in list(obj.users_collection):
            owner.objects.unlink(obj)
        infra.objects.link(obj)

    select_only(duplicates)
    bpy.ops.object.join()
    joined = bpy.context.view_layer.objects.active
    joined.name = f"GEO-Caral_LOD1_Infra_{group}"
    joined.data.name = f"MESH-Caral_LOD1_Infra_{group}"
    joined.hide_set(False)
    joined.hide_render = False
    joined["layer"] = layer
    joined["sublayer"] = "infra"
    joined["lod"] = 1
    joined["units"] = "meters"
    joined["source"] = "caral_remaster_v2"
    joined["evidence"] = "inferido"

    collection.hide_viewport = True
    collection.hide_render = True
    materials = sorted({slot.material.name for slot in joined.material_slots if slot.material})
    print(
        f"LOD1_INFRA {group} src={len(sources)} tris={tris(joined)} "
        f"materials={len(materials)} {materials}"
    )


def main():
    remove_existing_infra()
    infra = bpy.data.collections.new(INFRA_NAME)
    bpy.context.scene.collection.children.link(infra)
    infra.hide_viewport = False
    infra.hide_render = False
    for group, (collection, layer) in GROUPS.items():
        merge_group(infra, group, collection, layer)
    total = sum(tris(obj) for obj in infra.objects if obj.type == "MESH")
    print(f"LOD1_INFRA_TOTAL meshes={len(infra.objects)} tris={total}")
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)


if __name__ == "__main__":
    main()
