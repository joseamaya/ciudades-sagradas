"""Genera el preview v0.1 de Nik An (Chan Chan) como escena Blender.

Uso:
  blender --background --python scripts/chan-chan/build_chanchan_highpoly.py

La planta es una lectura de conjunto de Nik An: plaza principal de 65 x 75 m,
corredor de peces y aves, altarcillo, audiencias, segunda plaza, depósitos,
reservorio y plataforma funeraria. Las murallas y los relieves son
interpretaciones geométricas; no se copian planos ni imágenes oficiales.
"""

import json
import math
import os
import random
import sys

import bpy
import bmesh
from mathutils import Vector

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "scripts", "aypate"))
import build_aypate_blockout as base  # noqa: E402

OUT_BLEND = os.path.join(ROOT, "blender", "chan-chan", "chanchan_highpoly_v0.1.blend")
HERO = os.path.join(ROOT, "public", "cities", "chan-chan", "hero.jpg")
PREVIEW = "/tmp/chanchan_highpoly_v0.1.jpg"
SEED = 4217
TERRAIN_SIZE = 900
TERRAIN_N = 170
rng = random.Random(SEED)


def scene_collections(scene):
    for name in ("City", "Terrain", "Props", "Reference"):
        col = bpy.data.collections.new(f"COL-ChanChan_{name}")
        scene.collection.children.link(col)
    base.bucket = lambda name: bpy.data.collections[f"COL-ChanChan_{name}"]


def terrain_height(x, y):
    z = -1.2
    z += 0.55 * math.sin(x * 0.018) * math.cos(y * 0.015)
    z += 0.25 * math.sin((x + y) * 0.035)
    d = math.hypot(x, y)
    if d > 260:
        z += 0.018 * (d - 260)
    return z


def terrain(mats):
    n = TERRAIN_N
    size = TERRAIN_SIZE
    verts = []
    faces = []
    for j in range(n + 1):
        for i in range(n + 1):
            x = -size / 2 + size * i / n
            y = -size / 2 + size * j / n
            verts.append((x, y, terrain_height(x, y)))
    for j in range(n):
        for i in range(n):
            a = j * (n + 1) + i
            faces.append((a, a + 1, a + n + 2, a + n + 1))
    mesh = bpy.data.meshes.new("MESH-ChanChan_Terrain")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new("GEO-ChanChan_Terrain", mesh)
    base.bucket("Terrain").objects.link(obj)
    obj.data.materials.append(mats["sand"])
    uv = mesh.uv_layers.new(name="UVMap")
    for poly in mesh.polygons:
        for loop in poly.loop_indices:
            co = mesh.vertices[mesh.loops[loop].vertex_index].co
            uv.data[loop].uv = ((co.x + size / 2) / 22.0, (co.y + size / 2) / 22.0)
    obj["layer"] = "terrain"
    return obj


def make_materials():
    adobe = base.texture_set("Adobe", SEED, (0.43, 0.27, 0.17), (0.68, 0.48, 0.30), "stone", 2048)
    adobe_dark = base.texture_set("AdobeDark", SEED + 7, (0.38, 0.24, 0.15), (0.58, 0.40, 0.25), "stone", 1024)
    sand = base.texture_set("Sand", SEED + 20, (0.50, 0.39, 0.25), (0.72, 0.58, 0.39), "stone", 2048)
    stone = base.texture_set("Stone", SEED + 40, (0.30, 0.27, 0.22), (0.52, 0.47, 0.39), "stone", 2048)
    water = base.material("MAT-ChanChan_Water", color=(0.05, 0.19, 0.22, 1.0), roughness_value=0.22)
    wood = base.material("MAT-ChanChan_Wood", color=(0.16, 0.10, 0.055, 1.0), roughness_value=0.9)
    leaf = base.material("MAT-ChanChan_Leaf", color=(0.11, 0.20, 0.07, 1.0), roughness_value=0.92)
    leaf_dark = base.material("MAT-ChanChan_LeafDark", color=(0.055, 0.12, 0.04, 1.0), roughness_value=0.94)
    return {
        "adobe": base.material("MAT-ChanChan_Adobe", *adobe),
        "adobe_dark": base.material("MAT-ChanChan_AdobeDark", *adobe_dark),
        "sand": base.material("MAT-ChanChan_Sand", *sand),
        "stone": base.material("MAT-ChanChan_Stone", *stone),
        "water": water,
        "wood": wood,
        "leaf": leaf,
        "leaf_dark": leaf_dark,
    }


def mesh_obj(name, verts, faces, mat, layer="city"):
    mesh = bpy.data.meshes.new(f"MESH-{name}")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    base.bucket(layer.title()).objects.link(obj)
    obj.data.materials.append(mat)
    obj["layer"] = layer
    obj["lod1_exclude"] = False
    base.uv_cube(obj, 3.0)
    base.bevel(obj, 0.03)
    return obj


def tapered_wall(name, cx, cy, length, height, base_t, top_t, axis, z0, mat, layer="city"):
    half = length / 2.0
    b2 = base_t / 2.0
    t2 = top_t / 2.0
    if axis == "x":
        verts = [
            (cx - half, cy - b2, z0), (cx + half, cy - b2, z0),
            (cx + half, cy + b2, z0), (cx - half, cy + b2, z0),
            (cx - half, cy - t2, z0 + height), (cx + half, cy - t2, z0 + height),
            (cx + half, cy + t2, z0 + height), (cx - half, cy + t2, z0 + height),
        ]
    else:
        verts = [
            (cx - b2, cy - half, z0), (cx + b2, cy - half, z0),
            (cx + b2, cy + half, z0), (cx - b2, cy + half, z0),
            (cx - t2, cy - half, z0 + height), (cx + t2, cy - half, z0 + height),
            (cx + t2, cy + half, z0 + height), (cx - t2, cy + half, z0 + height),
        ]
    faces = [
        (0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
        (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7),
    ]
    return mesh_obj(name, verts, faces, mat, layer)


def box_face(verts, faces, mats, center, size, material_index):
    x, y, z = center
    sx, sy, sz = (v / 2 for v in size)
    n = len(verts)
    verts.extend([
        (x - sx, y - sy, z - sz), (x + sx, y - sy, z - sz),
        (x + sx, y + sy, z - sz), (x - sx, y + sy, z - sz),
        (x - sx, y - sy, z + sz), (x + sx, y - sy, z + sz),
        (x + sx, y + sy, z + sz), (x - sx, y + sy, z + sz),
    ])
    faces.extend([
        (n, n + 1, n + 5, n + 4), (n + 1, n + 2, n + 6, n + 5),
        (n + 2, n + 3, n + 7, n + 6), (n + 3, n, n + 4, n + 7),
        (n + 4, n + 5, n + 6, n + 7), (n, n + 3, n + 2, n + 1),
    ])
    mats.extend([material_index] * 6)


def adobe_courses(obj, mat_a, mat_b, max_blocks=1200):
    if obj.type != "MESH":
        return 0
    dx, dy, dz = obj.dimensions
    loc = obj.location
    x0, x1 = loc.x - dx / 2, loc.x + dx / 2
    y0, y1 = loc.y - dy / 2, loc.y + dy / 2
    z0, z1 = loc.z - dz / 2, loc.z + dz / 2
    verts, faces, indices = [], [], []
    blocks = 0
    if dx >= dy:
        for y_face, sign in ((y0, -1), (y1, 1)):
            rows = max(1, int(dz / 0.42))
            cols = max(1, int(dx / 1.55))
            for row in range(rows):
                h = dz / rows
                z = z0 + (row + 0.5) * h
                offset = (row % 2) * (dx / cols) * 0.5
                for col in range(cols):
                    if blocks >= max_blocks:
                        break
                    w = dx / cols * rng.uniform(0.82, 0.98)
                    x = x0 + offset + (col + 0.5) * (dx / cols)
                    if x - w / 2 < x0 or x + w / 2 > x1:
                        continue
                    yy = y_face + sign * 0.055
                    box_face(verts, faces, indices, (x, yy, z), (w, 0.10, h * 0.80), 0 if rng.random() < 0.72 else 1)
                    blocks += 1
    else:
        for x_face, sign in ((x0, -1), (x1, 1)):
            rows = max(1, int(dz / 0.42))
            cols = max(1, int(dy / 1.55))
            for row in range(rows):
                h = dz / rows
                z = z0 + (row + 0.5) * h
                offset = (row % 2) * (dy / cols) * 0.5
                for col in range(cols):
                    if blocks >= max_blocks:
                        break
                    w = dy / cols * rng.uniform(0.82, 0.98)
                    y = y0 + offset + (col + 0.5) * (dy / cols)
                    if y - w / 2 < y0 or y + w / 2 > y1:
                        continue
                    xx = x_face + sign * 0.055
                    box_face(verts, faces, indices, (xx, y, z), (0.10, w, h * 0.80), 0 if rng.random() < 0.72 else 1)
                    blocks += 1
    if blocks:
        mesh = bpy.data.meshes.new(f"MESH-{obj.name}_Courses")
        mesh.from_pydata(verts, [], faces)
        mesh.update()
        mesh.materials.append(mat_a)
        mesh.materials.append(mat_b)
        for poly, index in zip(mesh.polygons, indices):
            poly.material_index = index
        courses = bpy.data.objects.new(f"GEO-{obj.name}_Courses", mesh)
        base.bucket("City").objects.link(courses)
        courses["layer"] = "city"
        courses["lod1_exclude"] = True
        base.uv_cube(courses, 2.2)
    return blocks


def diamond_prism(name, x, y, z, width, height, depth, mat, axis="x", layer="props"):
    hw, hh, hd = width / 2, height / 2, depth / 2
    if axis == "x":
        verts = [
            (x - hw, y - hd, z), (x, y - hd, z + hh), (x + hw, y - hd, z), (x, y - hd, z - hh),
            (x - hw, y + hd, z), (x, y + hd, z + hh), (x + hw, y + hd, z), (x, y + hd, z - hh),
        ]
    else:
        verts = [
            (x - hd, y - hw, z), (x - hd, y, z + hh), (x - hd, y + hw, z), (x - hd, y, z - hh),
            (x + hd, y - hw, z), (x + hd, y, z + hh), (x + hd, y + hw, z), (x + hd, y, z - hh),
        ]
    faces = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return mesh_obj(name, verts, faces, mat, layer)


def relief_panel(name, x0, x1, y, z0, mat, count=9, axis="x"):
    for i in range(count):
        x = x0 + (i + 0.5) * (x1 - x0) / count
        diamond_prism(f"{name}_Diamond_{i}", x, y, z0, 1.5, 2.1, 0.18, mat, axis, "props")
    for i in range(count - 1):
        x = x0 + (i + 1) * (x1 - x0) / count
        base.box(f"{name}_Step_{i}", (0.55, 0.22, 0.55), (x, y, z0), mat, "props", 1.5, 0.01, True)


def audiencia(name, x, y, z, scale=1.0, mats=None):
    w = 12.0 * scale
    d = 10.0 * scale
    h = 3.0 * scale
    t = 0.9 * scale
    base.box(f"{name}_Platform", (w, d, 0.55), (x, y, z + 0.27), mats["adobe_dark"], "city", 3.0, 0.02)
    base.box(f"{name}_Back", (w, t, h), (x, y + d / 2, z + 0.55 + h / 2), mats["adobe"], "city", 3.0, 0.02)
    base.box(f"{name}_Left", (t, d, h), (x - w / 2, y, z + 0.55 + h / 2), mats["adobe"], "city", 3.0, 0.02)
    base.box(f"{name}_Right", (t, d, h), (x + w / 2, y, z + 0.55 + h / 2), mats["adobe"], "city", 3.0, 0.02)
    for i in range(3):
        base.box(f"{name}_Niche_{i}", (0.9, 0.25, 1.2), (x - 3.4 + i * 3.4, y + d / 2 - 0.55, z + 1.6), mats["adobe_dark"], "props", 1.0, 0.01, True)
    base.box(f"{name}_Step", (2.4, 1.0, 0.5), (x, y - d / 2 - 0.5, z + 0.25), mats["adobe_dark"], "city", 2.0, 0.01)


def storeroom(name, x, y, z, mats, w=5.0, d=6.0):
    h = 2.6
    t = 0.55
    base.box(f"{name}_Floor", (w, d, 0.25), (x, y, z + 0.12), mats["adobe_dark"], "city", 2.0, 0.01)
    base.box(f"{name}_Back", (w, t, h), (x, y + d / 2, z + h / 2), mats["adobe"], "city", 2.0, 0.015)
    base.box(f"{name}_Left", (t, d, h), (x - w / 2, y, z + h / 2), mats["adobe"], "city", 2.0, 0.015)
    base.box(f"{name}_Right", (t, d, h), (x + w / 2, y, z + h / 2), mats["adobe"], "city", 2.0, 0.015)
    base.box(f"{name}_FrontL", (w / 2 - 0.8, t, h), (x - w / 4 - 0.4, y - d / 2, z + h / 2), mats["adobe"], "city", 2.0, 0.015)
    base.box(f"{name}_FrontR", (w / 2 - 0.8, t, h), (x + w / 4 + 0.4, y - d / 2, z + h / 2), mats["adobe"], "city", 2.0, 0.015)


def human(name, x, y, z, mats):
    base.cylinder(f"{name}_body", 0.16, 1.05, (x, y, z + 0.52), mats["adobe_dark"], "reference", 8)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.12, location=(x, y, z + 1.2))
    head = bpy.context.object
    head.name = f"{name}_head"
    head.data.materials.append(mats["stone"])
    base.add_to(head, base.bucket("Reference"))
    head["layer"] = "reference"


def main():
    scene = base.clean_scene()
    scene_collections(scene)
    mats = make_materials()
    terrain_obj = terrain(mats)

    site = 280
    wall_h = 9.0
    base_t = 5.0
    top_t = 1.4
    taper = tapered_wall
    perimeter = [
        ("N1", -73, 70, 134, wall_h, 140, "x"),
        ("N2", 73, 70, 134, wall_h, 140, "x"),
        ("S", 0, -120, 280, wall_h, 140, "x"),
        ("W", -140, 0, 240, wall_h, 120, "y"),
        ("E", 140, 0, 240, wall_h, 120, "y"),
    ]
    for name, x, y, length, h, z0, axis in perimeter:
        taper(f"GEO-ChanChan_Perimeter_{name}", x, y, length, h, base_t, top_t, axis, z0, mats["adobe"])
    base.box("GEO-ChanChan_Gate_W", (2.2, 6.0, 10.0), (-7, 70, 5.0), mats["adobe"], "city", 3.0, 0.02)
    base.box("GEO-ChanChan_Gate_E", (2.2, 6.0, 10.0), (7, 70, 5.0), mats["adobe"], "city", 3.0, 0.02)
    base.box("GEO-ChanChan_Processional_Path", (10, 55, 0.18), (0, 97.5, 0.09), mats["stone"], "props", 3.0, 0.01)
    for i, y in enumerate((80, 92, 104, 116)):
        base.box(f"GEO-ChanChan_Path_Bench_W_{i}", (1.2, 4.0, 0.45), (-7, y, 0.23), mats["adobe"], "props", 2.0, 0.01, True)
        base.box(f"GEO-ChanChan_Path_Bench_E_{i}", (1.2, 4.0, 0.45), (7, y, 0.23), mats["adobe"], "props", 2.0, 0.01, True)

    # Plaza principal de 65 x 75 m, con cuatro accesos.
    plaza_cx, plaza_cy = 0, 88
    pw, pd = 65, 75
    base.box("GEO-ChanChan_Plaza_Main_Floor", (pw, pd, 0.35), (plaza_cx, plaza_cy, 0.18), mats["sand"], "city", 4.0, 0.01)
    base.wall_x("GEO-ChanChan_Plaza_Main_N", -pw / 2, pw / 2, plaza_cy + pd / 2, 0.35, 4.2, 4.0, mats["adobe"], [(-10, 5.0), (10, 5.0)], "city")
    base.wall_x("GEO-ChanChan_Plaza_Main_S", -pw / 2, pw / 2, plaza_cy - pd / 2, 0.35, 4.2, 4.0, mats["adobe"], [(0, 5.0)], "city")
    base.wall_y("GEO-ChanChan_Plaza_Main_W", -pw / 2, plaza_cy - pd / 2, plaza_cy + pd / 2, 0.35, 4.2, 4.0, mats["adobe"], [(0, 5.0)], "city")
    base.wall_y("GEO-ChanChan_Plaza_Main_E", pw / 2, plaza_cy - pd / 2, plaza_cy + pd / 2, 0.35, 4.2, 4.0, mats["adobe"], [(0, 5.0)], "city")
    relief_panel("GEO-ChanChan_Plaza_Relief_N", -20, 20, plaza_cy + pd / 2 - 2.1, 2.4, mats["adobe_dark"], 8)
    relief_panel("GEO-ChanChan_Plaza_Relief_S", -20, 20, plaza_cy - pd / 2 + 2.1, 2.4, mats["adobe_dark"], 8)
    relief_panel("GEO-ChanChan_Plaza_Relief_S_Outer", -24, 24, plaza_cy - pd / 2 - 2.1, 2.4, mats["adobe_dark"], 10)
    for i, x in enumerate((-22, -11, 11, 22)):
        base.box(f"GEO-ChanChan_Plaza_Niche_N_{i}", (2.6, 0.7, 2.0), (x, plaza_cy + pd / 2 - 0.55, 1.35), mats["adobe_dark"], "props", 1.5, 0.01, True)
        base.box(f"GEO-ChanChan_Plaza_Bench_N_{i}", (3.8, 1.0, 0.55), (x, plaza_cy + pd / 2 - 3.0, 0.6), mats["adobe"], "props", 2.0, 0.01, True)

    # Rampa de acceso al lado norte.
    base.stairs("GEO-ChanChan_Plaza_Ramp", (0, plaza_cy + pd / 2 - 12, 0.2), 5.0, 1.1, 0.35, 9, "y", mats["adobe_dark"])

    # Corredor de peces y aves.
    corridor_y0, corridor_y1 = 18, plaza_cy - pd / 2
    base.box("GEO-ChanChan_Corridor_Floor", (6.0, corridor_y1 - corridor_y0, 0.24), (0, (corridor_y0 + corridor_y1) / 2, 0.12), mats["sand"], "city", 3.0, 0.01)
    base.wall_y("GEO-ChanChan_Corridor_W", -3.0, corridor_y0, corridor_y1, 0.35, 3.0, 0.9, mats["adobe"], [], "city")
    base.wall_y("GEO-ChanChan_Corridor_E", 3.0, corridor_y0, corridor_y1, 0.35, 3.0, 0.9, mats["adobe"], [], "city")
    for side, x in (("W", -3.0), ("E", 3.0)):
        for i in range(7):
            y = corridor_y0 + (i + 0.5) * (corridor_y1 - corridor_y0) / 7
            diamond_prism(f"GEO-ChanChan_Corridor_{side}_Diamond_{i}", x, y, 1.8, 0.9, 1.1, 0.18, mats["adobe_dark"], "y", "props")
            base.box(f"GEO-ChanChan_Corridor_{side}_Fish_{i}", (0.18, 0.35, 0.35), (x, y, 1.35), mats["stone"], "props", 1.0, 0.01, True)

    # Altarcillo: patio hundido entre plaza y corredor.
    alt_cx, alt_cy = 0, 38
    base.box("GEO-ChanChan_Altarcillo_Floor", (24, 20, 0.30), (alt_cx, alt_cy, -1.2), mats["sand"], "city", 3.0, 0.01)
    base.wall_x("GEO-ChanChan_Altarcillo_N", -12, 12, alt_cy + 10, -1.2, 2.4, 1.0, mats["adobe"], [(0, 3.0)], "city")
    base.wall_x("GEO-ChanChan_Altarcillo_S", -12, 12, alt_cy - 10, -1.2, 2.4, 1.0, mats["adobe"], [], "city")
    base.wall_y("GEO-ChanChan_Altarcillo_W", -12, alt_cy - 10, alt_cy + 10, -1.2, 2.4, 1.0, mats["adobe"], [], "city")
    base.wall_y("GEO-ChanChan_Altarcillo_E", 12, alt_cy - 10, alt_cy + 10, -1.2, 2.4, 1.0, mats["adobe"], [], "city")
    base.stairs("GEO-ChanChan_Altarcillo_Stairs", (0, alt_cy - 13, -1.2), 3.0, 0.8, 0.22, 6, "y", mats["adobe_dark"])

    # Audiencias alrededor de un patio central.
    for i, (x, y) in enumerate(((-34, 8), (-34, -12), (34, 8), (34, -12), (-18, -22), (18, -22), (-18, 22), (18, 22))):
        audiencia(f"GEO-ChanChan_Audiencia_{i}", x, y, 0.0, 1.0, mats)

    # Segunda plaza.
    p2x, p2y = 0, -48
    base.box("GEO-ChanChan_Plaza_Second_Floor", (38, 34, 0.32), (p2x, p2y, 0.16), mats["sand"], "city", 3.0, 0.01)
    base.wall_x("GEO-ChanChan_Plaza_Second_N", -19, 19, p2y + 17, 0.3, 3.2, 1.8, mats["adobe"], [(-8, 4.0), (8, 4.0)], "city")
    base.wall_x("GEO-ChanChan_Plaza_Second_S", -19, 19, p2y - 17, 0.3, 3.2, 1.8, mats["adobe"], [(0, 4.0)], "city")
    base.wall_y("GEO-ChanChan_Plaza_Second_W", -19, p2y - 17, p2y + 17, 0.3, 3.2, 1.8, mats["adobe"], [], "city")
    base.wall_y("GEO-ChanChan_Plaza_Second_E", 19, p2y - 17, p2y + 17, 0.3, 3.2, 1.8, mats["adobe"], [], "city")

    # Depósitos en dos alas.
    for row in range(4):
        for col in range(3):
            storeroom(f"GEO-ChanChan_Store_W_{row}_{col}", -55 + col * 8.5, -72 + row * 13, 0, mats)
            storeroom(f"GEO-ChanChan_Store_E_{row}_{col}", 30 + col * 8.5, -72 + row * 13, 0, mats)

    # Reservorio y plataforma funeraria.
    base.box("GEO-ChanChan_Reservoir_Water", (38, 30, 0.12), (-55, -112, -0.55), mats["water"], "props", 4.0, 0.0)
    base.wall_x("GEO-ChanChan_Reservoir_N", -74, -36, -97, -0.6, 1.6, 1.0, mats["adobe"], [], "city")
    base.wall_x("GEO-ChanChan_Reservoir_S", -74, -36, -127, -0.6, 1.6, 1.0, mats["adobe"], [], "city")
    base.wall_y("GEO-ChanChan_Reservoir_W", -74, -127, -97, -0.6, 1.6, 1.0, mats["adobe"], [], "city")
    base.wall_y("GEO-ChanChan_Reservoir_E", -36, -127, -97, -0.6, 1.6, 1.0, mats["adobe"], [], "city")

    for i, (size, h) in enumerate(((22, 1.4), (17, 1.4), (12, 1.4))):
        base.box(f"GEO-ChanChan_Burial_Tier_{i}", (size, size, h), (55, -105, h * (i + 0.5)), mats["adobe"], "city", 3.0, 0.03)
    base.stairs("GEO-ChanChan_Burial_Stairs", (55, -122, 0), 3.2, 0.9, 0.22, 7, "y", mats["adobe_dark"])

    # Vegetación y rocas fuera del recinto.
    for i in range(45):
        angle = rng.uniform(0, math.tau)
        radius = rng.uniform(185, 380)
        x, y = math.cos(angle) * radius, math.sin(angle) * radius
        z = terrain_height(x, y)
        base.tree(f"GEO-ChanChan_Tree_{i}", x, y, z, rng.uniform(0.7, 1.2), mats, lod1_exclude=(i % 2 == 1))
    for i in range(70):
        angle = rng.uniform(0, math.tau)
        radius = rng.uniform(165, 360)
        x, y = math.cos(angle) * radius, math.sin(angle) * radius
        z = terrain_height(x, y)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=rng.uniform(0.35, 1.0), location=(x, y, z + 0.3))
        rock = bpy.context.object
        rock.name = f"GEO-ChanChan_Rock_{i}"
        rock.scale.z = rng.uniform(0.4, 0.8)
        rock.data.materials.append(mats["stone"] if i % 3 else mats["adobe_dark"])
        rock["layer"] = "props"
        rock["lod1_exclude"] = True
        base.add_to(rock, base.bucket("Props"))

    for i, (x, y) in enumerate(((-12, 55), (10, 62), (-2, -30), (16, 4), (-44, -86), (40, -100))):
        human(f"GEO-ChanChan_Human_{i}", x, y, terrain_height(x, y) + 0.2, mats)

    course_targets = ("Perimeter", "Plaza_Main", "Plaza_Second", "Corridor", "Audiencia_")
    for obj in list(bpy.data.objects):
        if obj.type != "MESH" or obj.get("layer") != "city":
            continue
        if not any(key in obj.name for key in course_targets):
            continue
        if obj.dimensions.z < 1.8 or max(obj.dimensions.x, obj.dimensions.y) < 5:
            continue
        adobe_courses(obj, mats["adobe"], mats["adobe_dark"], 260)

    sun_data = bpy.data.lights.new("LGT-ChanChan_Sun", "SUN")
    sun_data.energy = 4.0
    sun_data.angle = math.radians(4)
    sun_data.color = (1.0, 0.82, 0.62)
    sun = bpy.data.objects.new("LGT-ChanChan_Sun", sun_data)
    scene.collection.objects.link(sun)
    sun.rotation_euler = (math.radians(24), math.radians(-18), math.radians(-38))
    fill_data = bpy.data.lights.new("LGT-ChanChan_Fill", "AREA")
    fill_data.energy = 900
    fill_data.shape = "DISK"
    fill_data.size = 260
    fill_data.color = (0.58, 0.72, 0.92)
    fill = bpy.data.objects.new("LGT-ChanChan_Fill", fill_data)
    scene.collection.objects.link(fill)
    fill.location = (0, -220, 120)
    fill.rotation_euler = (Vector((0, 0, 10)) - fill.location).to_track_quat("-Z", "Y").to_euler()

    camera_defs = {
        "Hero": ((175, -215, 105), (-5, 0, 8), 42),
        "Tour1": ((18, 165, 14), (0, 120, 6), 42),
        "Tour2": ((0, 60, 7), (0, 112, 4), 44),
        "Tour3": ((11, 16, 5), (0, 38, 2.2), 55),
        "Tour4": ((32, 42, 14), (18, 18, 2), 45),
        "Tour5": ((-22, -72, 22), (0, -38, 4), 42),
        "Tour6": ((-12, -180, 30), (-25, -100, 2), 45),
    }
    for name, (pos, target, lens) in camera_defs.items():
        cam_data = bpy.data.cameras.new(f"CAM-ChanChan_{name}")
        cam_data.lens = lens
        cam = bpy.data.objects.new(f"CAM-ChanChan_{name}", cam_data)
        scene.collection.objects.link(cam)
        cam.location = pos
        cam.rotation_euler = (Vector(target) - cam.location).to_track_quat("-Z", "Y").to_euler()
    scene.camera = bpy.data.objects["CAM-ChanChan_Hero"]

    scene.render.resolution_x = 1600
    scene.render.resolution_y = 900
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "JPEG"
    scene.render.image_settings.quality = 90
    scene.render.film_transparent = False
    scene.world.color = (0.36, 0.47, 0.60)
    scene.render.filepath = PREVIEW
    bpy.ops.render.render(write_still=True)

    os.makedirs(os.path.dirname(OUT_BLEND), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
    print("CHANCHAN_HIGHPOLY_OK", OUT_BLEND, PREVIEW)
    print("CHANCHAN_CAMERAS", json.dumps({k: {"position": v[0], "target": v[1], "fov": v[2]} for k, v in camera_defs.items()}))


if __name__ == "__main__":
    main()
