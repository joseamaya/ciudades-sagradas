"""Genera el preview v0.1 del núcleo monumental de Wari.

Uso:
  blender --background --python scripts/wari/build_wari_highpoly.py

La planta es una lectura de conjunto de los sectores documentados:
Vegachayoc Moqo, Capillapata, Monqachayoc y Cheqo Huasi. No se modelan
las 2.000 ha del sitio ni se cierran alturas, techos o el trazado urbano.
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

OUT_BLEND = os.path.join(ROOT, "blender", "wari", "wari_highpoly_v0.1.blend")
PREVIEW = "/tmp/wari_highpoly_v0.1.jpg"
HERO = os.path.join(ROOT, "public", "cities", "wari", "hero.jpg")
SEED = 7311
TERRAIN_SIZE = 900
TERRAIN_N = 170
rng = random.Random(SEED)


def scene_collections(scene):
    for name in ("City", "Terrain", "Props", "Reference"):
        col = bpy.data.collections.new(f"COL-Wari_{name}")
        scene.collection.children.link(col)
    base.bucket = lambda name: bpy.data.collections[f"COL-Wari_{name}"]


def terrain_height(x, y):
    z = -0.8 + 0.012 * x - 0.008 * y
    z += 0.9 * math.sin(x * 0.018) * math.cos(y * 0.016)
    z += 0.35 * math.sin((x - y) * 0.031)
    r = math.hypot(x, y)
    if r > 250:
        z += 0.035 * (r - 250)
    z += 28 * math.exp(-(((x - 360) / 130) ** 2 + ((y + 160) / 180) ** 2))
    z += 24 * math.exp(-(((x + 350) / 120) ** 2 + ((y - 120) / 170) ** 2))
    z += 32 * math.exp(-(((x + 80) / 190) ** 2 + ((y + 360) / 130) ** 2))
    z += 46 * math.exp(-(((x - 70) / 150) ** 2 + ((y - 360) / 115) ** 2))
    z += 38 * math.exp(-(((x + 310) / 140) ** 2 + ((y - 250) / 140) ** 2))
    z += 34 * math.exp(-(((x - 330) / 130) ** 2 + ((y - 210) / 150) ** 2))
    return z


def cut_terrain_area(obj, points, target_z, margin=8.0):
    x0, x1 = min(p[0] for p in points), max(p[0] for p in points)
    y0, y1 = min(p[1] for p in points), max(p[1] for p in points)
    for vert in obj.data.vertices:
        x, y, old = vert.co.x, vert.co.y, vert.co.z
        dx = max(x0 - x, 0.0, x - x1)
        dy = max(y0 - y, 0.0, y - y1)
        dist = max(dx, dy)
        if dist <= 0.0:
            vert.co.z = target_z
        elif dist < margin:
            t = 1.0 - dist / margin
            t = t * t * (3.0 - 2.0 * t)
            vert.co.z = old * (1.0 - t) + target_z * t
    obj.data.update()


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
    mesh = bpy.data.meshes.new("MESH-Wari_Terrain")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new("GEO-Wari_Terrain", mesh)
    base.bucket("Terrain").objects.link(obj)
    obj.data.materials.append(mats["earth"])
    uv = mesh.uv_layers.new(name="UVMap")
    for poly in mesh.polygons:
        for loop in poly.loop_indices:
            co = mesh.vertices[mesh.loops[loop].vertex_index].co
            uv.data[loop].uv = ((co.x + size / 2) / 24.0, (co.y + size / 2) / 24.0)
    obj["layer"] = "terrain"
    return obj


def make_materials():
    stone = base.texture_set("WariStone", SEED, (0.30, 0.27, 0.22), (0.58, 0.52, 0.42), "stone", 2048)
    stone_dark = base.texture_set("WariStoneDark", SEED + 7, (0.20, 0.18, 0.15), (0.42, 0.38, 0.31), "stone", 1024)
    earth = base.texture_set("WariEarth", SEED + 20, (0.42, 0.33, 0.21), (0.62, 0.50, 0.33), "stone", 2048)
    plaster = base.texture_set("WariPlaster", SEED + 31, (0.58, 0.54, 0.45), (0.78, 0.72, 0.60), "stone", 1024)
    red = base.texture_set("WariRed", SEED + 37, (0.34, 0.10, 0.07), (0.58, 0.20, 0.13), "stone", 1024)
    water = base.material("MAT-Wari_Water", color=(0.06, 0.20, 0.23, 1.0), roughness_value=0.24)
    wood = base.material("MAT-Wari_Wood", color=(0.16, 0.10, 0.06, 1.0), roughness_value=0.9)
    leaf = base.material("MAT-Wari_Leaf", color=(0.12, 0.21, 0.08, 1.0), roughness_value=0.92)
    leaf_dark = base.material("MAT-Wari_LeafDark", color=(0.07, 0.14, 0.05, 1.0), roughness_value=0.94)
    grass = base.texture_set("WariGrass", SEED + 51, (0.18, 0.22, 0.10), (0.36, 0.40, 0.18), "moss", 1024)
    return {
        "stone": base.material("MAT-Wari_Stone", *stone),
        "stone_dark": base.material("MAT-Wari_StoneDark", *stone_dark),
        "earth": base.material("MAT-Wari_Earth", *earth),
        "plaster": base.material("MAT-Wari_Plaster", *plaster),
        "red": base.material("MAT-Wari_Red", *red),
        "grass": base.material("MAT-Wari_Grass", *grass),
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


def stone_courses(obj, mat_a, mat_b, max_blocks=260):
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
            rows = max(1, int(dz / 0.55))
            cols = max(1, int(dx / 1.4))
            for row in range(rows):
                h = dz / rows
                z = z0 + (row + 0.5) * h
                offset = (row % 2) * (dx / cols) * 0.5
                for col in range(cols):
                    if blocks >= max_blocks:
                        break
                    w = dx / cols * rng.uniform(0.78, 0.97)
                    x = x0 + offset + (col + 0.5) * (dx / cols)
                    if x - w / 2 < x0 or x + w / 2 > x1:
                        continue
                    yy = y_face + sign * 0.06
                    box_face(verts, faces, indices, (x, yy, z), (w, 0.12, h * 0.82), 0 if rng.random() < 0.7 else 1)
                    blocks += 1
    else:
        for x_face, sign in ((x0, -1), (x1, 1)):
            rows = max(1, int(dz / 0.55))
            cols = max(1, int(dy / 1.4))
            for row in range(rows):
                h = dz / rows
                z = z0 + (row + 0.5) * h
                offset = (row % 2) * (dy / cols) * 0.5
                for col in range(cols):
                    if blocks >= max_blocks:
                        break
                    w = dy / cols * rng.uniform(0.78, 0.97)
                    y = y0 + offset + (col + 0.5) * (dy / cols)
                    if y - w / 2 < y0 or y + w / 2 > y1:
                        continue
                    xx = x_face + sign * 0.06
                    box_face(verts, faces, indices, (xx, y, z), (0.12, w, h * 0.82), 0 if rng.random() < 0.7 else 1)
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


def d_wall(name, cx, cy, radius, thickness, height, z0, start, end, mat, segments=18):
    verts = []
    faces = []
    for i in range(segments + 1):
        a = start + (end - start) * i / segments
        co, si = math.cos(a), math.sin(a)
        for r in (radius, radius + thickness):
            for z in (z0, z0 + height):
                verts.append((cx + co * r, cy + si * r, z))
    for i in range(segments):
        b = i * 4
        n = (i + 1) * 4
        faces.extend([
            (b, n, n + 1, b + 1),
            (b + 2, b + 3, n + 3, n + 2),
            (b, b + 2, n + 2, n),
            (b + 1, n + 1, n + 3, b + 3),
        ])
    faces.append((0, 1, 3, 2))
    b = segments * 4
    faces.append((b, b + 2, b + 3, b + 1))
    return mesh_obj(name, verts, faces, mat)


def niche(name, x, y, z, w=1.0, h=1.3, depth=0.35, mat=None):
    base.box(name, (w, depth, h), (x, y, z), mat, "props", 1.4, 0.01, True)


def gallery(name, x, y, z, w, d, h, mats, door_side="south"):
    t = 0.7
    base.box(f"{name}_Floor", (w, d, 0.25), (x, y, z + 0.12), mats["earth"], "city", 2.0, 0.01)
    base.box(f"{name}_Back", (w, t, h), (x, y + d / 2, z + h / 2), mats["stone"], "city", 2.2, 0.02)
    base.box(f"{name}_Left", (t, d, h), (x - w / 2, y, z + h / 2), mats["stone"], "city", 2.2, 0.02)
    base.box(f"{name}_Right", (t, d, h), (x + w / 2, y, z + h / 2), mats["stone"], "city", 2.2, 0.02)
    if door_side == "south":
        base.box(f"{name}_FrontL", (w / 2 - 0.7, t, h), (x - w / 4 - 0.35, y - d / 2, z + h / 2), mats["stone"], "city", 2.2, 0.02)
        base.box(f"{name}_FrontR", (w / 2 - 0.7, t, h), (x + w / 4 + 0.35, y - d / 2, z + h / 2), mats["stone"], "city", 2.2, 0.02)
    for i in range(3):
        niche(f"{name}_Niche_{i}", x - w / 3 + i * w / 3, y + d / 2 - 0.42, z + 1.35, 0.9, 1.2, 0.3, mats["stone_dark"])
    base.box(f"{name}_Lintel", (w, t + 0.1, 0.35), (x, y + d / 2 - 0.02, z + h - 0.18), mats["stone_dark"], "city", 2.0, 0.01, True)


def terrace(name, x, y, w, d, h, z0, mats):
    base.box(name, (w, d, h), (x, y, z0 + h / 2), mats["stone"], "city", 3.0, 0.03)
    base.box(f"{name}_Top", (w - 1.0, d - 1.0, 0.22), (x, y, z0 + h + 0.11), mats["earth"], "city", 3.0, 0.01)
    base.box(f"{name}_RedBand", (w, 0.18, 0.9), (x, y - d / 2 - 0.09, z0 + h - 0.55), mats["red"], "props", 2.0, 0.01, True)


def main():
    scene = base.clean_scene()
    scene_collections(scene)
    mats = make_materials()
    terrain_obj = terrain(mats)
    cut_terrain_area(terrain_obj, [(74, -61), (106, -61), (106, -29), (74, -29)], -3.0, 8.0)

    # Capillapata: doble muro segmentado de 360 m, 9 m de alto.
    zc = terrain_height(0, 100)
    tapered_wall("GEO-Wari_Capillapata_N", 0, 107, 360, 9.0, 3.0, 1.0, "x", zc, mats["stone"])
    tapered_wall("GEO-Wari_Capillapata_S", 0, 96, 360, 8.0, 2.8, 0.95, "x", zc, mats["stone"])
    base.box("GEO-Wari_Capillapata_Red", (360, 0.2, 0.8), (0, 107 + 1.6, zc + 6.2), mats["red"], "props", 2.0, 0.01, True)
    for i in range(8):
        niche(f"GEO-Wari_Capillapata_Niche_{i}", -140 + i * 40, 96 - 1.5, zc + 2.4, 1.6, 2.0, 0.4, mats["stone_dark"])

    # Terraza ceremonial y plaza central.
    terrace("GEO-Wari_Terrace_Main", 0, 20, 150, 95, 2.4, terrain_height(0, 20) - 2.4, mats)
    base.box("GEO-Wari_Plaza_Floor", (46, 38, 0.25), (0, 10, 2.45), mats["earth"], "city", 3.0, 0.01)
    base.wall_x("GEO-Wari_Plaza_N", -23, 23, 29, 2.4, 2.2, 1.1, mats["plaster"], [(-6, 3.0), (6, 3.0)], "city")
    base.wall_x("GEO-Wari_Plaza_S", -23, 23, -9, 2.4, 2.2, 1.1, mats["plaster"], [(0, 3.0)], "city")
    base.wall_y("GEO-Wari_Plaza_W", -23, -9, 29, 2.4, 2.2, 1.1, mats["plaster"], [], "city")
    base.wall_y("GEO-Wari_Plaza_E", 23, -9, 29, 2.4, 2.2, 1.1, mats["plaster"], [], "city")
    for i in range(5):
        niche(f"GEO-Wari_Plaza_Niche_{i}", -12 + i * 6, 28.1, 3.4, 1.2, 1.5, 0.35, mats["stone_dark"])

    # Plataforma de Vegachayoc Moqo y templo en D.
    base.box("GEO-Wari_Vegachayoc_Platform", (76, 58, 3.2), (-88, 34, terrain_height(-88, 34) + 1.6), mats["stone"], "city", 3.0, 0.03)
    base.box("GEO-Wari_Vegachayoc_Top", (74, 56, 0.22), (-88, 34, terrain_height(-88, 34) + 3.31), mats["earth"], "city", 3.0, 0.01)
    base.stairs("GEO-Wari_Vegachayoc_Stairs", (-48, 34, terrain_height(-48, 34)), 4.0, 1.0, 0.32, 10, "x", mats["stone"])
    for i, y in enumerate((56, 70)):
        terrace(f"GEO-Wari_Terrace_North_{i}", -20, y, 210, 12, 1.6 + i * 0.4, terrain_height(-20, y) - 1.6 - i * 0.4, mats)
    tcx, tcy, tr = -85, 30, 24
    tz = terrain_height(tcx, tcy) + 3.4
    d_wall("GEO-Wari_D_Temple", tcx, tcy, tr, 1.5, 5.0, tz, math.radians(-90), math.radians(90), mats["stone"])
    base.wall_y("GEO-Wari_D_Temple_Flat", tcx, tcy - tr, tcy + tr, tz, 5.0, 1.5, mats["stone"], [(tcy, 4.0)], "city")
    base.box("GEO-Wari_D_Temple_Floor", (tr * 2, tr * 2, 0.3), (tcx + tr / 2, tcy, tz + 0.15), mats["earth"], "city", 3.0, 0.01)
    base.box("GEO-Wari_D_Temple_Altar", (6, 5, 1.1), (tcx + 8, tcy, tz + 0.55), mats["red"], "city", 2.0, 0.02)
    d_wall("GEO-Wari_D_Temple_Red", tcx, tcy, tr + 0.06, 0.12, 0.45, tz + 3.7, math.radians(-90), math.radians(90), mats["red"], 18)
    for i in range(4):
        niche(f"GEO-Wari_D_Temple_Niche_{i}", tcx + tr * math.cos(math.radians(-60 + i * 40)), tcy + tr * math.sin(math.radians(-60 + i * 40)), tz + 2.2, 1.1, 1.5, 0.35, mats["stone_dark"])

    # Monqachayoc: patio hundido, mausoleo y galerías perimetrales.
    mcx, mcy = 90, -45
    mz = -3.0
    base.box("GEO-Wari_Monqachayoc_Floor", (26, 26, 0.3), (mcx, mcy, mz + 0.15), mats["stone_dark"], "city", 3.0, 0.01)
    for name, x, y, w, d in (
        ("N", mcx, mcy + 13, 30, 1.4),
        ("S", mcx, mcy - 13, 30, 1.4),
        ("W", mcx - 13, mcy, 1.4, 30),
        ("E", mcx + 13, mcy, 1.4, 30),
    ):
        base.box(f"GEO-Wari_Monqachayoc_Wall_{name}", (w, d, 3.4), (x, y, mz + 1.7), mats["stone"], "city", 2.5, 0.02)
    for i in range(4):
        niche(f"GEO-Wari_Monqachayoc_Niche_{i}", mcx - 9 + i * 6, mcy + 12.2, mz + 1.4, 1.1, 1.5, 0.35, mats["stone_dark"])
    base.stairs("GEO-Wari_Monqachayoc_Stairs", (mcx, mcy - 16, mz), 3.0, 0.8, 0.22, 8, "y", mats["stone"])
    base.box("GEO-Wari_Monqachayoc_Mausoleum", (12, 10, 3.8), (mcx, mcy + 2, mz + 1.9), mats["stone"], "city", 2.5, 0.02)
    base.box("GEO-Wari_Monqachayoc_Door", (2.2, 0.6, 2.2), (mcx, mcy - 3.2, mz + 1.1), mats["stone_dark"], "city", 1.5, 0.01)

    # Cheqo Huasi: recinto de galerías y nichos.
    ccx, ccy = 105, 42
    cz = terrain_height(ccx, ccy)
    base.box("GEO-Wari_CheqoHuasi_Platform", (48, 34, 1.2), (ccx, ccy, cz + 0.6), mats["stone"], "city", 3.0, 0.02)
    base.wall_x("GEO-Wari_CheqoHuasi_N", ccx - 24, ccx + 24, ccy + 17, cz + 1.2, 3.8, 1.2, mats["stone"], [(-8, 3.0), (8, 3.0)], "city")
    base.wall_x("GEO-Wari_CheqoHuasi_S", ccx - 24, ccx + 24, ccy - 17, cz + 1.2, 3.8, 1.2, mats["stone"], [(0, 3.0)], "city")
    base.wall_y("GEO-Wari_CheqoHuasi_W", ccx - 24, ccy - 17, ccy + 17, cz + 1.2, 3.8, 1.2, mats["stone"], [], "city")
    base.wall_y("GEO-Wari_CheqoHuasi_E", ccx + 24, ccy - 17, ccy + 17, cz + 1.2, 3.8, 1.2, mats["stone"], [], "city")
    for i in range(4):
        gallery(f"GEO-Wari_CheqoHuasi_Gallery_{i}", ccx - 16 + i * 10, ccy + 5, cz + 1.2, 6.0, 7.0, 2.8, mats)
    base.box("GEO-Wari_CheqoHuasi_Red", (48, 0.2, 0.7), (ccx, ccy + 17.69, cz + 4.3), mats["red"], "props", 2.0, 0.01, True)

    # Terrazas meridionales y canal de agua.
    for i, (y, h) in enumerate(((-70, 1.8), (-88, 2.4), (-106, 3.0))):
        terrace(f"GEO-Wari_Terrace_South_{i}", 0, y, 300, 14, h, terrain_height(0, y) - h, mats)
    base.box("GEO-Wari_Canal", (180, 0.9, 0.28), (70, -62, terrain_height(70, -62) + 0.14), mats["water"], "props", 3.0, 0.0)
    base.wall_x("GEO-Wari_Canal_N", 0, 160, -61.1, terrain_height(0, -61.1), 0.5, 0.5, mats["stone"], [], "props")
    base.wall_x("GEO-Wari_Canal_S", 0, 160, -62.9, terrain_height(0, -62.9), 0.5, 0.5, mats["stone"], [], "props")

    # Muros y recintos menores.
    for i, (x, y, w, d) in enumerate(((40, 40, 20, 14), (-30, -20, 18, 12), (60, 10, 16, 12), (-120, -20, 22, 14))):
        gallery(f"GEO-Wari_Compound_{i}", x, y, terrain_height(x, y), w, d, 2.6, mats)
    for i, (x, y) in enumerate(((42, 26), (42, 8), (-38, 12), (-38, -4), (72, -12), (72, -30), (-58, -18), (-58, -36))):
        gallery(f"GEO-Wari_Barrio_{i}", x, y, terrain_height(x, y), 8.0, 9.0, 2.4, mats)
    for i, (x, y) in enumerate(((-12, -24), (12, -24), (-28, -40), (28, -40), (-48, -54), (48, -54), (0, -52), (20, -52))):
        gallery(f"GEO-Wari_Barrio_Sur_{i}", x, y, terrain_height(x, y), 7.0, 8.0, 2.2, mats)
    # Templo en D secundario, lectura de los sectores con planta en D.
    d_wall("GEO-Wari_D_Temple_2", 62, 64, 12, 1.2, 3.6, terrain_height(62, 64) + 1.6, math.radians(-90), math.radians(90), mats["stone"])
    d_wall("GEO-Wari_D_Temple_2_Red", 62, 64, 12.06, 0.10, 0.35, terrain_height(62, 64) + 4.7, math.radians(-90), math.radians(90), mats["red"], 12)
    base.wall_y("GEO-Wari_D_Temple_2_Flat", 62, 52, 76, terrain_height(62, 64) + 1.6, 3.6, 1.2, mats["stone"], [(64, 3.0)], "city")

    # Vegetación andina dispersa.
    for i in range(55):
        angle = rng.uniform(0, math.tau)
        radius = rng.uniform(210, 390)
        x, y = math.cos(angle) * radius, math.sin(angle) * radius
        z = terrain_height(x, y)
        base.tree(f"GEO-Wari_Tree_{i}", x, y, z, rng.uniform(0.55, 0.95), mats, lod1_exclude=(i % 2 == 1))
    for i in range(80):
        angle = rng.uniform(0, math.tau)
        radius = rng.uniform(180, 370)
        x, y = math.cos(angle) * radius, math.sin(angle) * radius
        z = terrain_height(x, y)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=rng.uniform(0.35, 0.9), location=(x, y, z + 0.28))
        shrub = bpy.context.object
        shrub.name = f"GEO-Wari_Shrub_{i}"
        shrub.scale.z = rng.uniform(0.35, 0.7)
        shrub.data.materials.append(mats["leaf_dark"] if i % 2 else mats["leaf"])
        shrub["layer"] = "props"
        shrub["lod1_exclude"] = True
        base.add_to(shrub, base.bucket("Props"))

    for i, (x, y) in enumerate(((-10, 10), (12, 5), (-80, 20), (92, -40), (105, 30), (30, -70))):
        base.cylinder(f"GEO-Wari_Human_{i}", 0.16, 1.05, (x, y, terrain_height(x, y) + 0.52), mats["stone_dark"], "reference", 8)

    for obj in list(bpy.data.objects):
        if obj.type != "MESH" or obj.get("layer") != "city":
            continue
        if not any(key in obj.name for key in ("Capillapata", "D_Temple", "Plaza", "CheqoHuasi", "Monqachayoc", "Terrace")):
            continue
        if obj.dimensions.z < 1.5 or max(obj.dimensions.x, obj.dimensions.y) < 5:
            continue
        stone_courses(obj, mats["stone"], mats["stone_dark"], 240)

    sun_data = bpy.data.lights.new("LGT-Wari_Sun", "SUN")
    sun_data.energy = 3.4
    sun_data.angle = math.radians(5)
    sun_data.color = (1.0, 0.86, 0.68)
    sun = bpy.data.objects.new("LGT-Wari_Sun", sun_data)
    scene.collection.objects.link(sun)
    sun.rotation_euler = (math.radians(25), math.radians(-16), math.radians(-42))
    fill_data = bpy.data.lights.new("LGT-Wari_Fill", "AREA")
    fill_data.energy = 800
    fill_data.shape = "DISK"
    fill_data.size = 260
    fill_data.color = (0.56, 0.70, 0.92)
    fill = bpy.data.objects.new("LGT-Wari_Fill", fill_data)
    scene.collection.objects.link(fill)
    fill.location = (0, -220, 120)
    fill.rotation_euler = (Vector((0, 0, 10)) - fill.location).to_track_quat("-Z", "Y").to_euler()

    camera_defs = {
        "Hero": ((135, -170, 70), (0, 12, 8), 45),
        "Tour1": ((120, -160, 75), (0, 12, 8), 46),
        "Tour2": ((-5, 95, 30), (-85, 35, 4), 50),
        "Tour3": ((0, -58, 26), (0, 10, 4), 45),
        "Tour4": ((60, 20, 32), (0, 100, 7), 45),
        "Tour5": ((90, -92, 30), (90, -45, -1), 50),
        "Tour6": ((150, 80, 36), (105, 42, 4), 50),
    }
    for name, (pos, target, lens) in camera_defs.items():
        cam_data = bpy.data.cameras.new(f"CAM-Wari_{name}")
        cam_data.lens = lens
        cam = bpy.data.objects.new(f"CAM-Wari_{name}", cam_data)
        scene.collection.objects.link(cam)
        cam.location = pos
        cam.rotation_euler = (Vector(target) - cam.location).to_track_quat("-Z", "Y").to_euler()
    scene.camera = bpy.data.objects["CAM-Wari_Hero"]

    scene.render.resolution_x = 1600
    scene.render.resolution_y = 900
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "JPEG"
    scene.render.image_settings.quality = 90
    scene.render.film_transparent = False
    scene.world.color = (0.36, 0.45, 0.58)
    scene.render.filepath = PREVIEW
    bpy.ops.render.render(write_still=True)

    os.makedirs(os.path.dirname(OUT_BLEND), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
    print("WARI_HIGHPOLY_OK", OUT_BLEND, PREVIEW)
    print("WARI_CAMERAS", json.dumps({k: {"position": v[0], "target": v[1], "fov": v[2]} for k, v in camera_defs.items()}))


if __name__ == "__main__":
    main()
