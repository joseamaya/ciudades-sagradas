"""Genera el blockout navegable de Aypate v0.1.

Uso:
  blender --background --python scripts/build_aypate_blockout.py

La planta completa de Aypate no está publicada. El blockout usa la descripción
del Proyecto Integral Aypate (plaza, ushnu, kallanka, acllawasi, palacio,
colcas, fuente y Qhapaq Ñan) y marca la composición como interpretativa.
No copia imágenes oficiales ni usa texturas de IA.
"""

import math
import os
import random

import bpy
import bmesh
import numpy as np
from mathutils import Matrix, Vector

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_BLEND = os.path.join(ROOT, "blender", "aypate", "aypate_blockout_v0.1.blend")
HERO = "/tmp/aypate_hero.jpg"
SEED = 7319
SIZE = 512
PLAZA_Z = 8.0


def clean_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 1600
    scene.render.resolution_y = 900
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "JPEG"
    scene.render.image_settings.quality = 88
    scene.render.film_transparent = False
    scene.world = bpy.data.worlds.new("WORLD-Aypate")
    scene.world.use_nodes = True
    background = next(n for n in scene.world.node_tree.nodes if n.type == "BACKGROUND")
    background.inputs["Color"].default_value = (0.18, 0.23, 0.25, 1.0)
    background.inputs["Strength"].default_value = 0.7
    scene.view_settings.look = "AgX - Medium High Contrast"
    return scene


def collection(name):
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(col)
    return col


def unlink_all(obj):
    for col in list(obj.users_collection):
        col.objects.unlink(obj)


def bucket(name):
    return collection(f"COL-Aypate_{name}")


def fbm(size, cells, seed, octaves=4):
    rng = np.random.default_rng(seed)
    total = np.zeros((size, size), dtype=np.float32)
    amplitude = 1.0
    normal = 0.0
    current = cells
    for _ in range(octaves):
        grid = rng.random((current + 1, current + 1), dtype=np.float32)
        x = np.linspace(0, current, size, endpoint=False, dtype=np.float32)
        y = np.linspace(0, current, size, endpoint=False, dtype=np.float32)
        x0 = x.astype(np.int32)
        y0 = y.astype(np.int32)
        fx = x - x0
        fy = y - y0
        g00 = grid[np.ix_(x0, y0)]
        g10 = grid[np.ix_(x0 + 1, y0)]
        g01 = grid[np.ix_(x0, y0 + 1)]
        g11 = grid[np.ix_(x0 + 1, y0 + 1)]
        sx = fx[:, None]
        sy = fy[None, :]
        top = g00 * (1 - sx) + g10 * sx
        bottom = g01 * (1 - sx) + g11 * sx
        total += amplitude * (top * (1 - sy) + bottom * sy)
        normal += amplitude
        amplitude *= 0.5
        current *= 2
    total /= normal
    total -= total.min()
    total /= max(total.max(), 1e-6)
    return total


def image(name, rgb, non_color=False):
    height, width = rgb.shape[:2]
    rgba = np.ones((height, width, 4), dtype=np.float32)
    rgba[:, :, :3] = np.clip(rgb, 0, 1)
    img = bpy.data.images.new(name, width=width, height=height, alpha=False, float_buffer=False)
    img.colorspace_settings.name = "Non-Color" if non_color else "sRGB"
    img.pixels.foreach_set(rgba.ravel())
    img.update()
    img.pack()
    return img


def texture_set(name, seed, base, accent, kind="stone", size=SIZE):
    height = fbm(size, 4, seed)
    detail = fbm(size, 16, seed + 11, 3)
    if kind == "stone":
        h = 0.35 + 0.5 * height + 0.15 * detail
        rgb = np.stack(
            [
                base[0] + (accent[0] - base[0]) * h,
                base[1] + (accent[1] - base[1]) * h,
                base[2] + (accent[2] - base[2]) * h,
            ],
            axis=-1,
        )
        cracks = (np.abs(np.sin((np.arange(size)[None, :] + np.arange(size)[:, None] * 0.7) * 0.22)) < 0.025)
        rgb[cracks] *= 0.56
    elif kind == "ground":
        h = 0.25 + 0.65 * height + 0.1 * detail
        rgb = np.stack(
            [
                0.24 + 0.16 * h,
                0.21 + 0.23 * h,
                0.13 + 0.10 * h,
            ],
            axis=-1,
        )
        green = np.clip((detail - 0.48) * 2.2, 0, 1)
        rgb[:, :, 0] *= 1 - 0.18 * green
        rgb[:, :, 1] += 0.075 * green
        rgb[:, :, 2] *= 1 - 0.12 * green
    elif kind == "moss":
        h = 0.3 + 0.6 * height
        rgb = np.stack([0.12 + 0.08 * h, 0.22 + 0.23 * h, 0.10 + 0.10 * h], axis=-1)
    else:
        rgb = np.stack([0.18 + 0.18 * height, 0.19 + 0.18 * height, 0.13 + 0.12 * height], axis=-1)
    rgb = np.clip(rgb, 0, 1)
    diffuse = image(f"IMG-Aypate_{name}_diffuse", rgb)
    rough = image(f"IMG-Aypate_{name}_roughness", np.clip(0.7 + 0.25 * detail, 0, 1)[:, :, None].repeat(3, axis=2), True)
    gy, gx = np.gradient(height)
    nx = -gx * 7.0
    ny = -gy * 7.0
    nz = np.ones_like(height)
    length = np.sqrt(nx * nx + ny * ny + nz * nz)
    normal = np.stack([(nx / length) * 0.5 + 0.5, (ny / length) * 0.5 + 0.5, (nz / length) * 0.5 + 0.5], axis=-1)
    normal_img = image(f"IMG-Aypate_{name}_normal", normal, True)
    return diffuse, rough, normal_img


def material(name, diffuse=None, roughness=None, normal=None, color=(0.4, 0.38, 0.33, 1), roughness_value=0.88):
    mat = bpy.data.materials.get(name)
    if mat is not None:
        return mat
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = next(n for n in nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Roughness"].default_value = roughness_value
    mat.diffuse_color = color
    if diffuse is not None:
        tex = nodes.new("ShaderNodeTexImage")
        tex.name = "Diffuse"
        tex.image = diffuse
        tex.location = (-620, 260)
        links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    if roughness is not None:
        tex = nodes.new("ShaderNodeTexImage")
        tex.name = "Roughness"
        tex.image = roughness
        tex.location = (-620, 0)
        links.new(tex.outputs["Color"], bsdf.inputs["Roughness"])
    if normal is not None:
        tex = nodes.new("ShaderNodeTexImage")
        tex.name = "Normal"
        tex.image = normal
        tex.location = (-620, -260)
        nmap = nodes.new("ShaderNodeNormalMap")
        nmap.name = "NormalMap"
        nmap.location = (-320, -260)
        nmap.inputs["Strength"].default_value = 0.8
        links.new(tex.outputs["Color"], nmap.inputs["Color"])
        links.new(nmap.outputs["Normal"], bsdf.inputs["Normal"])
    return mat


def make_materials():
    stone = texture_set("Stone", SEED, (0.30, 0.29, 0.25), (0.58, 0.54, 0.45), "stone")
    ground = texture_set("Ground", SEED + 20, (0.2, 0.17, 0.11), (0.45, 0.39, 0.26), "ground")
    moss = texture_set("Moss", SEED + 40, (0.10, 0.18, 0.06), (0.30, 0.42, 0.16), "moss")
    stone_dark = texture_set("StoneDark", SEED + 60, (0.16, 0.16, 0.14), (0.38, 0.36, 0.31), "stone")
    return {
        "stone": material("MAT-Aypate_Stone", *stone),
        "stone_dark": material("MAT-Aypate_StoneDark", *stone_dark),
        "ground": material("MAT-Aypate_Ground", *ground),
        "moss": material("MAT-Aypate_Moss", *moss),
        "water": material("MAT-Aypate_Water", color=(0.07, 0.20, 0.24, 1), roughness_value=0.18),
        "wood": material("MAT-Aypate_Wood", color=(0.20, 0.12, 0.07, 1), roughness_value=0.82),
        "leaf": material("MAT-Aypate_Leaf", color=(0.10, 0.22, 0.09, 1), roughness_value=0.9),
        "leaf_dark": material("MAT-Aypate_LeafDark", color=(0.05, 0.13, 0.055, 1), roughness_value=0.92),
        "cloud": material("MAT-Aypate_Cloud", color=(0.68, 0.72, 0.70, 1), roughness_value=1.0),
    }


def add_to(obj, col):
    unlink_all(obj)
    col.objects.link(obj)


def apply_scale(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.select_set(False)


def uv_cube(obj, cube_size=4.0):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.cube_project(cube_size=cube_size)
    bpy.ops.object.mode_set(mode="OBJECT")
    obj.select_set(False)


def bevel(obj, width=0.035):
    if width <= 0:
        return
    mod = obj.modifiers.new("Bevel", "BEVEL")
    mod.width = width
    mod.segments = 1
    mod.limit_method = "ANGLE"
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.modifier_apply(modifier=mod.name)
    obj.select_set(False)


def box(name, size, location, mat, layer="city", uv=4.0, bevel_width=0.035, lod1_exclude=False):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.data.name = f"MESH-{name}"
    obj.dimensions = size
    apply_scale(obj)
    obj.data.materials.append(mat)
    if uv:
        uv_cube(obj, uv)
    bevel(obj, bevel_width)
    obj["layer"] = layer
    obj["lod1_exclude"] = bool(lod1_exclude)
    add_to(obj, bucket(layer.title()))
    return obj


def cylinder(name, radius, depth, location, mat, layer="props", vertices=12, lod1_exclude=False):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.data.name = f"MESH-{name}"
    obj.data.materials.append(mat)
    obj["layer"] = layer
    obj["lod1_exclude"] = bool(lod1_exclude)
    add_to(obj, bucket(layer.title()))
    return obj


def wall_x(name, x0, x1, y, z0, height, thickness, mat, openings=(), layer="city", lod1_exclude=False):
    cursor = x0
    index = 0
    for center, width in sorted(openings):
        left = center - width / 2
        if left > cursor:
            box(f"{name}_{index}", (left - cursor, thickness, height), ((cursor + left) / 2, y, z0 + height / 2), mat, layer, 4.0, 0.025, lod1_exclude)
            index += 1
        cursor = center + width / 2
    if cursor < x1:
        box(f"{name}_{index}", (x1 - cursor, thickness, height), ((cursor + x1) / 2, y, z0 + height / 2), mat, layer, 4.0, 0.025, lod1_exclude)
    for center, width in openings:
        box(f"{name}_lintel_{int(center)}", (width + 0.15, thickness + 0.05, 0.45), (center, y, z0 + height - 0.22), mat, layer, 4.0, 0.02, lod1_exclude)


def wall_y(name, x, y0, y1, z0, height, thickness, mat, openings=(), layer="city", lod1_exclude=False):
    cursor = y0
    index = 0
    for center, width in sorted(openings):
        left = center - width / 2
        if left > cursor:
            box(f"{name}_{index}", (thickness, left - cursor, height), (x, (cursor + left) / 2, z0 + height / 2), mat, layer, 4.0, 0.025, lod1_exclude)
            index += 1
        cursor = center + width / 2
    if cursor < y1:
        box(f"{name}_{index}", (thickness, y1 - cursor, height), (x, (cursor + y1) / 2, z0 + height / 2), mat, layer, 4.0, 0.025, lod1_exclude)


def stairs(name, start, width, run, rise, steps, axis="x", mat=None, layer="city"):
    for i in range(steps):
        height = rise * (i + 1)
        x = start[0] + (run * (i + 0.5) if axis == "x" else 0)
        y = start[1] + (run * (i + 0.5) if axis == "y" else 0)
        box(f"{name}_{i}", (run if axis == "x" else width, width if axis == "x" else run, height), (x, y, start[2] + height / 2), mat, layer, 3.0, 0.015)


def mountain(name, x, y, radius, height, mat, scale_y=1.0, lod1_exclude=False):
    bpy.ops.mesh.primitive_cone_add(vertices=9, radius1=radius, radius2=radius * 0.08, depth=height, location=(x, y, height / 2 - 8))
    obj = bpy.context.object
    obj.name = name
    obj.data.name = f"MESH-{name}"
    obj.scale.y = scale_y
    apply_scale(obj)
    obj.data.materials.append(mat)
    obj["layer"] = "terrain"
    obj["lod1_exclude"] = bool(lod1_exclude)
    add_to(obj, bucket("Terrain"))
    return obj


def tree(name, x, y, z, scale, mats, lod1_exclude=False):
    parts = []
    trunk_h = 4.0 * scale
    bpy.ops.mesh.primitive_cylinder_add(vertices=7, radius=0.22 * scale, depth=trunk_h, location=(x, y, z + trunk_h / 2))
    trunk = bpy.context.object
    trunk.name = f"{name}_trunk"
    trunk.data.materials.append(mats["wood"])
    parts.append(trunk)
    for i, (dx, dy, dz, rad) in enumerate(((0, 0, trunk_h + 1.7 * scale, 2.6 * scale), (-1.3, 0.7, trunk_h + 1.2 * scale, 1.9 * scale), (1.2, -0.5, trunk_h + 1.3 * scale, 1.8 * scale))):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=rad, location=(x + dx * scale, y + dy * scale, z + dz))
        leaf = bpy.context.object
        leaf.name = f"{name}_leaf{i}"
        leaf.data.materials.append(mats["leaf"] if i % 2 == 0 else mats["leaf_dark"])
        parts.append(leaf)
    bpy.ops.object.select_all(action="DESELECT")
    for part in parts:
        part.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    obj = bpy.context.object
    obj.name = name
    obj.data.name = f"MESH-{name}"
    obj["layer"] = "props"
    obj["lod1_exclude"] = lod1_exclude
    add_to(obj, bucket("Props"))


def human(name, x, y, z, mats):
    body = cylinder(f"{name}_body", 0.18, 1.15, (x, y, z + 0.58), mats["ground"], "reference", 8)
    head = bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.13, location=(x, y, z + 1.34))
    head_obj = bpy.context.object
    head_obj.name = f"{name}_head"
    head_obj.data.materials.append(mats["stone"])
    add_to(head_obj, bucket("Reference"))
    for obj in (body, head_obj):
        obj["layer"] = "reference"


def terrain(mats):
    size = 700
    n = 110
    verts = []
    faces = []
    for j in range(n + 1):
        for i in range(n + 1):
            x = -size / 2 + size * i / n
            y = -size / 2 + size * j / n
            dx = max(0, abs(x) - 140)
            dy = max(0, abs(y + 20) - 100)
            d = math.hypot(dx, dy)
            plateau = 1.0 if d <= 0 else max(0.0, 1.0 - d / 170)
            z = PLAZA_Z - 6.0 * (1 - plateau) + 0.8 * math.sin(x * 0.026) * math.cos(y * 0.021)
            z += 38 * math.exp(-(((x - 300) / 110) ** 2 + ((y + 30) / 190) ** 2))
            z += 30 * math.exp(-(((x + 310) / 120) ** 2 + ((y - 40) / 180) ** 2))
            z += 44 * math.exp(-(((x + 30) / 190) ** 2 + ((y + 305) / 115) ** 2))
            z += 22 * math.exp(-(((x - 20) / 160) ** 2 + ((y - 310) / 120) ** 2))
            verts.append((x, y, z))
    for j in range(n):
        for i in range(n):
            a = j * (n + 1) + i
            faces.append((a, a + 1, a + n + 2, a + n + 1))
    mesh = bpy.data.meshes.new("MESH-Aypate_Terrain")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new("GEO-Aypate_Terrain", mesh)
    bucket("Terrain").objects.link(obj)
    obj.data.materials.append(mats["ground"])
    uv = mesh.uv_layers.new(name="UVMap")
    for poly in mesh.polygons:
        for loop in poly.loop_indices:
            co = mesh.vertices[mesh.loops[loop].vertex_index].co
            uv.data[loop].uv = ((co.x + size / 2) / 18.0, (co.y + size / 2) / 18.0)
    obj["layer"] = "terrain"
    return obj


def main():
    scene = clean_scene()
    for name in ("City", "Terrain", "Props", "Reference", "Later"):
        bucket(name)
    mats = make_materials()
    terrain(mats)

    # Plaza Inca and Qhapaq Ñan.
    box("GEO-Aypate_Plaza", (120, 90, 0.35), (0, 0, PLAZA_Z + 0.1), mats["stone"], "city", 8.0, 0.02)
    box("GEO-Aypate_Plaza_Parapet_S", (120, 1.0, 0.55), (0, 45, PLAZA_Z + 0.3), mats["stone_dark"], "city", 8.0, 0.02)
    box("GEO-Aypate_Plaza_Parapet_N", (120, 1.0, 0.55), (0, -45, PLAZA_Z + 0.3), mats["stone_dark"], "city", 8.0, 0.02)
    box("GEO-Aypate_QhapaqNan", (8, 150, 0.18), (0, 118, PLAZA_Z + 0.02), mats["stone_dark"], "city", 8.0, 0.02)
    box("GEO-Aypate_QhapaqNan_Alt", (6, 95, 0.16), (92, 105, PLAZA_Z + 0.01), mats["stone_dark"], "city", 8.0, 0.02)
    for i in range(18):
        box(f"GEO-Aypate_Path_Stone_{i}", (8, 2.0, 0.10), (0, 48 + i * 8, PLAZA_Z + 0.12), mats["stone"], "props", 2.0, 0.01, True)

    # Ushnu: three stepped platforms.
    box("GEO-Aypate_Ushnu_Base", (26, 26, 1.4), (-47, -10, PLAZA_Z + 0.7), mats["stone"], "city", 6.0, 0.04)
    box("GEO-Aypate_Ushnu_Tier1", (21, 21, 1.2), (-47, -10, PLAZA_Z + 2.0), mats["stone"], "city", 6.0, 0.035)
    box("GEO-Aypate_Ushnu_Tier2", (15, 15, 1.2), (-47, -10, PLAZA_Z + 3.2), mats["stone"], "city", 6.0, 0.03)
    box("GEO-Aypate_Ushnu_Top", (9, 9, 1.0), (-47, -10, PLAZA_Z + 4.3), mats["stone_dark"], "city", 5.0, 0.03)
    stairs("GEO-Aypate_Ushnu_Stairs", (-34, -10, PLAZA_Z + 0.1), 5.0, 1.4, 0.28, 5, "x", mats["stone"])
    box("GEO-Aypate_Ushnu_Seat", (3.8, 3.8, 0.65), (-47, -10, PLAZA_Z + 5.05), mats["stone_dark"], "props", 2.0, 0.02)

    # Kallanka: long roofless hall with 13 entrances.
    box("GEO-Aypate_Kallanka_Platform", (102, 16, 0.7), (0, -52, PLAZA_Z + 0.35), mats["stone"], "city", 8.0, 0.03)
    wall_x("GEO-Aypate_Kallanka_Front", -51, 51, -44.5, PLAZA_Z + 0.7, 3.0, 0.9, mats["stone"], [(i * 4, 1.4) for i in range(-6, 7)], "city")
    wall_x("GEO-Aypate_Kallanka_Back", -51, 51, -59.5, PLAZA_Z + 0.7, 3.0, 0.9, mats["stone"], layer="city")
    wall_y("GEO-Aypate_Kallanka_W", -51, -59.5, -44.5, PLAZA_Z + 0.7, 3.0, 0.9, mats["stone"], layer="city")
    wall_y("GEO-Aypate_Kallanka_E", 51, -59.5, -44.5, PLAZA_Z + 0.7, 3.0, 0.9, mats["stone"], layer="city")
    for i in range(-6, 7):
        box(f"GEO-Aypate_Kallanka_Step_{i}", (2.2, 1.8, 0.22), (i * 4, -41.8, PLAZA_Z + 0.15), mats["stone"], "props", 2.0, 0.01, True)

    # Acllawasi: enclosure with a patio and a monumental gate.
    box("GEO-Aypate_Acllawasi_Platform", (48, 36, 0.55), (66, -8, PLAZA_Z + 0.28), mats["stone"], "city", 7.0, 0.03)
    wall_y("GEO-Aypate_Acllawasi_W", 42, -26, 10, PLAZA_Z + 0.55, 3.1, 1.0, mats["stone"], [(0, 4.0)], "city")
    wall_y("GEO-Aypate_Acllawasi_E", 90, -26, 10, PLAZA_Z + 0.55, 3.1, 1.0, mats["stone"], layer="city")
    wall_x("GEO-Aypate_Acllawasi_N", 42, 90, -26, PLAZA_Z + 0.55, 3.1, 1.0, mats["stone"], layer="city")
    wall_x("GEO-Aypate_Acllawasi_S", 42, 90, 10, PLAZA_Z + 0.55, 3.1, 1.0, mats["stone"], layer="city")
    box("GEO-Aypate_Acllawasi_Patio", (30, 20, 0.12), (66, -8, PLAZA_Z + 0.62), mats["moss"], "props", 6.0, 0.01, True)
    for i, (x, y) in enumerate(((55, -18), (76, -18), (55, 2), (76, 2))):
        box(f"GEO-Aypate_Acllawasi_Room_{i}", (10, 8, 2.2), (x, y, PLAZA_Z + 1.65), mats["stone"], "city", 4.0, 0.025)
    # Portada: two jambs and a lintel at the west gate.
    for i, y in enumerate((-2.2, 2.2)):
        box(f"GEO-Aypate_Acllawasi_Jamb_{i}", (1.0, 1.2, 3.2), (42, y, PLAZA_Z + 2.15), mats["stone_dark"], "props", 2.0, 0.03)
    box("GEO-Aypate_Acllawasi_Lintel", (1.4, 5.8, 0.7), (42, 0, PLAZA_Z + 4.0), mats["stone_dark"], "props", 2.0, 0.03)

    # Palace behind the kallanka, secondary.
    for i in range(3):
        box(f"GEO-Aypate_Palace_Room_{i}", (14, 8, 2.1), (-18 + i * 18, -72, PLAZA_Z + 1.6), mats["stone"], "city", 4.0, 0.02)
    box("GEO-Aypate_Palace_Patio", (44, 12, 0.2), (0, -62, PLAZA_Z + 0.2), mats["moss"], "props", 5.0, 0.01, True)

    # Colcas near the entrance.
    for i in range(3):
        box(f"GEO-Aypate_Colca_{i}", (26, 6, 2.4), (-66, 82 + i * 9, PLAZA_Z + 1.25), mats["stone"], "city", 4.0, 0.02)
    # Control kancha on the path.
    wall_x("GEO-Aypate_Control_N", -12, 12, 110, PLAZA_Z + 0.1, 2.1, 0.7, mats["stone"], [(-12, 1.8), (12, 1.8)], "city")
    wall_x("GEO-Aypate_Control_S", -12, 12, 98, PLAZA_Z + 0.1, 2.1, 0.7, mats["stone"], [(-12, 1.8), (12, 1.8)], "city")
    wall_y("GEO-Aypate_Control_W", -12, 98, 110, PLAZA_Z + 0.1, 2.1, 0.7, mats["stone"], layer="city")
    wall_y("GEO-Aypate_Control_E", 12, 98, 110, PLAZA_Z + 0.1, 2.1, 0.7, mats["stone"], layer="city")

    # Sunken ritual fountain.
    box("GEO-Aypate_Fountain_Floor", (8, 6, 0.25), (-58, 48, PLAZA_Z - 0.45), mats["stone_dark"], "city", 3.0, 0.02)
    for name, size, loc in (
        ("N", (8, 0.8, 1.2), (-58, 51, PLAZA_Z + 0.1)),
        ("S", (8, 0.8, 1.2), (-58, 45, PLAZA_Z + 0.1)),
        ("W", (0.8, 6, 1.2), (-62, 48, PLAZA_Z + 0.1)),
        ("E", (0.8, 6, 1.2), (-54, 48, PLAZA_Z + 0.1)),
    ):
        box(f"GEO-Aypate_Fountain_Wall_{name}", size, loc, mats["stone"], "city", 3.0, 0.02)
    box("GEO-Aypate_Fountain_Water", (6.6, 4.6, 0.08), (-58, 48, PLAZA_Z - 0.25), mats["water"], "props", 0, 0.0)
    for i in range(3):
        box(f"GEO-Aypate_Fountain_Niche_{i}", (0.35, 0.9, 0.55), (-62.25, 46.5 + i * 1.5, PLAZA_Z + 0.35), mats["stone_dark"], "props", 1.0, 0.005, True)

    # Agricultural terraces on the west slope.
    for i in range(5):
        z = PLAZA_Z - 1.2 - i * 1.25
        x = -145 - i * 18
        box(f"GEO-Aypate_Terrace_{i}", (8, 120, 1.15), (x, 10, z), mats["stone"], "terrain", 5.0, 0.02)
        box(f"GEO-Aypate_Terrace_Soil_{i}", (22, 120, 0.25), (x - 14, 10, z + 0.35), mats["moss"], "terrain", 6.0, 0.01, True)

    # Cloud forest and rocks; deterministic placement.
    rng = random.Random(SEED)
    for i in range(92):
        angle = rng.uniform(0, math.tau)
        radius = rng.uniform(160, 300)
        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        if abs(x) < 145 and abs(y + 10) < 110:
            continue
        z = terrain_height(x, y)
        tree(f"GEO-Aypate_Tree_{i}", x, y, z, rng.uniform(0.75, 1.35), mats, lod1_exclude=(i % 2 == 1))
    for i in range(54):
        angle = rng.uniform(0, math.tau)
        radius = rng.uniform(105, 175)
        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        if abs(x) < 82 and abs(y + 12) < 76:
            continue
        z = terrain_height(x, y)
        tree(f"GEO-Aypate_Forest_{i}", x, y, z, rng.uniform(0.65, 1.1), mats, lod1_exclude=(i % 3 == 0))
    for i in range(55):
        angle = rng.uniform(0, math.tau)
        radius = rng.uniform(130, 310)
        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        z = terrain_height(x, y)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=rng.uniform(0.45, 1.4), location=(x, y, z + 0.3))
        rock = bpy.context.object
        rock.name = f"GEO-Aypate_Rock_{i}"
        rock.scale.z = rng.uniform(0.35, 0.75)
        rock.data.materials.append(mats["stone_dark"] if i % 3 else mats["moss"])
        rock["layer"] = "props"
        rock["lod1_exclude"] = i % 2 == 0
        add_to(rock, bucket("Props"))
    for i in range(28):
        x = rng.uniform(-110, 110)
        y = rng.uniform(-35, 30)
        if abs(x) < 35 and abs(y) < 35:
            continue
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=rng.uniform(0.3, 0.8), location=(x, y, PLAZA_Z + 0.4))
        shrub = bpy.context.object
        shrub.name = f"GEO-Aypate_Shrub_{i}"
        shrub.scale.z = rng.uniform(0.35, 0.7)
        shrub.data.materials.append(mats["leaf_dark"] if i % 2 else mats["leaf"])
        shrub["layer"] = "props"
        shrub["lod1_exclude"] = True
        add_to(shrub, bucket("Props"))

    # Small human references.
    human("GEO-Aypate_Human_1", 12, 8, PLAZA_Z + 0.15, mats)
    human("GEO-Aypate_Human_2", -15, -2, PLAZA_Z + 0.15, mats)

    # Lighting.
    sun_data = bpy.data.lights.new("LGT-Aypate_Sun", "SUN")
    sun_data.energy = 3.2
    sun_data.angle = math.radians(8)
    sun_data.color = (1.0, 0.91, 0.78)
    sun = bpy.data.objects.new("LGT-Aypate_Sun", sun_data)
    scene.collection.objects.link(sun)
    sun.rotation_euler = (math.radians(38), math.radians(-22), math.radians(-42))
    fill_data = bpy.data.lights.new("LGT-Aypate_Fill", "AREA")
    fill_data.energy = 480
    fill_data.shape = "DISK"
    fill_data.size = 80
    fill_data.color = (0.62, 0.76, 0.88)
    fill = bpy.data.objects.new("LGT-Aypate_Fill", fill_data)
    scene.collection.objects.link(fill)
    fill.location = (60, -90, 70)
    fill.rotation_euler = (Vector((0, 0, 6)) - fill.location).to_track_quat("-Z", "Y").to_euler()

    # Cameras.
    camera_defs = {
        "Hero": ((86, 112, 42), (0, -4, 8), 40),
        "Tour1": ((25, 165, 38), (0, 65, 7), 42),
        "Tour2": ((70, 85, 38), (0, 0, 6), 40),
        "Tour3": ((-78, 32, 27), (-47, -10, 6), 42),
        "Tour4": ((58, -72, 26), (0, -50, 6), 40),
        "Tour5": ((92, 32, 25), (62, -8, 5), 42),
        "Tour6": ((-55, 85, 35), (-58, 48, 5), 38),
    }
    for name, (pos, target, lens) in camera_defs.items():
        cam_data = bpy.data.cameras.new(f"CAM-Aypate_{name}")
        cam_data.lens = lens
        cam = bpy.data.objects.new(f"CAM-Aypate_{name}", cam_data)
        scene.collection.objects.link(cam)
        cam.location = pos
        cam.rotation_euler = (Vector(target) - cam.location).to_track_quat("-Z", "Y").to_euler()
    scene.camera = bpy.data.objects["CAM-Aypate_Hero"]
    scene.render.filepath = HERO
    bpy.ops.render.render(write_still=True)

    os.makedirs(os.path.dirname(OUT_BLEND), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
    for name in ("City", "Terrain", "Props", "Reference"):
        col = bpy.data.collections.get(f"COL-Aypate_{name}")
        count = sum(len(o.data.loop_triangles) for o in col.objects if o.type == "MESH") if col else 0
        print(f"AYPATE_{name.upper()}_TRIS {count}")
    print("AYPATE_BLOCKOUT_OK", OUT_BLEND, HERO)


def terrain_height(x, y):
    dx = max(0, abs(x) - 140)
    dy = max(0, abs(y + 20) - 100)
    d = math.hypot(dx, dy)
    plateau = 1.0 if d <= 0 else max(0.0, 1.0 - d / 170)
    z = PLAZA_Z - 6.0 * (1 - plateau) + 0.8 * math.sin(x * 0.026) * math.cos(y * 0.021)
    z += 38 * math.exp(-(((x - 300) / 110) ** 2 + ((y + 30) / 190) ** 2))
    z += 30 * math.exp(-(((x + 310) / 120) ** 2 + ((y - 40) / 180) ** 2))
    z += 44 * math.exp(-(((x + 30) / 190) ** 2 + ((y + 305) / 115) ** 2))
    z += 22 * math.exp(-(((x - 20) / 160) ** 2 + ((y - 310) / 120) ** 2))
    return z


if __name__ == "__main__":
    main()
