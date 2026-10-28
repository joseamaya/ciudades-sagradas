"""Sustituye el Lanzón v0.2 por una malla adaptada del escaneo CyArk.

Uso:
  blender --background blender/chavin/chavin_highpoly_v0.2.blend \
    --python scripts/build_chavin_lanzon_scan_v0_3.py -- \
    --scan /tmp/chavin_scan/lanzon_cyark.glb \
    --out-blend blender/chavin/chavin_highpoly_v0.3.blend

El escaneo no se versiona. La malla resultante es un derivado CC BY-NC-SA 4.0
de CyArk/Google Arts & Culture; se conserva la atribución en los metadatos y
en docs/fuentes/registro-assets.csv. No se reutiliza la textura fotográfica.
"""

import argparse
import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

SCAN_OBJECT = "Lnzon_Chavin_De_Huantar_glb"
LANZON_SIZE_Z = 4.5
LANZON_BASE_Z = 3.0
LANZON_CENTER_Y = 62.0
SLAB_Z = 0.045
DEFAULT_SCAN = "/tmp/chavin_scan/lanzon_cyark.glb"


def parse_args():
    argv = sys.argv
    argv = argv[argv.index("--") + 1 :] if "--" in argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--scan", default=DEFAULT_SCAN)
    parser.add_argument("--out-blend", required=True)
    parser.add_argument("--target-tris", type=int, default=50000)
    parser.add_argument("--normal-size", type=int, default=2048)
    parser.add_argument("--no-bake", action="store_true")
    return parser.parse_args(argv)


def activate(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def apply_transform(obj):
    activate(obj)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


def bounds(obj):
    verts = [obj.matrix_world @ vertex.co for vertex in obj.data.vertices]
    minimum = Vector((min(v[i] for v in verts) for i in range(3)))
    maximum = Vector((max(v[i] for v in verts) for i in range(3)))
    return minimum, maximum


def clean_scan(obj, slab_z):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    slab = [vertex for vertex in bm.verts if vertex.co.z < slab_z]
    if slab:
        bmesh.ops.delete(bm, geom=slab, context="VERTS")
    loose = [vertex for vertex in bm.verts if not vertex.link_faces]
    if loose:
        bmesh.ops.delete(bm, geom=loose, context="VERTS")
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()


def repair_mesh(obj):
    activate(obj)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.customdata_custom_splitnormals_clear()
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.mesh.fill_holes(sides=0)
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.shade_smooth()


def create_scan_material(name, normal_image=None):
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    bsdf = next(node for node in nodes if node.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (0.085, 0.080, 0.072, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.93
    bsdf.inputs["Metallic"].default_value = 0.0
    material.diffuse_color = (0.085, 0.080, 0.072, 1.0)
    if normal_image is not None:
        texture = nodes.new("ShaderNodeTexImage")
        texture.name = "LanzonNormal"
        texture.image = normal_image
        texture.location = (-620, -260)
        normal_map = nodes.new("ShaderNodeNormalMap")
        normal_map.name = "LanzonNormalMap"
        normal_map.location = (-300, -260)
        normal_map.inputs["Strength"].default_value = 1.0
        links.new(texture.outputs["Color"], normal_map.inputs["Color"])
        links.new(normal_map.outputs["Normal"], bsdf.inputs["Normal"])
        nodes.active = texture
    return material


def bake_normal(high, low, size):
    if low.data.uv_layers:
        uv_layer = low.data.uv_layers.new(name="UVMap_Bake")
        low.data.uv_layers.active = uv_layer
    activate(low)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(66.0), island_margin=0.015)
    bpy.ops.object.mode_set(mode="OBJECT")
    image = bpy.data.images.new("chavin_lanzon_v1_normal", size, size)
    image.colorspace_settings.name = "Non-Color"
    material = create_scan_material("MAT-Chavin_Lanzon_Scan", image)
    low.data.materials.clear()
    low.data.materials.append(material)

    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 1
    scene.cycles.use_denoising = False
    scene.render.bake.margin = 16
    scene.render.bake.use_clear = True

    bpy.ops.object.select_all(action="DESELECT")
    high.hide_set(False)
    high.hide_render = False
    high.select_set(True)
    low.hide_set(False)
    low.hide_render = False
    low.select_set(True)
    bpy.context.view_layer.objects.active = low
    bpy.ops.object.bake(
        type="NORMAL",
        use_selected_to_active=True,
        cage_extrusion=0.01,
        normal_space="TANGENT",
        margin=16,
        use_clear=True,
    )
    image.pack()
    print("CHAVIN_LANZON_NORMAL_BAKED", image.name, image.size[:])
    return material


def decimate(obj, target_tris):
    obj.data.calc_loop_triangles()
    current = len(obj.data.loop_triangles)
    if current <= target_tris:
        return current
    modifier = obj.modifiers.new("ScanDecimate", "DECIMATE")
    modifier.decimate_type = "COLLAPSE"
    modifier.ratio = target_tris / current
    modifier.use_collapse_triangulate = True
    activate(obj)
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    obj.data.calc_loop_triangles()
    return len(obj.data.loop_triangles)


def main():
    args = parse_args()
    scan = os.path.abspath(args.scan)
    out = os.path.abspath(args.out_blend)
    if not os.path.exists(scan):
        raise SystemExit(f"No existe el escaneo: {scan}")

    bpy.ops.object.select_all(action="DESELECT")
    bpy.ops.import_scene.gltf(filepath=scan)
    imported = bpy.data.objects.get(SCAN_OBJECT)
    if imported is None:
        imported = next(
            (obj for obj in bpy.context.selected_objects if obj.type == "MESH"),
            None,
        )
    if imported is None:
        raise SystemExit("No se importó ninguna malla del escaneo")

    apply_transform(imported)
    clean_scan(imported, SLAB_Z)
    imported.rotation_mode = "XYZ"
    imported.rotation_euler[0] = math.pi
    imported.rotation_euler[2] = -math.pi / 2
    apply_transform(imported)
    minimum, _ = bounds(imported)
    imported.location.z -= minimum.z
    apply_transform(imported)
    clean_scan(imported, SLAB_Z)

    minimum, maximum = bounds(imported)
    scale = LANZON_SIZE_Z / (maximum.z - minimum.z)
    imported.scale = (scale, scale, scale)
    apply_transform(imported)
    minimum, maximum = bounds(imported)
    center = (minimum + maximum) * 0.5
    imported.location.x += -center.x
    imported.location.y += LANZON_CENTER_Y - center.y
    imported.location.z += LANZON_BASE_Z - minimum.z
    apply_transform(imported)

    high = None
    if not args.no_bake:
        high = imported.copy()
        high.data = imported.data.copy()
        high.name = "GEO-Chavin_Lanzon_BakeHigh"
        high.data.name = "MESH-Chavin_Lanzon_BakeHigh"
        for collection in imported.users_collection:
            collection.objects.link(high)

    tris = decimate(imported, args.target_tris)
    repair_mesh(imported)
    scan_material = None
    if high is not None:
        scan_material = bake_normal(high, imported, args.normal_size)
        bpy.data.objects.remove(high, do_unlink=True)

    for name in ("GEO-Chavin_Lanzon_HP_FaceRelief",):
        obj = bpy.data.objects.get(name)
        if obj is not None:
            bpy.data.objects.remove(obj, do_unlink=True)
    old = bpy.data.objects.get("GEO-Chavin_Lanzon")
    if old is not None and old != imported:
        bpy.data.objects.remove(old, do_unlink=True)

    imported.name = "GEO-Chavin_Lanzon"
    imported.data.name = "MESH-Chavin_Lanzon_Scan"
    imported["layer"] = "props"
    imported["lod"] = 0
    imported["lod1_exclude"] = True
    imported["units"] = "meters"
    imported["chavin_highpoly"] = "v0.3"
    imported["source"] = "CyArk / Google Arts & Culture, Lanzón de Chavín"
    imported["license"] = "CC BY-NC-SA 4.0"
    imported["attribution"] = "CyArk; adaptación del proyecto Ciudades Sagradas"
    imported["evidence"] = "documentado (escaneo) + adaptado"
    imported["derivative"] = "geometría decimada; textura fotográfica no reutilizada"

    if scan_material is None:
        scan_material = create_scan_material("MAT-Chavin_Lanzon_Scan")
    imported.data.materials.clear()
    imported.data.materials.append(scan_material)

    old_plain = bpy.data.objects.get("GEO-Chavin_Lanzon_Plain")
    if old_plain is not None:
        bpy.data.objects.remove(old_plain, do_unlink=True)
    plain = imported.copy()
    plain.data = imported.data.copy()
    plain.name = "GEO-Chavin_Lanzon_Plain"
    plain.data.name = "MESH-Chavin_Lanzon_Plain"
    for collection in imported.users_collection:
        collection.objects.link(plain)
    decimate(plain, 12000)
    plain.data.materials.clear()
    plain.data.materials.append(scan_material)
    plain["lod1_quality"] = "malla decimada 12k"
    plain["lod0_exclude"] = True
    plain["lod1_exclude"] = False
    plain["lod"] = 1
    plain["chavin_highpoly"] = "v0.3"
    plain["units"] = "meters"
    plain.hide_viewport = False
    plain.hide_render = True
    plain.hide_set(True)

    scan_material = bpy.data.materials.get("lambert18.001")
    if scan_material is not None and scan_material.users == 0:
        bpy.data.materials.remove(scan_material)
    for image in list(bpy.data.images):
        if image.users == 0 and image.name != "Render Result":
            bpy.data.images.remove(image)

    bpy.context.scene.camera = bpy.data.objects.get("CAM-Chavin_HP_LanzonFace")
    bpy.ops.wm.save_as_mainfile(filepath=out)

    minimum, maximum = bounds(imported)
    print(
        "CHAVIN_LANZON_SCAN_OK",
        out,
        "tris", tris,
        "min", tuple(round(x, 3) for x in minimum),
        "max", tuple(round(x, 3) for x in maximum),
        "scan", scan,
    )


if __name__ == "__main__":
    main()
