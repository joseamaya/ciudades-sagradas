"""Construye el pase de valle de Chavín v0.7 sobre highpoly v0.6.

Uso:
  blender --background blender/chavin/chavin_highpoly_v0.6.blend \
    --python scripts/build_chavin_valley_v0_7.py -- \
    --out-blend blender/chavin/chavin_highpoly_v0.7.blend

No modifica arquitectura, galerías, Portada ni Lanzón. Sustituye únicamente
el terreno, ríos, rocas, vegetación y cámaras de paisaje.
"""

import argparse
import math
import os
import random
import sys

import bpy
import numpy as np
from mathutils import Matrix, Vector

TEXTURE_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "blender", "textures", "chavin")
)
TERRAIN_COLLECTION = "COL-Chavin_Terrain"
CAMERA_COLLECTION = "COL-Chavin_Cameras"
SITE_HALF_X = 148.0
SITE_HALF_Y = 157.0
SITE_TOP = 0.0
MOSNA_CENTER = 210.0
MOSNA_BANK = 48.0
WACHEQSA_CENTER = 300.0
WACHEQSA_BANK = 143.0
RIVER_BED = -28.0
WATER_Z = -26.45
FAR_Z = -25.5


def parse_args():
    argv = sys.argv
    argv = argv[argv.index("--") + 1 :] if "--" in argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-blend", required=True)
    return parser.parse_args(argv)


def smoothstep(edge0, edge1, value):
    if edge0 == edge1:
        return 1.0 if value >= edge1 else 0.0
    t = max(0.0, min(1.0, (value - edge0) / (edge1 - edge0)))
    return t * t * (3.0 - 2.0 * t)


def brighten(color, factor=1.12):
    return (min(1.0, color[0] * factor), min(1.0, color[1] * factor), min(1.0, color[2] * factor))


def surface_noise(x, y):
    return (
        0.55 * math.sin(x * 0.017 + y * 0.011)
        + 0.28 * math.sin(x * 0.043 - y * 0.031)
        + 0.17 * math.sin(x * 0.091 + y * 0.067)
    )


def mosna_center(y):
    return MOSNA_CENTER + 14.0 * math.sin(y / 82.0) + 5.0 * math.sin(y / 31.0)


def wacheqsa_center(x):
    return WACHEQSA_CENTER + 12.0 * math.sin(x / 78.0) + 4.0 * math.sin(x / 27.0)


def terrain_height(x, y):
    base = -24.0 + 2.6 * surface_noise(x, y)
    dx = max(abs(x) - SITE_HALF_X, 0.0)
    dy = max(abs(y) - SITE_HALF_Y, 0.0)
    distance = math.hypot(dx, dy)
    mesa = SITE_TOP - 0.4 - 31.0 * smoothstep(0.0, 35.0, distance)
    z = max(base, mesa)

    md = abs(x - mosna_center(y))
    if md < MOSNA_BANK:
        channel = RIVER_BED + 28.0 * smoothstep(15.0, MOSNA_BANK, md)
        z = min(z, channel)

    wd = abs(y - wacheqsa_center(x))
    if wd < WACHEQSA_BANK:
        channel = RIVER_BED + 28.0 * smoothstep(12.0, WACHEQSA_BANK, wd)
        z = min(z, channel)

    if distance > 10.0:
        z += 0.9 * surface_noise(x * 1.7, y * 1.7) * smoothstep(10.0, 55.0, distance)
    return z


def terrain_color(x, y, z):
    md = abs(x - mosna_center(y))
    wd = abs(y - wacheqsa_center(x))
    river = min(md, wd)
    n = 0.5 + 0.5 * surface_noise(x * 0.8, y * 0.8)
    slope = abs(terrain_height(x + 7.0, y) - z) + abs(terrain_height(x, y + 7.0) - z)
    if z < -25.8:
        return (0.50 + 0.08 * n, 0.46 + 0.06 * n, 0.38 + 0.04 * n)
    if river < 30.0:
        return (0.70 + 0.08 * n, 0.64 + 0.06 * n, 0.50 + 0.04 * n)
    if abs(x) < SITE_HALF_X + 32.0 and abs(y) < SITE_HALF_Y + 32.0:
        if slope > 1.1:
            return (0.66 + 0.06 * n, 0.60 + 0.05 * n, 0.48 + 0.04 * n)
        return (0.74 + 0.05 * n, 0.67 + 0.04 * n, 0.52 + 0.03 * n)
    if slope > 2.0 or z > 65.0:
        return (0.62 + 0.06 * n, 0.61 + 0.05 * n, 0.55 + 0.04 * n)
    if z > -19.0:
        if n > 0.62:
            return (0.46 + 0.06 * n, 0.58 + 0.06 * n, 0.31 + 0.04 * n)
        return (0.62 + 0.06 * n, 0.56 + 0.05 * n, 0.41 + 0.04 * n)
    return (0.64 + 0.06 * n, 0.56 + 0.05 * n, 0.42 + 0.04 * n)


def site_surface_color(x, y, z):
    n = 0.5 + 0.5 * surface_noise(x * 1.3, y * 1.3)
    if z > 2.55:
        return (0.66 + 0.05 * n, 0.61 + 0.04 * n, 0.49 + 0.03 * n)
    return (0.72 + 0.05 * n, 0.66 + 0.04 * n, 0.52 + 0.03 * n)


def ridge_color(height, max_height):
    t = max(0.0, min(1.0, height / max(1.0, max_height)))
    if t > 0.62:
        return (0.68, 0.67, 0.62)
    if t > 0.25:
        return (0.55, 0.55, 0.46)
    return (0.42, 0.52, 0.34)


def collection(name):
    coll = bpy.data.collections.get(name)
    if coll is None:
        raise RuntimeError(f"Falta la colección {name}")
    return coll


def add_color_attribute(mesh, colors):
    layer = mesh.color_attributes.new(name="Col", type="FLOAT_COLOR", domain="POINT")
    for index, color in enumerate(colors):
        layer.data[index].color = (color[0], color[1], color[2], 1.0)
    return layer


def add_uv_attribute(mesh, verts):
    uv_layer = mesh.uv_layers.new(name="UVMap")
    for polygon in mesh.polygons:
        for loop_index in polygon.loop_indices:
            vertex = verts[mesh.loops[loop_index].vertex_index]
            uv_layer.data[loop_index].uv = (vertex[0] / 320.0, vertex[1] / 320.0)
    return uv_layer


def mesh_object(name, verts, faces, material, colors=None, smooth=True):
    mesh = bpy.data.meshes.new("MESH-" + name[4:])
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    if colors is not None:
        add_color_attribute(mesh, colors)
    add_uv_attribute(mesh, verts)
    if smooth:
        for polygon in mesh.polygons:
            polygon.use_smooth = True
    obj = bpy.data.objects.new(name, mesh)
    collection(TERRAIN_COLLECTION).objects.link(obj)
    if material is not None:
        obj.data.materials.append(material)
    return obj


def ensure_color(obj, color_fn):
    mesh = obj.data
    if not mesh.color_attributes:
        mesh.color_attributes.new(name="Col", type="FLOAT_COLOR", domain="POINT")
    layer = mesh.color_attributes.get("Col")
    for index, vertex in enumerate(mesh.vertices):
        co = obj.matrix_world @ vertex.co
        color = brighten(color_fn(co.x, co.y, co.z))
        layer.data[index].color = (color[0], color[1], color[2], 1.0)
    if not mesh.uv_layers:
        add_uv_attribute(mesh, [(obj.matrix_world @ v.co)[:] for v in mesh.vertices])


def load_texture(name, filename, non_color=False):
    image = bpy.data.images.get(name)
    if image is None:
        image = bpy.data.images.load(os.path.join(TEXTURE_ROOT, filename), check_existing=True)
        image.name = name
    if non_color:
        image.colorspace_settings.name = "Non-Color"
    else:
        image.colorspace_settings.name = "sRGB"
    if image.packed_file is None:
        image.pack()
    return image


def material_earth():
    material = bpy.data.materials.get("MAT-Chavin_Earth")
    if material is None:
        material = bpy.data.materials.new("MAT-Chavin_Earth")
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    nodes.clear()
    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (420, 0)
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (120, 0)
    bsdf.inputs["Metallic"].default_value = 0.0
    bsdf.inputs["Roughness"].default_value = 0.92
    vertex = nodes.new("ShaderNodeVertexColor")
    vertex.name = "TerrainVertexColor"
    vertex.layer_name = "Col"
    vertex.location = (-520, 220)
    diffuse = nodes.new("ShaderNodeTexImage")
    diffuse.name = "TerrainDiffuse"
    diffuse.image = load_texture("chavin_terrain_v2_diffuse", "chavin_terrain_v2_diffuse.jpg")
    diffuse.location = (-520, -20)
    mix = nodes.new("ShaderNodeMixRGB")
    mix.blend_type = "MULTIPLY"
    mix.inputs["Fac"].default_value = 1.0
    mix.location = (-210, 120)
    links.new(diffuse.outputs["Color"], mix.inputs[1])
    links.new(vertex.outputs["Color"], mix.inputs[2])
    links.new(mix.outputs["Color"], bsdf.inputs["Base Color"])

    roughness = nodes.new("ShaderNodeTexImage")
    roughness.name = "TerrainRoughness"
    roughness.image = load_texture(
        "chavin_terrain_v2_roughness", "chavin_terrain_v2_roughness.jpg", non_color=True
    )
    roughness.location = (-520, -260)
    links.new(roughness.outputs["Color"], bsdf.inputs["Roughness"])

    normal = nodes.new("ShaderNodeTexImage")
    normal.name = "TerrainNormal"
    normal.image = load_texture(
        "chavin_terrain_v2_normal", "chavin_terrain_v2_normal.png", non_color=True
    )
    normal.location = (-520, -500)
    normal_map = nodes.new("ShaderNodeNormalMap")
    normal_map.location = (-210, -500)
    normal_map.inputs["Strength"].default_value = 0.95
    links.new(normal.outputs["Color"], normal_map.inputs["Color"])
    links.new(normal_map.outputs["Normal"], bsdf.inputs["Normal"])
    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    material["chavin:source"] = "scripts/make_chavin_terrain_materials_v2.py"
    return material


def material_water():
    material = bpy.data.materials.get("MAT-Chavin_Water")
    if material is None:
        material = bpy.data.materials.new("MAT-Chavin_Water")
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    nodes.clear()
    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (360, 0)
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (80, 0)
    bsdf.inputs["Base Color"].default_value = (0.075, 0.210, 0.230, 1.0)
    bsdf.inputs["Metallic"].default_value = 0.0
    bsdf.inputs["Roughness"].default_value = 0.22
    bsdf.inputs["IOR"].default_value = 1.333
    normal = nodes.new("ShaderNodeTexImage")
    normal.name = "WaterNormal"
    normal.image = load_texture("chavin_water_v1_normal", "chavin_water_v1_normal.png", non_color=True)
    normal.location = (-420, -220)
    normal_map = nodes.new("ShaderNodeNormalMap")
    normal_map.location = (-120, -220)
    normal_map.inputs["Strength"].default_value = 0.9
    links.new(normal.outputs["Color"], normal_map.inputs["Color"])
    links.new(normal_map.outputs["Normal"], bsdf.inputs["Normal"])
    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return material


def material_vegetation(name, color):
    material = bpy.data.materials.get(name)
    if material is None:
        material = bpy.data.materials.new(name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    nodes.clear()
    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (260, 0)
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (0, 0)
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.9
    nodes.new("ShaderNodeTexNoise")
    links = material.node_tree.links
    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    material.diffuse_color = (*color, 1.0)
    return material


def remove_old_terrain():
    prefixes = (
        "GEO-Chavin_Terrain_Valley",
        "GEO-Chavin_Terrain_Slope",
        "GEO-Chavin_Hill_",
        "GEO-Chavin_River_",
        "GEO-Chavin_Rock_Mosna_",
        "GEO-Chavin_Rock_Wacheqsa_",
        "GEO-Chavin_Rock_Plateau_",
    )
    for obj in list(bpy.data.objects):
        if obj.name.startswith(prefixes):
            bpy.data.objects.remove(obj, do_unlink=True)


def build_terrain(material):
    resolution = 96
    half = 650.0
    step = (half * 2.0) / resolution
    verts = []
    colors = []
    for j in range(resolution + 1):
        y = -half + j * step
        for i in range(resolution + 1):
            x = -half + i * step
            z = terrain_height(x, y)
            verts.append((x, y, z))
            colors.append(brighten(terrain_color(x, y, z)))
    faces = []
    for j in range(resolution):
        for i in range(resolution):
            a = j * (resolution + 1) + i
            b = a + 1
            c = a + resolution + 2
            d = a + resolution + 1
            faces.append((a, b, c, d))
    obj = mesh_object("GEO-Chavin_Terrain_Valley", verts, faces, material, colors)
    obj["chavin:evidence"] = "terreno inferido; cauce documentado en posición y desnivel"
    return obj


def build_site_ground(material):
    cols = 24
    rows = 24
    verts = []
    colors = []
    for j in range(rows + 1):
        y = -SITE_HALF_Y + 2.0 * SITE_HALF_Y * j / rows
        for i in range(cols + 1):
            x = -SITE_HALF_X + 2.0 * SITE_HALF_X * i / cols
            verts.append((x, y, 0.03))
            n = 0.5 + 0.5 * surface_noise(x * 1.7, y * 1.7)
            colors.append(brighten((0.72 + 0.05 * n, 0.66 + 0.04 * n, 0.52 + 0.03 * n)))
    faces = []
    for j in range(rows):
        for i in range(cols):
            a = j * (cols + 1) + i
            faces.append((a, a + 1, a + cols + 2, a + cols + 1))
    obj = mesh_object("GEO-Chavin_Terrain_SiteGround", verts, faces, material, colors)
    obj["chavin:evidence"] = "superficie inferida"
    return obj


def build_water(material):
    objects = []
    for name, axis, start, end, center_fn, width, level in (
        ("Mosna", "y", -625.0, 625.0, mosna_center, 20.0, WATER_Z),
        ("Wacheqsa", "x", -625.0, 204.0, wacheqsa_center, 16.0, WATER_Z + 0.02),
    ):
        verts = []
        faces = []
        steps = 104
        for index in range(steps + 1):
            t = start + (end - start) * index / steps
            if axis == "y":
                cx, cy = center_fn(t), t
                nx, ny = 1.0, 0.0
            else:
                cx, cy = t, center_fn(t)
                nx, ny = 0.0, 1.0
            half = width * 0.5 * (1.0 + 0.08 * math.sin(t / 31.0))
            verts.append((cx - nx * half, cy - ny * half, level))
            verts.append((cx + nx * half, cy + ny * half, level))
            if index:
                a = (index - 1) * 2
                faces.append((a, a + 1, a + 3, a + 2))
        obj = mesh_object(f"GEO-Chavin_River_{name}", verts, faces, material, smooth=False)
        objects.append(obj)
    return objects


def ridge_mesh(name, center, width, depth, height, angle, material):
    cols = 22
    rows = 10
    verts = []
    colors = []
    half_w = width * 0.5
    half_d = depth * 0.5
    rot = Matrix.Rotation(math.radians(angle), 3, "Z")
    for j in range(rows + 1):
        v = -1.0 + 2.0 * j / rows
        for i in range(cols + 1):
            u = -1.0 + 2.0 * i / cols
            profile = math.exp(-((u / 0.72) ** 2 + (v / 0.86) ** 2))
            detail = 0.55 + 0.45 * (0.5 + 0.5 * surface_noise(u * 11.0, v * 9.0))
            peaks = 0.45 + 0.55 * abs(math.sin(u * 7.3 + 0.8))
            h = height * profile * detail * peaks
            local = Vector((u * half_w, v * half_d, FAR_Z + h))
            world = rot @ local + Vector((center[0], center[1], 0.0))
            verts.append(tuple(world))
            colors.append(brighten(ridge_color(h, height), 1.15))
    faces = []
    for j in range(rows):
        for i in range(cols):
            a = j * (cols + 1) + i
            faces.append((a, a + 1, a + cols + 2, a + cols + 1))
    obj = mesh_object(name, verts, faces, material, colors, smooth=False)
    obj.visible_shadow = False
    obj["chavin:evidence"] = "silueta inferida"
    return obj


def build_mountains(material):
    ridges = (
        ("GEO-Chavin_Ridge_NW", (-1080.0, 880.0), 1080.0, 620.0, 430.0, 18.0),
        ("GEO-Chavin_Ridge_NE", (1080.0, 780.0), 1020.0, 660.0, 470.0, -22.0),
        ("GEO-Chavin_Ridge_SW", (-1040.0, -900.0), 1080.0, 660.0, 410.0, -15.0),
        ("GEO-Chavin_Ridge_SE", (1080.0, -860.0), 1020.0, 600.0, 450.0, 16.0),
        ("GEO-Chavin_Ridge_N", (0.0, 1420.0), 1320.0, 720.0, 540.0, 0.0),
        ("GEO-Chavin_Ridge_W", (-1450.0, 0.0), 920.0, 700.0, 460.0, 90.0),
    )
    for name, center, width, depth, height, angle in ridges:
        ridge_mesh(name, center, width, depth, height, angle, material)

    inner = 650.0
    half = 2400.0
    verts = []
    faces = []
    for x0, y0, x1, y1 in (
        (-half, inner, half, half),
        (-half, -half, half, -inner),
        (-half, -inner, -inner, inner),
        (inner, -inner, half, inner),
    ):
        base = len(verts)
        verts.extend([(x0, y0, FAR_Z), (x1, y0, FAR_Z), (x1, y1, FAR_Z), (x0, y1, FAR_Z)])
        faces.append((base, base + 1, base + 2, base + 3))
    colors = [(0.70, 0.72, 0.64)] * len(verts)
    far = mesh_object("GEO-Chavin_Terrain_Far", verts, faces, material, colors, smooth=False)
    far.visible_shadow = False


def add_river_rocks(stone, count=110):
    rng = random.Random(1407)
    for index in range(count):
        on_mosna = index % 2 == 0
        if on_mosna:
            y = rng.uniform(-590.0, 590.0)
            x = mosna_center(y) + rng.uniform(-22.0, 22.0)
        else:
            x = rng.uniform(-590.0, 180.0)
            y = wacheqsa_center(x) + rng.uniform(-18.0, 18.0)
        z = terrain_height(x, y) + 0.25
        scale = (rng.uniform(0.7, 2.4), rng.uniform(0.5, 1.8), rng.uniform(0.35, 1.1))
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1.0, location=(x, y, z))
        obj = bpy.context.object
        obj.name = f"GEO-Chavin_Rock_River_{index:03d}"
        obj.data.name = "MESH-Chavin_Rock_River"
        obj.dimensions = scale
        obj.rotation_euler = (
            rng.uniform(0.0, math.tau),
            rng.uniform(0.0, math.tau),
            rng.uniform(0.0, math.tau),
        )
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        for owner in list(obj.users_collection):
            owner.objects.unlink(obj)
        collection(TERRAIN_COLLECTION).objects.link(obj)
        obj.data.materials.append(stone)
        if index % 3:
            obj["lod1_exclude"] = True


def add_gravel_bars(material, count=7):
    rng = random.Random(331)
    for index in range(count):
        y = rng.uniform(-500.0, 500.0)
        side = -1.0 if index % 2 else 1.0
        x = mosna_center(y) + side * rng.uniform(13.0, 25.0)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1.0, location=(x, y, WATER_Z + 0.18))
        obj = bpy.context.object
        obj.name = f"GEO-Chavin_GravelBar_{index:03d}"
        obj.data.name = "MESH-Chavin_GravelBar"
        obj.dimensions = (rng.uniform(5.0, 10.0), rng.uniform(2.0, 3.6), rng.uniform(0.25, 0.45))
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        for owner in list(obj.users_collection):
            owner.objects.unlink(obj)
        collection(TERRAIN_COLLECTION).objects.link(obj)
        obj.data.materials.append(material)
        add_color_attribute(obj.data, [(0.85, 0.78, 0.64)] * len(obj.data.vertices))
        if index % 2:
            obj["lod1_exclude"] = True


def add_edge_boulders(stone, count=28):
    rng = random.Random(557)
    for index in range(count):
        if index % 2:
            x = SITE_HALF_X + rng.uniform(1.0, 9.0)
            y = rng.uniform(-SITE_HALF_Y, SITE_HALF_Y)
        else:
            x = rng.uniform(-SITE_HALF_X, SITE_HALF_X)
            y = SITE_HALF_Y + rng.uniform(1.0, 9.0)
        z = terrain_height(x, y)
        scale = (rng.uniform(1.2, 4.2), rng.uniform(1.0, 3.2), rng.uniform(0.7, 2.0))
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1.0, location=(x, y, z + scale[2] * 0.2))
        obj = bpy.context.object
        obj.name = f"GEO-Chavin_EdgeBoulder_{index:03d}"
        obj.data.name = "MESH-Chavin_EdgeBoulder"
        obj.dimensions = scale
        obj.rotation_euler = (rng.uniform(0.0, math.tau), rng.uniform(0.0, math.tau), rng.uniform(0.0, math.tau))
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        for owner in list(obj.users_collection):
            owner.objects.unlink(obj)
        collection(TERRAIN_COLLECTION).objects.link(obj)
        obj.data.materials.append(stone)
        if index % 3:
            obj["lod1_exclude"] = True


def add_boulders(stone, count=34):
    rng = random.Random(2231)
    for index in range(count):
        x = rng.uniform(-560.0, 560.0)
        y = rng.uniform(-560.0, 560.0)
        if abs(x) < SITE_HALF_X + 20.0 and abs(y) < SITE_HALF_Y + 20.0:
            continue
        z = terrain_height(x, y)
        if z < -24.0:
            continue
        scale = (rng.uniform(0.8, 3.2), rng.uniform(0.7, 2.4), rng.uniform(0.5, 1.6))
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1.0, location=(x, y, z + scale[2] * 0.3))
        obj = bpy.context.object
        obj.name = f"GEO-Chavin_Boulder_{index:03d}"
        obj.data.name = "MESH-Chavin_Boulder"
        obj.dimensions = scale
        obj.rotation_euler = (rng.uniform(0.0, math.tau), rng.uniform(0.0, math.tau), rng.uniform(0.0, math.tau))
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        for owner in list(obj.users_collection):
            owner.objects.unlink(obj)
        collection(TERRAIN_COLLECTION).objects.link(obj)
        obj.data.materials.append(stone)
        if index % 4:
            obj["lod1_exclude"] = True


def add_vegetation(light, dark):
    rng = random.Random(914)
    placed = 0
    attempts = 0
    while placed < 138 and attempts < 3000:
        attempts += 1
        x = rng.uniform(-610.0, 610.0)
        y = rng.uniform(-610.0, 610.0)
        if abs(x) < SITE_HALF_X + 16.0 and abs(y) < SITE_HALF_Y + 16.0:
            continue
        z = terrain_height(x, y)
        if z < -22.5:
            continue
        if abs(x - mosna_center(y)) < 30.0 or abs(y - wacheqsa_center(x)) < 26.0:
            continue
        slope = abs(terrain_height(x + 6.0, y) - z) + abs(terrain_height(x, y + 6.0) - z)
        if slope > 2.4:
            continue
        size = rng.uniform(0.45, 1.35)
        bpy.ops.mesh.primitive_ico_sphere_add(
            subdivisions=1, radius=1.0, location=(x, y, z + size * 0.55)
        )
        obj = bpy.context.object
        obj.name = f"GEO-Chavin_Shrub_{placed:03d}"
        obj.data.name = "MESH-Chavin_Shrub"
        obj.dimensions = (size * rng.uniform(1.0, 1.7), size * rng.uniform(0.8, 1.4), size)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        for owner in list(obj.users_collection):
            owner.objects.unlink(obj)
        collection(TERRAIN_COLLECTION).objects.link(obj)
        obj.data.materials.append(light if rng.random() < 0.62 else dark)
        if rng.random() < 0.68:
            obj["lod1_exclude"] = True
        placed += 1

    for index in range(190):
        x = rng.uniform(-600.0, 600.0)
        y = rng.uniform(-600.0, 600.0)
        if abs(x) < SITE_HALF_X + 8.0 and abs(y) < SITE_HALF_Y + 8.0:
            continue
        z = terrain_height(x, y)
        if z < -23.0:
            continue
        if abs(x - mosna_center(y)) < 28.0 or abs(y - wacheqsa_center(x)) < 24.0:
            continue
        bpy.ops.mesh.primitive_cone_add(
            vertices=5,
            radius1=rng.uniform(0.18, 0.42),
            radius2=0.02,
            depth=rng.uniform(0.45, 0.95),
            location=(x, y, z + 0.35),
        )
        obj = bpy.context.object
        obj.name = f"GEO-Chavin_Grass_{index:03d}"
        obj.data.name = "MESH-Chavin_Grass"
        for owner in list(obj.users_collection):
            owner.objects.unlink(obj)
        collection(TERRAIN_COLLECTION).objects.link(obj)
        obj.data.materials.append(light if rng.random() < 0.7 else dark)
        if rng.random() < 0.5:
            obj["lod1_exclude"] = True


def update_camera(name, location, target, lens):
    camera = bpy.data.objects.get(name)
    if camera is None or camera.type != "CAMERA":
        data = bpy.data.cameras.new("DATA-" + name[4:])
        camera = bpy.data.objects.new(name, data)
        collection(CAMERA_COLLECTION).objects.link(camera)
    camera.location = location
    direction = Vector(target) - Vector(location)
    camera.rotation_mode = "QUATERNION"
    camera.rotation_quaternion = direction.to_track_quat("-Z", "Y")
    camera.data.lens = lens
    camera.data.clip_end = 5000.0
    return camera


def main():
    args = parse_args()
    remove_old_terrain()
    earth = material_earth()
    water = material_water()
    light = material_vegetation("MAT-Chavin_Vegetation", (0.28, 0.42, 0.16))
    dark = material_vegetation("MAT-Chavin_Vegetation_Dark", (0.18, 0.30, 0.11))
    stone = bpy.data.materials.get("MAT-Chavin_Stone_Tiled")
    if stone is None:
        raise RuntimeError("Falta MAT-Chavin_Stone_Tiled")

    for name in ("GEO-Chavin_Terrain_SitePlateau", "GEO-Chavin_Terrain_Terrace_01",
                 "GEO-Chavin_Terrain_Terrace_02", "GEO-Chavin_Terrain_Terrace_03"):
        obj = bpy.data.objects.get(name)
        if obj is not None:
            ensure_color(obj, site_surface_color)

    build_terrain(earth)
    build_site_ground(earth)
    build_water(water)
    build_mountains(earth)
    add_river_rocks(stone)
    add_gravel_bars(earth)
    add_edge_boulders(stone)
    add_boulders(stone)
    add_vegetation(light, dark)
    update_camera("CAM-Chavin_Hero", (500.0, 0.0, 337.5), (87.5, 0.0, -18.75), 45.0)
    update_camera("CAM-Chavin_Plan", (0.0, 0.0, 760.0), (0.0, 0.0, 0.0), 50.0)
    update_camera("CAM-Chavin_HP_Valley", (320.0, -320.0, 130.0), (10.0, 20.0, -2.0), 38.0)
    update_camera("CAM-Chavin_HP_Confluence", (390.0, 430.0, 145.0), (150.0, 250.0, -18.0), 42.0)
    update_camera("CAM-Chavin_HP_River", (305.0, -40.0, 35.0), (210.0, 60.0, -25.0), 55.0)

    world = bpy.context.scene.world
    if world and world.use_nodes:
        background = world.node_tree.nodes.get("Background")
        if background:
            background.inputs[0].default_value = (0.10, 0.13, 0.16, 1.0)
            background.inputs[1].default_value = 0.9
    fill = bpy.data.objects.get("LGT-Chavin_Fill")
    if fill and fill.data.type == "AREA":
        fill.data.energy = 700.0
        fill.data.size = 220.0
    bpy.context.scene.camera = bpy.data.objects.get("CAM-Chavin_Hero")
    bpy.context.scene["chavin:terrain"] = "v0.7-valle-procedural"
    bpy.context.scene["chavin:terrain_evidence"] = "inferido; cauces documentados en posición y desnivel"
    out = os.path.abspath(args.out_blend)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=out)
    print("CHAVIN_VALLEY_OK", out)
    print("TERRAIN_OBJECTS", len(collection(TERRAIN_COLLECTION).objects))


if __name__ == "__main__":
    main()
