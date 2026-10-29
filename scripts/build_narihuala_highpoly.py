"""Sube el blockout de Narihualá a un pase high-poly v0.1.

Uso:
  blender --background blender/narihuala/narihuala_blockout_v0.1.blend \
    --python scripts/build_narihuala_highpoly.py

Añade cursos de adobe, erosión, vegetación y texturas 2K. No inventa techos ni
recintos: el montículo oeste y la plaza siguen siendo inferencias explícitas.
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
import build_aypate_blockout as base  # noqa: E402

OUT = os.path.join(ROOT, "blender", "narihuala", "narihuala_highpoly_v0.1.blend")
HERO = "/tmp/narihuala_highpoly_v0.1.jpg"
SEED = 91357
rng = random.Random(SEED)


def add_to(obj, col_name):
    for col in list(obj.users_collection):
        col.objects.unlink(obj)
    bpy.data.collections[col_name].objects.link(obj)


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


def make_block_mesh(name, verts, faces, mat_indices, materials, layer="city"):
    mesh = bpy.data.meshes.new(f"MESH-{name}")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    for mat in materials:
        mesh.materials.append(mat)
    for poly, index in zip(mesh.polygons, mat_indices):
        poly.material_index = index
    obj = bpy.data.objects.new(name, mesh)
    bpy.data.collections[f"COL-Narihuala_{layer.title()}"].objects.link(obj)
    obj["layer"] = layer
    obj["lod1_exclude"] = False
    base.uv_cube(obj, 2.5)
    return obj


def adobe_courses(obj, adobe, adobe_dark, max_blocks=900):
    if obj.type != "MESH" or obj.name.startswith("GEO-Narihuala_Courses"):
        return 0
    if not any(k in obj.name for k in ("East", "West", "Plaza", "SectorII")):
        return 0
    dx, dy, dz = obj.dimensions
    if dz < 0.8 or min(dx, dy) < 0.7:
        return 0
    loc = obj.location
    x0, x1 = loc.x - dx / 2, loc.x + dx / 2
    y0, y1 = loc.y - dy / 2, loc.y + dy / 2
    z0, z1 = loc.z - dz / 2, loc.z + dz / 2
    verts, faces, indices = [], [], []
    blocks = 0
    if dx >= dy:
        for y_face, sign in ((y0, -1), (y1, 1)):
            cols = max(1, int(dx / 1.25))
            rows = max(1, int(dz / 0.38))
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
                    yy = y_face + sign * 0.045
                    box_face(verts, faces, indices, (x, yy, z), (w, 0.09, h * 0.82), 0 if rng.random() < 0.72 else 1)
                    blocks += 1
    else:
        for x_face, sign in ((x0, -1), (x1, 1)):
            cols = max(1, int(dy / 1.25))
            rows = max(1, int(dz / 0.38))
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
                    xx = x_face + sign * 0.045
                    box_face(verts, faces, indices, (xx, y, z), (0.09, w, h * 0.82), 0 if rng.random() < 0.72 else 1)
                    blocks += 1
    if blocks:
        make_block_mesh(f"GEO-Narihuala_Courses_{obj.name.replace('GEO-Narihuala_', '')}", verts, faces, indices, [adobe, adobe_dark])
    return blocks


def add_tree_high(name, x, y, z, scale, mats, lod1_exclude=False):
    parts = []
    trunk_h = 4.2 * scale
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.22 * scale, depth=trunk_h, location=(x, y, z + trunk_h / 2))
    trunk = bpy.context.object
    trunk.name = f"{name}_trunk"
    trunk.data.materials.append(mats["wood"])
    parts.append(trunk)
    for i, (dx, dy, dz, rad) in enumerate(((0, 0, trunk_h + 1.8 * scale, 2.5 * scale), (-1.2, 0.6, trunk_h + 1.2 * scale, 1.8 * scale), (1.1, -0.5, trunk_h + 1.4 * scale, 1.7 * scale), (0.2, 1.0, trunk_h + 2.8 * scale, 1.3 * scale))):
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
    add_to(obj, "COL-Narihuala_Props")


def replace_textures():
    mappings = (
        ("MAT-Narihuala_Adobe", "Adobe2K", 8451, (0.43, 0.29, 0.19), (0.66, 0.48, 0.32), "stone"),
        ("MAT-Narihuala_Sand", "Sand2K", 8471, (0.34, 0.27, 0.18), (0.56, 0.45, 0.30), "ground"),
        ("MAT-Narihuala_Stone", "Stone2K", 8491, (0.30, 0.27, 0.22), (0.55, 0.50, 0.41), "stone"),
    )
    for mat_name, label, seed, base_c, accent, kind in mappings:
        mat = bpy.data.materials.get(mat_name)
        if mat is None:
            continue
        diffuse, rough, normal = base.texture_set(label, seed, base_c, accent, kind, 2048)
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
        print("NARIHUALA_TEXTURE_2K", mat_name)


def main():
    bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, "blender", "narihuala", "narihuala_blockout_v0.1.blend"))
    replace_textures()
    mats = {name: bpy.data.materials[name] for name in ("MAT-Narihuala_Adobe", "MAT-Narihuala_Sand", "MAT-Narihuala_Stone", "MAT-Narihuala_Wood", "MAT-Narihuala_Leaf", "MAT-Narihuala_LeafDark")}
    # Adobe courses on architectural volumes.
    total = 0
    for obj in list(bpy.data.objects):
        if obj.type == "MESH" and any(c.name == "COL-Narihuala_City" for c in obj.users_collection):
            total += adobe_courses(obj, mats["MAT-Narihuala_Adobe"], mats["MAT-Narihuala_Stone"])
    print("NARIHUALA_COURSES", total)
    # High-detail dry forest.
    tree_mats = {"wood": mats["MAT-Narihuala_Wood"], "leaf": mats["MAT-Narihuala_Leaf"], "leaf_dark": mats["MAT-Narihuala_LeafDark"]}
    for i in range(40):
        angle = rng.uniform(0, math.tau)
        radius = rng.uniform(125, 250)
        x, y = math.cos(angle) * radius, math.sin(angle) * radius
        if abs(x) < 110 and abs(y) < 110:
            continue
        z = 20.0 + 0.55 * math.sin(x * 0.018) * math.cos(y * 0.021)
        # use blockout height approximation for placement
        z = max(z, 20.0)
        add_tree_high(f"GEO-Narihuala_HighTree_{i}", x, y, z, rng.uniform(0.65, 1.1), tree_mats, lod1_exclude=(i % 2 == 1))
    for i in range(55):
        angle = rng.uniform(0, math.tau)
        radius = rng.uniform(115, 220)
        x, y = math.cos(angle) * radius, math.sin(angle) * radius
        z = 20.0
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=rng.uniform(0.35, 0.9), location=(x, y, z + 0.4))
        shrub = bpy.context.object
        shrub.name = f"GEO-Narihuala_HighShrub_{i}"
        shrub.scale.z = rng.uniform(0.35, 0.7)
        shrub.data.materials.append(mats["MAT-Narihuala_LeafDark"] if i % 2 else mats["MAT-Narihuala_Leaf"])
        shrub["layer"] = "props"
        shrub["lod1_exclude"] = True
        add_to(shrub, "COL-Narihuala_Props")
    scene = bpy.context.scene
    later = bpy.data.collections.get("COL-Narihuala_Later")
    if later:
        later.hide_render = True
        later.hide_viewport = True
        for obj in later.objects:
            obj.hide_render = True
            obj.hide_set(True)
    scene.camera = bpy.data.objects["CAM-Narihuala_Hero"]
    scene.render.filepath = HERO
    bpy.ops.render.render(write_still=True)
    bpy.ops.wm.save_as_mainfile(filepath=OUT)
    print("NARIHUALA_HIGHPOLY_OK", OUT, HERO)


if __name__ == "__main__":
    main()
