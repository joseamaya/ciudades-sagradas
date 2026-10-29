"""Sube el blockout de Aypate a un pase high-poly v0.4.

Uso:
  blender --background blender/aypate/aypate_blockout_v0.4.blend \
    --python scripts/build_aypate_highpoly_v0_3.py

Añade cladding de piedra, pavimento, vegetación y texturas 2K. No inventa
techos, alturas ni recintos: el layout macro sigue el plano de 2013 y los
detalles no conservados quedan como interpretativos.
"""

import math
import os
import random
import sys

import bpy
import numpy as np
from mathutils import Vector

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import build_aypate_blockout as base_mod  # noqa: E402
import build_aypate_blockout_v0_4 as block  # noqa: E402

OUT = os.path.join(ROOT, "blender", "aypate", "aypate_highpoly_v0.4.blend")
HERO = "/tmp/aypate_highpoly_v04_hero.jpg"
SEED = 90210
rng = random.Random(SEED)


def add_to(obj, col_name):
    for col in list(obj.users_collection):
        col.objects.unlink(obj)
    bpy.data.collections[col_name].objects.link(obj)


def uv_cube(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.cube_project(cube_size=2.5)
    bpy.ops.object.mode_set(mode="OBJECT")
    obj.select_set(False)


def box_face(verts, faces, mats, center, size, material_index):
    x, y, z = center
    sx, sy, sz = (v / 2 for v in size)
    base = len(verts)
    verts.extend([
        (x - sx, y - sy, z - sz), (x + sx, y - sy, z - sz),
        (x + sx, y + sy, z - sz), (x - sx, y + sy, z - sz),
        (x - sx, y - sy, z + sz), (x + sx, y - sy, z + sz),
        (x + sx, y + sy, z + sz), (x - sx, y + sy, z + sz),
    ])
    faces.extend([
        (base, base + 1, base + 5, base + 4),
        (base + 1, base + 2, base + 6, base + 5),
        (base + 2, base + 3, base + 7, base + 6),
        (base + 3, base, base + 4, base + 7),
        (base + 4, base + 5, base + 6, base + 7),
        (base, base + 3, base + 2, base + 1),
    ])
    mats.extend([material_index] * 6)


def make_block_mesh(name, verts, faces, mat_indices, materials, layer):
    mesh = bpy.data.meshes.new(f"MESH-{name}")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    for mat in materials:
        mesh.materials.append(mat)
    for poly, index in zip(mesh.polygons, mat_indices):
        poly.material_index = index
    obj = bpy.data.objects.new(name, mesh)
    bpy.data.collections[f"COL-Aypate_{layer.title()}"].objects.link(obj)
    obj["layer"] = layer
    obj["lod1_exclude"] = False
    uv_cube(obj)
    return obj


def skin_object(obj, stone, stone_dark, max_blocks=1000, block_w=1.05, block_h=0.52, depth=0.10):
    if obj.type != "MESH" or obj.name.startswith("GEO-Aypate_Blocks"):
        return 0
    dx, dy, dz = obj.dimensions
    if dz < 0.55 or min(dx, dy) < 0.45:
        return 0
    loc = obj.location
    x0, x1 = loc.x - dx / 2, loc.x + dx / 2
    y0, y1 = loc.y - dy / 2, loc.y + dy / 2
    z0, z1 = loc.z - dz / 2, loc.z + dz / 2
    verts, faces, indices = [], [], []
    blocks = 0
    if dx >= dy:
        length = dx
        for side, y_face, sign in (("S", y0, -1), ("N", y1, 1)):
            cols = max(1, int(length / block_w))
            rows = max(1, int(dz / block_h))
            for row in range(rows):
                h = dz / rows
                z = z0 + (row + 0.5) * h
                offset = (row % 2) * (length / cols) * 0.5
                for col in range(cols):
                    if blocks >= max_blocks:
                        break
                    w = length / cols * rng.uniform(0.82, 0.98)
                    x = x0 + offset + (col + 0.5) * (length / cols)
                    if x - w / 2 < x0 or x + w / 2 > x1:
                        continue
                    yy = y_face + sign * (depth / 2 + 0.015)
                    box_face(verts, faces, indices, (x, yy, z), (w, depth, h * 0.86), 0 if rng.random() < 0.72 else 1)
                    blocks += 1
    else:
        length = dy
        for side, x_face, sign in (("W", x0, -1), ("E", x1, 1)):
            cols = max(1, int(length / block_w))
            rows = max(1, int(dz / block_h))
            for row in range(rows):
                h = dz / rows
                z = z0 + (row + 0.5) * h
                offset = (row % 2) * (length / cols) * 0.5
                for col in range(cols):
                    if blocks >= max_blocks:
                        break
                    w = length / cols * rng.uniform(0.82, 0.98)
                    y = y0 + offset + (col + 0.5) * (length / cols)
                    if y - w / 2 < y0 or y + w / 2 > y1:
                        continue
                    xx = x_face + sign * (depth / 2 + 0.015)
                    box_face(verts, faces, indices, (xx, y, z), (depth, w, h * 0.86), 0 if rng.random() < 0.72 else 1)
                    blocks += 1
    if blocks:
        make_block_mesh(f"GEO-Aypate_Blocks_{obj.name.replace('GEO-Aypate_', '')}", verts, faces, indices, [stone, stone_dark], "city")
    return blocks


def paving(stone):
    verts, faces, indices = [], [], []
    poly = block.PLAZA_POLY
    x0 = min(p[0] for p in poly)
    x1 = max(p[0] for p in poly)
    y0 = min(p[1] for p in poly)
    y1 = max(p[1] for p in poly)

    def inside(x, y):
        hit = False
        j = len(poly) - 1
        for i in range(len(poly)):
            xi, yi = poly[i]
            xj, yj = poly[j]
            if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
                hit = not hit
            j = i
        return hit

    size = 2.0
    z = block.PLAZA_Z + 0.28
    for x in np.arange(x0 + size / 2, x1, size):
        for y in np.arange(y0 + size / 2, y1, size):
            if not inside(float(x), float(y)):
                continue
            if abs(x + 78) < 5:
                continue
            box_face(verts, faces, indices, (float(x), float(y), z), (size * 0.92, size * 0.92, 0.10), 0)
    obj = make_block_mesh("GEO-Aypate_Plaza_Paving", verts, faces, indices, [stone], "city")
    obj["lod1_exclude"] = True
    return len(faces) // 6


def add_tree_high(name, x, y, z, scale, mats, lod1_exclude=False):
    # More detailed canopy than the blockout tree.
    parts = []
    trunk_h = 3.8 * scale
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.18 * scale, depth=trunk_h, location=(x, y, z + trunk_h / 2))
    trunk = bpy.context.object
    trunk.name = f"{name}_trunk"
    trunk.data.materials.append(mats["wood"])
    parts.append(trunk)
    for i, (dx, dy, dz, rad) in enumerate(((0, 0, trunk_h + 1.7 * scale, 2.4 * scale), (-1.1, 0.6, trunk_h + 1.2 * scale, 1.8 * scale), (1.0, -0.5, trunk_h + 1.4 * scale, 1.7 * scale), (0.2, 1.0, trunk_h + 2.7 * scale, 1.3 * scale))):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=rad, location=(x + dx * scale, y + dy * scale, z + dz))
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
    add_to(obj, "COL-Aypate_Props")


def replace_textures():
    b = base_mod
    mappings = (
        ("MAT-Aypate_Stone", "Stone2K", 7319, (0.30, 0.29, 0.25), (0.58, 0.54, 0.45), "stone"),
        ("MAT-Aypate_StoneDark", "StoneDark2K", 7379, (0.16, 0.16, 0.14), (0.38, 0.36, 0.31), "stone"),
        ("MAT-Aypate_Ground", "Ground2K", 7339, (0.2, 0.17, 0.11), (0.45, 0.39, 0.26), "ground"),
        ("MAT-Aypate_Moss", "Moss2K", 7359, (0.10, 0.18, 0.06), (0.30, 0.42, 0.16), "moss"),
        ("MAT-Aypate_Clay", "Clay2K", 7399, (0.42, 0.25, 0.18), (0.62, 0.39, 0.26), "stone"),
    )
    for mat_name, label, seed, base, accent, kind in mappings:
        mat = bpy.data.materials.get(mat_name)
        if mat is None:
            continue
        diffuse, rough, normal = b.texture_set(label, seed, base, accent, kind, 2048)
        for image in (rough, normal):
            image.scale(1024, 1024)
            image.pack()
        for node in mat.node_tree.nodes:
            if node.type != "TEX_IMAGE":
                continue
            if node.name == "Diffuse":
                node.image = diffuse
            elif node.name == "Roughness":
                node.image = rough
            elif node.name == "Normal":
                node.image = normal
        print("AYPATE_TEXTURE_2K", mat_name)


def main():
    bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, "blender", "aypate", "aypate_blockout_v0.4.blend"))
    replace_textures()
    mats = {name: bpy.data.materials[name] for name in ("MAT-Aypate_Stone", "MAT-Aypate_StoneDark", "MAT-Aypate_Ground", "MAT-Aypate_Moss", "MAT-Aypate_Wood", "MAT-Aypate_Leaf", "MAT-Aypate_LeafDark")}
    tree_mats = {
        "wood": mats["MAT-Aypate_Wood"],
        "leaf": mats["MAT-Aypate_Leaf"],
        "leaf_dark": mats["MAT-Aypate_LeafDark"],
    }
    # Only detail the documented architectural core.
    tokens = (
        "Kallanka", "Acllawasi", "Ushnu", "Palace", "Colca", "Control",
        "Fountain", "Plaza_Parapet", "Terrace", "QhapaqNan",
    )
    total_blocks = 0
    for obj in list(bpy.data.objects):
        if obj.type == "MESH" and any(token in obj.name for token in tokens):
            total_blocks += skin_object(obj, mats["MAT-Aypate_Stone"], mats["MAT-Aypate_StoneDark"])
    print("AYPATE_BLOCKS", total_blocks)
    # La plaza es arcilla compacta: no se genera una cuadrícula de losas.
    for i, (x, y, sx, sy) in enumerate((
        (-66, 0, 7, 3), (60, 0, 7, 3), (0, -48, 3, 7), (0, 38, 3, 7),
        (0, -101, 6, 3),
    )):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, block.PLAZA_Z + 0.34))
        slab = bpy.context.object
        slab.name = f"GEO-Aypate_Threshold_{i}"
        slab.dimensions = (sx, sy, 0.12)
        slab.data.materials.append(mats["MAT-Aypate_Stone"])
        slab["layer"] = "props"
        slab["lod1_exclude"] = True
        add_to(slab, "COL-Aypate_Props")
    for i in range(48):
        angle = rng.uniform(0, math.tau)
        radius = rng.uniform(130, 260)
        x, y = math.cos(angle) * radius, math.sin(angle) * radius
        if abs(x) < 175 and abs(y + 20) < 150:
            continue
        if abs(x + 78) < 18 and -300 < y < 60:
            continue
        z = block.terrain_height(x, y)
        add_tree_high(f"GEO-Aypate_HighTree_{i}", x, y, z, rng.uniform(0.65, 1.1), tree_mats, lod1_exclude=(i % 2 == 1))
    for i in range(58):
        angle = rng.uniform(0, math.tau)
        radius = rng.uniform(120, 230)
        x, y = math.cos(angle) * radius, math.sin(angle) * radius
        if abs(x + 78) < 18 and -300 < y < 60:
            continue
        z = block.terrain_height(x, y)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=rng.uniform(0.35, 0.8), location=(x, y, z + 0.3))
        shrub = bpy.context.object
        shrub.name = f"GEO-Aypate_HighShrub_{i}"
        shrub.scale.z = rng.uniform(0.35, 0.7)
        shrub.data.materials.append(mats["MAT-Aypate_LeafDark"] if i % 2 else mats["MAT-Aypate_Leaf"])
        shrub["layer"] = "props"
        shrub["lod1_exclude"] = True
        add_to(shrub, "COL-Aypate_Props")
    scene = bpy.context.scene
    scene.render.filepath = HERO
    bpy.ops.render.render(write_still=True)
    bpy.ops.wm.save_as_mainfile(filepath=OUT)
    print("AYPATE_HIGHPOLY_OK", OUT, HERO)


if __name__ == "__main__":
    main()
