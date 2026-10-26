"""Bake de LOD1 para Caral v2 (Fase C).

Uso:
    blender --background blender/caral/caral_remaster_v2.blend \
      --python scripts/bake_caral_lod1.py -- \
      --out-blend blender/caral/caral_lod1.blend \
      --texture-dir blender/textures/baked/caral \
      --resolution 2048

Después, fusionar la infraestructura:
    blender --background blender/caral/caral_lod1.blend \
      --python scripts/optimize_caral_lod1.py

No modifica public/ ni caral_remaster_v2.blend.
"""

import argparse
import math
import os
import sys

import bpy
import numpy as np


REGIONS = {
    "Mayor": {
        "high": "COL-Caral_HighPoly_Mayor",
        "low": "COL-Caral_LowPoly_Mayor",
        "sublayer": "mayor",
        "source": "UNESCO 1269 p. 351",
        "exclude_low": (),
        "include_high": (),
    },
    "PlazaMayor": {
        "high": "COL-Caral_HighPoly_PlazaMayor",
        "low": "COL-Caral_LowPoly_PlazaMayor",
        "sublayer": "plaza-mayor",
        "source": "UNESCO 1269 p. 351",
        "exclude_low": ("GEO-Caral_PlazaMayor_Piso",),
        "include_high": (),
        "include_high_exact": ("GEO-Caral_HighPoly_plaza-mayor_Piso",),
        "keep_separate": (
            "GEO-Caral_PlazaMayor_BandaRoja",
            "GEO-Caral_PlazaMayor_PisoAnilloRojo",
            "GEO-Caral_PlazaMayor_PisoRojo",
            "GEO-Caral_PlazaMayor_Fogon",
            "GEO-Caral_PlazaMayor_FogonAro",
        ),
    },
    "Anfiteatro": {
        "high": "COL-Caral_HighPoly_Anfiteatro",
        "low": "COL-Caral_LowPoly_Anfiteatro",
        "sublayer": "anfiteatro",
        "source": "UNESCO 1269 p. 358",
        "exclude_low": (),
        "include_high": (),
    },
    "AltarCircular": {
        "high": "COL-Caral_HighPoly_AltarCircular",
        "low": "COL-Caral_LowPoly_AltarCircular",
        "sublayer": "altar-circular",
        "source": "UNESCO 1269 p. 359",
        "exclude_low": ("GEO-Caral_AltarCircular_Aro", "GEO-Caral_AltarCircular_Altar"),
        "include_high": ("_AltarRing", "_AltarCoping"),
    },
}
EXCLUDED_COLLECTIONS = {
    "COL-Caral_GameExport",
    "COL-Caral_ScenarioCityExport",
    "COL-Caral_Gameplay",
    "COL-Caral_Cameras",
    "COL-Caral_Lights",
}


def parse_args():
    argv = sys.argv
    argv = argv[argv.index("--") + 1 :] if "--" in argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-blend", required=True)
    parser.add_argument("--texture-dir", required=True)
    parser.add_argument("--resolution", type=int, default=2048)
    parser.add_argument("--ao-samples", type=int, default=48)
    parser.add_argument("--ao-distance", type=float, default=0.35)
    parser.add_argument("--regions", default="all")
    parser.add_argument("--no-ao", action="store_true")
    return parser.parse_args(argv)


def ensure_collection(name, parent):
    collection = bpy.data.collections.get(name)
    if collection is None:
        collection = bpy.data.collections.new(name)
    if collection.name not in parent.children:
        parent.children.link(collection)
    return collection


def unhide_collection(collection):
    collection.hide_viewport = False
    collection.hide_render = False
    for obj in collection.objects:
        obj.hide_set(False)
        obj.hide_render = False


def hide_collection(collection):
    collection.hide_viewport = True
    collection.hide_render = True


def deselect_all():
    for obj in bpy.context.view_layer.objects:
        obj.select_set(False)


def evaluated_mesh_object(obj, collection, depsgraph):
    evaluated = obj.evaluated_get(depsgraph)
    mesh = bpy.data.meshes.new_from_object(
        evaluated,
        preserve_all_data_layers=True,
        depsgraph=depsgraph,
    )
    duplicate = bpy.data.objects.new(obj.name + "_LOD1_tmp", mesh)
    collection.objects.link(duplicate)
    duplicate.matrix_world = obj.matrix_world.copy()
    duplicate.hide_set(False)
    duplicate.hide_render = False
    return duplicate


def build_region_lod1(region, config, lod_root, depsgraph, resolution, texture_dir):
    high = bpy.data.collections[config["high"]]
    low = bpy.data.collections[config["low"]]
    work = ensure_collection("COL-Caral_LOD1_" + region, lod_root)
    unhide_collection(low)
    bpy.context.view_layer.update()
    depsgraph = bpy.context.evaluated_depsgraph_get()

    copies = []
    separate = []
    keep_separate = config.get("keep_separate", ())
    for obj in low.objects:
        if obj.type != "MESH":
            continue
        if obj.name in keep_separate:
            duplicate = evaluated_mesh_object(obj, work, depsgraph)
            duplicate.name = "GEO-Caral_LOD1_" + region + "_" + obj.name.split("_")[-1]
            duplicate["layer"] = "city"
            duplicate["sublayer"] = config["sublayer"]
            duplicate["lod"] = 1
            duplicate["units"] = "meters"
            duplicate["source"] = config["source"]
            duplicate["evidence"] = "documentado + inferido"
            separate.append(duplicate)
            continue
        if obj.name in config["exclude_low"]:
            continue
        copies.append(evaluated_mesh_object(obj, work, depsgraph))

    include_exact = config.get("include_high_exact", ())
    for obj in high.objects:
        if obj.type != "MESH":
            continue
        matches_suffix = bool(config["include_high"]) and any(
            suffix in obj.name for suffix in config["include_high"]
        )
        if obj.name not in include_exact and not matches_suffix:
            continue
        mesh = obj.data.copy()
        duplicate = bpy.data.objects.new(obj.name + "_LOD1_tmp", mesh)
        work.objects.link(duplicate)
        duplicate.matrix_world = obj.matrix_world.copy()
        copies.append(duplicate)

    if not copies:
        raise RuntimeError(f"No hay geometría para {region}")
    deselect_all()
    for obj in copies:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = copies[0]
    bpy.ops.object.join()
    lod = bpy.context.view_layer.objects.active
    lod.name = "GEO-Caral_LOD1_" + region
    lod.data.name = lod.name + "_Mesh"
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode="OBJECT")

    lod.data.materials.clear()
    material = create_bake_material(region, resolution, texture_dir)
    lod.data.materials.append(material)
    lod["layer"] = "city"
    lod["sublayer"] = config["sublayer"]
    lod["lod"] = 1
    lod["units"] = "meters"
    lod["source"] = config["source"]
    lod["evidence"] = "documentado + inferido"

    uv = lod.data.uv_layers.new(name="UVAtlas")
    lod.data.uv_layers.active = uv
    for layer in list(lod.data.uv_layers):
        if layer.name != "UVAtlas":
            lod.data.uv_layers.remove(layer)
    uv.active_render = True

    bpy.context.view_layer.objects.active = lod
    lod.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(
        angle_limit=math.radians(66),
        island_margin=0.015,
        area_weight=0.0,
        correct_aspect=True,
        scale_to_bounds=False,
    )
    bpy.ops.object.mode_set(mode="OBJECT")
    lod.data.calc_loop_triangles()
    for obj in separate:
        deselect_all()
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    print(
        f"LOD1_BUILT {region} tris={len(lod.data.loop_triangles)} "
        f"uvs={len(lod.data.uv_layers)} separate={len(separate)}"
    )
    return lod, high, work


def create_image(name, resolution, colorspace, path):
    image = bpy.data.images.new(name, width=resolution, height=resolution, alpha=False)
    image.colorspace_settings.name = colorspace
    image.filepath_raw = path
    image.file_format = "PNG"
    return image


def create_bake_material(region, resolution, texture_dir):
    os.makedirs(texture_dir, exist_ok=True)
    material = bpy.data.materials.new("MAT-Caral_LOD1_" + region)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    for node in list(nodes):
        nodes.remove(node)
    output = nodes.new("ShaderNodeOutputMaterial")
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (100, 0)
    links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])

    base = create_image(
        f"CARAL_LOD1_{region}_BaseColor",
        resolution,
        "sRGB",
        os.path.join(texture_dir, f"lod1_{region.lower()}_basecolor.png"),
    )
    normal = create_image(
        f"CARAL_LOD1_{region}_Normal",
        resolution,
        "Non-Color",
        os.path.join(texture_dir, f"lod1_{region.lower()}_normal.png"),
    )
    ao = create_image(
        f"CARAL_LOD1_{region}_AO",
        resolution,
        "Non-Color",
        os.path.join(texture_dir, f"lod1_{region.lower()}_ao.png"),
    )
    rough = create_image(
        f"CARAL_LOD1_{region}_Roughness",
        resolution,
        "Non-Color",
        os.path.join(texture_dir, f"lod1_{region.lower()}_roughness.png"),
    )

    tex_base = nodes.new("ShaderNodeTexImage")
    tex_base.name = "Bake_BaseColor"
    tex_base.label = "BASE COLOR"
    tex_base.image = base
    tex_base.location = (-500, 300)
    tex_normal = nodes.new("ShaderNodeTexImage")
    tex_normal.name = "Bake_Normal"
    tex_normal.label = "NORMAL"
    tex_normal.image = normal
    tex_normal.location = (-500, 60)
    tex_ao = nodes.new("ShaderNodeTexImage")
    tex_ao.name = "Bake_AO"
    tex_ao.label = "AO"
    tex_ao.image = ao
    tex_ao.location = (-500, -180)
    tex_rough = nodes.new("ShaderNodeTexImage")
    tex_rough.name = "Bake_Roughness"
    tex_rough.label = "ROUGHNESS"
    tex_rough.image = rough
    tex_rough.location = (-500, -420)

    material["bake_region"] = region
    material["tex_base"] = base.name
    material["tex_normal"] = normal.name
    material["tex_ao"] = ao.name
    material["tex_roughness"] = rough.name
    return material


def connect_material(material, include_ao=True):
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    bsdf = next(node for node in nodes if node.type == "BSDF_PRINCIPLED")
    tex_base = nodes["Bake_BaseColor"]
    tex_normal = nodes["Bake_Normal"]
    tex_rough = nodes["Bake_Roughness"]
    tex_ao = nodes["Bake_AO"]
    normal_map = nodes.new("ShaderNodeNormalMap")
    normal_map.location = (-180, 40)
    normal_map.inputs["Strength"].default_value = 0.35
    links.new(tex_base.outputs["Color"], bsdf.inputs["Base Color"])
    links.new(tex_normal.outputs["Color"], normal_map.inputs["Color"])
    links.new(normal_map.outputs["Normal"], bsdf.inputs["Normal"])
    bsdf.inputs["Roughness"].default_value = 0.85
    material["roughness_mode"] = "constante 0.85"

    if include_ao:
        group = bpy.data.node_groups.get("glTF Material Output")
        if group is None:
            group = bpy.data.node_groups.new("glTF Material Output", "ShaderNodeTree")
            group.interface.new_socket(name="Occlusion", in_out="INPUT", socket_type="NodeSocketFloat")
        group_node = nodes.new("ShaderNodeGroup")
        group_node.node_tree = group
        group_node.location = (100, -260)
        links.new(tex_ao.outputs["Color"], group_node.inputs["Occlusion"])


def bake_image(lod, high, material, node_name, bake_type, image_path, samples, pass_filter=None, normal_space=None, selected_to_active=True):
    nodes = material.node_tree.nodes
    bpy.context.view_layer.objects.active = lod
    deselect_all()
    lod.select_set(True)
    if selected_to_active:
        for obj in high.objects:
            if obj.type == "MESH":
                obj.hide_set(False)
                obj.select_set(True)
    bpy.context.view_layer.objects.active = lod
    for node in nodes:
        node.select = False
    target = nodes[node_name]
    target.select = True
    material.node_tree.nodes.active = target
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = samples
    scene.cycles.use_denoising = False
    kwargs = {
        "type": bake_type,
        "margin": 12,
        "use_clear": True,
        "use_selected_to_active": selected_to_active,
        "cage_extrusion": 0.55,
        "max_ray_distance": 1.0,
    }
    if pass_filter is not None:
        kwargs["pass_filter"] = pass_filter
    if normal_space is not None:
        kwargs["normal_space"] = normal_space
    hidden = []
    if not selected_to_active:
        for obj in bpy.context.view_layer.objects:
            if obj != lod and obj.type == "MESH" and not obj.hide_render:
                hidden.append(obj)
                obj.hide_render = True
    try:
        bpy.ops.object.bake(**kwargs)
    finally:
        for obj in hidden:
            obj.hide_render = False
    image = target.image
    image.filepath_raw = image_path
    image.file_format = "PNG"
    image.save()
    print(f"BAKED {bake_type} {image_path} {image.size[0]}x{image.size[1]} samples={samples}")


def fill_gaps(image, mode, iterations=48):
    width, height = image.size
    pixels = np.array(image.pixels[:], dtype=np.float32).reshape(height, width, 4)
    rgb = pixels[..., :3]
    if mode == "normal":
        invalid = np.max(rgb, axis=2) < 0.01
        fill = np.array([0.5, 0.5, 1.0], dtype=np.float32)
    else:
        invalid = np.max(rgb, axis=2) < 0.001
        fill = None
    if not invalid.any():
        return
    valid = ~invalid
    if fill is not None:
        rgb[invalid] = fill
        valid = valid | invalid
    else:
        for _ in range(iterations):
            if valid.all():
                break
            pad_rgb = np.pad(rgb, ((1, 1), (1, 1), (0, 0)), mode="edge")
            pad_valid = np.pad(valid, 1, mode="constant", constant_values=False)
            acc = np.zeros_like(rgb)
            count = np.zeros((height, width), dtype=np.float32)
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dy == 0 and dx == 0:
                        continue
                    shifted = pad_rgb[1 + dy : 1 + dy + height, 1 + dx : 1 + dx + width]
                    shifted_valid = pad_valid[1 + dy : 1 + dy + height, 1 + dx : 1 + dx + width]
                    acc += shifted * shifted_valid[..., None]
                    count += shifted_valid
            update = (invalid & ~valid) & (count > 0)
            if not update.any():
                break
            rgb[update] = acc[update] / count[update, None]
            valid |= update
    if mode == "normal":
        vector = rgb * 2.0 - 1.0
        length = np.linalg.norm(vector, axis=2, keepdims=True)
        vector = vector / np.where(length < 1e-6, 1.0, length)
        rgb = vector * 0.5 + 0.5
    pixels[..., :3] = np.clip(rgb, 0.0, 1.0)
    image.pixels.foreach_set(pixels.ravel())
    image.update()
    image.save()
    print(f"CLEANED {image.name} invalid={int(invalid.sum())} mode={mode}")


def bake_region(lod, high, material, region, resolution, ao_samples, texture_dir, include_ao=True):
    base_path = os.path.join(texture_dir, f"lod1_{region.lower()}_basecolor.png")
    normal_path = os.path.join(texture_dir, f"lod1_{region.lower()}_normal.png")
    ao_path = os.path.join(texture_dir, f"lod1_{region.lower()}_ao.png")
    rough_path = os.path.join(texture_dir, f"lod1_{region.lower()}_roughness.png")
    bake_image(lod, high, material, "Bake_BaseColor", "DIFFUSE", base_path, 1, pass_filter={"COLOR"})
    bake_image(lod, high, material, "Bake_Normal", "NORMAL", normal_path, 1, normal_space="TANGENT")
    bake_image(lod, high, material, "Bake_Roughness", "ROUGHNESS", rough_path, 1)
    if include_ao:
        bake_image(lod, high, material, "Bake_AO", "AO", ao_path, ao_samples, selected_to_active=False)
    nodes = material.node_tree.nodes
    fill_gaps(nodes["Bake_BaseColor"].image, "color")
    fill_gaps(nodes["Bake_Normal"].image, "normal")
    fill_gaps(nodes["Bake_Roughness"].image, "roughness")
    connect_material(material, include_ao=include_ao)


def main():
    args = parse_args()
    if not bpy.data.filepath.endswith("caral_remaster_v2.blend"):
        raise RuntimeError("Abrir caral_remaster_v2.blend antes de ejecutar")
    if bpy.data.collections.get("COL-Caral_LOD1") is not None:
        raise RuntimeError("COL-Caral_LOD1 ya existe; usar una escena v2 limpia")
    out_blend = os.path.abspath(args.out_blend)
    texture_dir = os.path.abspath(args.texture_dir)
    os.makedirs(os.path.dirname(out_blend), exist_ok=True)
    os.makedirs(texture_dir, exist_ok=True)
    resolution = args.resolution
    ao_samples = args.ao_samples
    if bpy.context.scene.world is not None:
        bpy.context.scene.world.light_settings.distance = args.ao_distance
        print(f"AO_DISTANCE {args.ao_distance}")
    selected_regions = list(REGIONS) if args.regions == "all" else [r.strip() for r in args.regions.split(",") if r.strip()]
    for region in selected_regions:
        if region not in REGIONS:
            raise RuntimeError(f"Región desconocida: {region}")

    lod_root = ensure_collection("COL-Caral_LOD1", bpy.context.scene.collection)
    lod_root.hide_render = False
    lod_root.hide_viewport = False
    high_root = bpy.data.collections["COL-Caral_HighPoly"]
    low_root = bpy.data.collections["COL-Caral_LowPoly"]
    unhide_collection(high_root)
    unhide_collection(low_root)
    for region in REGIONS:
        hide_collection(bpy.data.collections[REGIONS[region]["high"]])
        hide_collection(bpy.data.collections[REGIONS[region]["low"]])

    for region in selected_regions:
        config = REGIONS[region]
        high = bpy.data.collections[config["high"]]
        low = bpy.data.collections[config["low"]]
        unhide_collection(high)
        unhide_collection(low)
        bpy.context.view_layer.update()
        lod, high, work = build_region_lod1(region, config, lod_root, bpy.context.evaluated_depsgraph_get(), resolution, texture_dir)
        bake_region(lod, high, lod.data.materials[0], region, resolution, ao_samples, texture_dir, include_ao=not args.no_ao)
        bpy.ops.wm.save_as_mainfile(filepath=out_blend)
        print(f"SAVED_LOD1_REGION {region} -> {out_blend}")
        hide_collection(high)
        hide_collection(low)

    hide_collection(high_root)
    hide_collection(low_root)
    lod_root.hide_render = False
    lod_root.hide_viewport = False
    deselect_all()
    bpy.context.scene.camera = bpy.data.objects.get("CAM-Caral_V2_Mayor", bpy.context.scene.camera)
    bpy.ops.wm.save_as_mainfile(filepath=out_blend)

    for region in selected_regions:
        lod = bpy.data.objects.get("GEO-Caral_LOD1_" + region)
        lod.data.calc_loop_triangles()
        print(
            f"LOD1_FINAL {region} tris={len(lod.data.loop_triangles)} "
            f"uv={lod.data.uv_layers.active.name} "
            f"material={lod.data.materials[0].name}"
        )
    print(f"LOD1_BAKE_OK {out_blend}")


if __name__ == "__main__":
    main()
