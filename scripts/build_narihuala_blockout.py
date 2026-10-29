"""Genera el blockout interpretativo v0.2 de Narihualá.

Uso:
  blender --background --python scripts/build_narihuala_blockout.py

El montículo este y la capilla se apoyan en la lectura libre de SIGRID 2018
(ortofoto 3,8 cm y DTM 0,19 m). El montículo oeste, la plaza de 60 x 40 m y
las rampas son inferencias explícitas a partir de RVM 2023, Mincetur 364 y
Fernández Villegas 1990. No se copia la ortofoto ni se presenta esto como un
levantamiento arqueológico.
"""

import json
import math
import os
import random
import sys

import bpy
from mathutils import Vector

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import build_aypate_blockout as base  # noqa: E402

OUT_BLEND = os.path.join(ROOT, "blender", "narihuala", "narihuala_blockout_v0.2.blend")
HERO = "/tmp/narihuala_blockout_v0.2.jpg"
SEED = 8451
TERRAIN_SIZE = 600
TERRAIN_N = 120
PLAZA_Z = 37.5
HEIGHTMAP = json.loads(open(os.path.join(ROOT, "blender", "narihuala", "terrain_heightmap.json")).read())


def terrain_height(x, y):
    """Terreno del núcleo desde el DTM SIGRID; valle suave fuera del recorte."""
    size = HEIGHTMAP["size_m"]
    n = HEIGHTMAP["n"]
    if -size / 2 <= x <= size / 2 and -size / 2 <= y <= size / 2:
        u = (x + size / 2) / size * (n - 1)
        v = (size / 2 - y) / size * (n - 1)
        i = min(n - 2, max(0, int(u)))
        j = min(n - 2, max(0, int(v)))
        fx = u - i
        fy = v - j
        z = HEIGHTMAP["z"]
        a = z[j][i] * (1 - fx) + z[j][i + 1] * fx
        b = z[j + 1][i] * (1 - fx) + z[j + 1][i + 1] * fx
        return a * (1 - fy) + b * fy
    # Borde del recorte: valle agrícola suave, sin inventar montículos.
    cx = max(-size / 2, min(size / 2, x))
    cy = max(-size / 2, min(size / 2, y))
    edge = terrain_height(cx, cy) if (cx != x or cy != y) else 24.0
    return edge + 0.35 * math.sin(x * 0.025) * math.cos(y * 0.022)


def terrain(mats):
    size = TERRAIN_SIZE
    n = TERRAIN_N
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
    mesh = bpy.data.meshes.new("MESH-Narihuala_Terrain")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new("GEO-Narihuala_Terrain", mesh)
    base.bucket("Terrain").objects.link(obj)
    obj.data.materials.append(mats["sand"])
    uv = mesh.uv_layers.new(name="UVMap")
    for poly in mesh.polygons:
        for loop in poly.loop_indices:
            co = mesh.vertices[mesh.loops[loop].vertex_index].co
            uv.data[loop].uv = ((co.x + size / 2) / 260.0, (co.y + size / 2) / 260.0)
    obj["layer"] = "terrain"
    return obj


def make_materials():
    adobe = base.texture_set("Adobe", SEED, (0.43, 0.29, 0.19), (0.66, 0.48, 0.32), "stone")
    sand = base.texture_set("Sand", SEED + 20, (0.34, 0.27, 0.18), (0.56, 0.45, 0.30), "ground")
    stone = base.texture_set("Stone", SEED + 40, (0.30, 0.27, 0.22), (0.55, 0.50, 0.41), "stone")
    wood = base.material("MAT-Narihuala_Wood", color=(0.18, 0.11, 0.06, 1.0), roughness_value=0.9)
    leaf = base.material("MAT-Narihuala_Leaf", color=(0.10, 0.22, 0.08, 1.0), roughness_value=0.92)
    leaf_dark = base.material("MAT-Narihuala_LeafDark", color=(0.05, 0.13, 0.045, 1.0), roughness_value=0.94)
    mats = {
        "adobe": base.material("MAT-Narihuala_Adobe", *adobe),
        "sand": base.material("MAT-Narihuala_Sand", *sand),
        "stone": base.material("MAT-Narihuala_Stone", *stone),
        "wood": wood,
        "leaf": leaf,
        "leaf_dark": leaf_dark,
        "plaster": base.material("MAT-Narihuala_Plaster", color=(0.66, 0.61, 0.50, 1.0), roughness_value=0.88),
        "water": base.material("MAT-Narihuala_Water", color=(0.08, 0.24, 0.26, 1.0), roughness_value=0.25),
    }
    mats["ground"] = mats["sand"]
    return mats



def terrace(name, points, z_top, thickness, mat, layer="city"):
    """Plataforma de contorno irregular con talud inferior, no una caja."""
    cx = sum(p[0] for p in points) / len(points)
    cy = sum(p[1] for p in points) / len(points)
    top = [(x, y, z_top) for x, y in points]
    bottom = [(cx + (x - cx) * 1.06, cy + (y - cy) * 1.06, z_top - thickness) for x, y in points]
    verts = top + bottom
    n = len(points)
    faces = [tuple(range(n - 1, -1, -1)), tuple(range(n, 2 * n))]
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
    mesh = bpy.data.meshes.new(f"MESH-{name}")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    base.bucket(layer.title()).objects.link(obj)
    obj.data.materials.append(mat)
    base.uv_cube(obj, 4.0)
    base.bevel(obj, 0.06)
    obj["layer"] = layer
    obj["lod1_exclude"] = False
    return obj

def ramp(name, center, size, z0, z1, axis, mat, layer="city"):
    sx, sy, sz = (v / 2 for v in size)
    verts = [
        (-sx, -sy, z0), (sx, -sy, z0), (sx, sy, z0), (-sx, sy, z0),
        (-sx, -sy, z1), (sx, -sy, z1), (sx, sy, z1), (-sx, sy, z1),
    ]
    # A wedge: one end at z0, the other at z1.
    if axis == "x":
        verts[4] = (-sx, -sy, z0)
        verts[5] = (sx, -sy, z1)
        verts[6] = (sx, sy, z1)
        verts[7] = (-sx, sy, z0)
    else:
        verts[4] = (-sx, -sy, z0)
        verts[5] = (sx, -sy, z0)
        verts[6] = (sx, sy, z1)
        verts[7] = (-sx, sy, z1)
    faces = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    mesh = bpy.data.meshes.new(f"MESH-{name}")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    base.bucket(layer.title()).objects.link(obj)
    obj.location = center
    obj.data.materials.append(mat)
    base.uv_cube(obj, 4.0)
    base.bevel(obj, 0.03)
    obj["layer"] = layer
    obj["lod1_exclude"] = False
    return obj


def main():
    scene = base.clean_scene()
    for name in ("City", "Terrain", "Props", "Reference", "Later"):
        col = bpy.data.collections.new(f"COL-Narihuala_{name}")
        scene.collection.children.link(col)
    base.bucket = lambda name: bpy.data.collections[f"COL-Narihuala_{name}"]
    mats = make_materials()
    terrain(mats)

    # Plaza central de 60 x 40 m, entre los dos montículos.
    terrace("GEO-Narihuala_Plaza", [(-45, -10), (15, -10), (15, 30), (-45, 30)], PLAZA_Z, 0.7, mats["sand"])
    base.wall_x("GEO-Narihuala_Plaza_N", -45, 15, 30, PLAZA_Z + 0.1, 1.0, 0.8, mats["adobe"], [(0, 8.0)], "city")
    base.wall_x("GEO-Narihuala_Plaza_S", -45, 15, -10, PLAZA_Z + 0.1, 1.0, 0.8, mats["adobe"], [(0, 8.0)], "city")
    base.wall_y("GEO-Narihuala_Plaza_W", -45, -10, 30, PLAZA_Z + 0.1, 1.0, 0.8, mats["adobe"], [(-5, 8.0)], "city")
    base.wall_y("GEO-Narihuala_Plaza_E", 15, -10, 30, PLAZA_Z + 0.1, 1.0, 0.8, mats["adobe"], [(0, 8.0)], "city")

    # Montículo oeste: plataformas inferidas, ocultas en parte por el museo.
    west_base = [(-90, 45), (-30, 50), (-25, -40), (-85, -45)]
    west_mid = [(-85, 35), (-35, 40), (-30, -30), (-80, -35)]
    west_top = [(-75, 25), (-45, 30), (-40, -20), (-70, -25)]
    terrace("GEO-Narihuala_West_Base", west_base, 30.0, 3.0, mats["adobe"])
    terrace("GEO-Narihuala_West_Mid", west_mid, 33.0, 3.0, mats["adobe"])
    terrace("GEO-Narihuala_West_Top", west_top, 37.0, 3.0, mats["adobe"])
    base.stairs("GEO-Narihuala_West_Stairs", (-95, 5, 30.0), 4.0, 0.8, 0.28, 25, "x", mats["adobe"])
    base.wall_y("GEO-Narihuala_West_Front", -75, -25, 30, 37.0, 1.8, 0.9, mats["adobe"], [(5, 4.0)], "city")

    # Montículo este: tres plataformas de contorno irregular y terraza superior.
    east_base = [(-20, 55), (80, 60), (85, -45), (-15, -50)]
    east_mid = [(-10, 45), (65, 50), (70, -35), (0, -40)]
    east_top = [(5, 35), (55, 40), (60, -25), (10, -30)]
    terrace("GEO-Narihuala_East_Base", east_base, 31.0, 3.0, mats["adobe"])
    terrace("GEO-Narihuala_East_Mid", east_mid, 37.0, 4.0, mats["adobe"])
    terrace("GEO-Narihuala_East_Top", east_top, 44.0, 4.0, mats["adobe"])
    base.stairs("GEO-Narihuala_East_Stairs", (-15, 5, 37.5), 5.0, 0.9, 0.34, 20, "x", mats["adobe"])
    base.wall_y("GEO-Narihuala_East_Front", 5, -25, 35, 44.0, 1.8, 1.0, mats["adobe"], [(5, 5.0)], "city")
    base.wall_y("GEO-Narihuala_East_Back", 60, -25, 35, 44.0, 1.8, 1.0, mats["adobe"], layer="city")
    base.wall_x("GEO-Narihuala_East_N", 5, 60, 35, 44.0, 1.8, 1.0, mats["adobe"], layer="city")
    base.wall_x("GEO-Narihuala_East_S", 5, 60, -25, 44.0, 1.8, 1.0, mats["adobe"], layer="city")

    # Rampas desde la plaza a los dos montículos.
    ramp("GEO-Narihuala_Ramp_East", (0, 10, 0), (20, 10, 5.0), 37.5, 39.0, "x", mats["sand"], "city")
    ramp("GEO-Narihuala_Ramp_West", (-60, 10, 0), (20, 10, 4.0), 37.5, 38.5, "x", mats["sand"], "city")

    # Sector II: tres hileras de muros paralelos y corredores.
    for i, y in enumerate((-8, 0, 8)):
        base.wall_x(f"GEO-Narihuala_SectorII_Wall_{i}", -45, 15, y, PLAZA_Z + 0.1, 1.2, 0.7, mats["adobe"], [(-20, 4.0)], "city")
    base.box("GEO-Narihuala_SectorII_Patio", (40, 22, 0.2), (-15, 10, PLAZA_Z + 0.1), mats["sand"], "props", 4.0, 0.01, True)

    # Camino de acceso desde el sur.
    for i in range(28):
        y = -235 + i * 7
        x = -15
        z = terrain_height(x, y) + 0.25
        base.box(f"GEO-Narihuala_Path_{i}", (8, 7.2, 0.18), (x, y, z), mats["sand"], "props", 3.0, 0.01, True)
    base.wall_y("GEO-Narihuala_Path_W", -22, -240, -40, 0, 0.8, 0.6, mats["adobe"], layer="props")

    # Capilla republicana: capa later, oculta por defecto.
    base.box("GEO-Narihuala_Chapel", (10, 16, 4.0), (30, 5, 46.0), mats["plaster"], "later", 4.0, 0.03)
    base.box("GEO-Narihuala_Chapel_Roof", (12, 18, 1.0), (30, 5, 48.5), mats["stone"], "later", 4.0, 0.02)
    base.box("GEO-Narihuala_Chapel_Door", (2.5, 0.4, 2.8), (30, -3.2, 45.8), mats["wood"], "later", 1.0, 0.01, True)

    # Rocas, arbustos y bosque seco.
    rng = random.Random(SEED)
    for i in range(85):
        angle = rng.uniform(0, math.tau)
        radius = rng.uniform(150, 290)
        x, y = math.cos(angle) * radius, math.sin(angle) * radius
        if abs(x) < 115 and abs(y) < 105:
            continue
        z = terrain_height(x, y)
        base.tree(f"GEO-Narihuala_Tree_{i}", x, y, z, rng.uniform(0.7, 1.25), mats, lod1_exclude=(i % 2 == 1))
    for i in range(55):
        x = rng.uniform(-150, 150)
        y = rng.uniform(-150, 150)
        if abs(x) < 105 and abs(y) < 95:
            continue
        z = terrain_height(x, y)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=rng.uniform(0.35, 0.9), location=(x, y, z + 0.35))
        shrub = bpy.context.object
        shrub.name = f"GEO-Narihuala_Shrub_{i}"
        shrub.scale.z = rng.uniform(0.4, 0.8)
        shrub.data.materials.append(mats["leaf_dark"] if i % 2 else mats["leaf"])
        shrub["layer"] = "props"
        shrub["lod1_exclude"] = True
        base.add_to(shrub, base.bucket("Props"))
    for i in range(40):
        x = rng.uniform(-120, 120)
        y = rng.uniform(-120, 120)
        if abs(x) < 75 and abs(y) < 70:
            continue
        z = terrain_height(x, y)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=rng.uniform(0.4, 1.2), location=(x, y, z + 0.25))
        rock = bpy.context.object
        rock.name = f"GEO-Narihuala_Rock_{i}"
        rock.scale.z = rng.uniform(0.35, 0.7)
        rock.data.materials.append(mats["stone"] if i % 3 else mats["adobe"])
        rock["layer"] = "props"
        rock["lod1_exclude"] = i % 2 == 0
        base.add_to(rock, base.bucket("Props"))

    for i, (x, y) in enumerate(((-30, -8), (5, 10), (25, -5), (50, 20), (-60, 30), (30, -35))):
        base.human(f"GEO-Narihuala_Human_{i + 1}", x, y, terrain_height(x, y) + 0.15, mats)

    # Lighting.
    sun_data = bpy.data.lights.new("LGT-Narihuala_Sun", "SUN")
    sun_data.energy = 2.7
    sun_data.angle = math.radians(5)
    sun_data.color = (1.0, 0.82, 0.63)
    sun = bpy.data.objects.new("LGT-Narihuala_Sun", sun_data)
    scene.collection.objects.link(sun)
    sun.rotation_euler = (math.radians(24), math.radians(-20), math.radians(-36))
    fill_data = bpy.data.lights.new("LGT-Narihuala_Fill", "AREA")
    fill_data.energy = 700
    fill_data.shape = "DISK"
    fill_data.size = 200
    fill_data.color = (0.62, 0.76, 0.92)
    fill = bpy.data.objects.new("LGT-Narihuala_Fill", fill_data)
    scene.collection.objects.link(fill)
    fill.location = (0, -180, 100)
    fill.rotation_euler = (Vector((0, 0, 10)) - fill.location).to_track_quat("-Z", "Y").to_euler()

    # Cameras: viewer x = model x * 0.08; viewer z = -model y * 0.08.
    camera_defs = {
        "Hero": ((160, -240, 80), (0, 0, 35), 45),
        "Tour1": ((0, -250, 15), (0, -170, 20), 42),
        "Tour2": ((-60, -250, 60), (-60, 5, 33), 42),
        "Tour3": ((-15, -220, 65), (-15, 10, 38), 40),
        "Tour4": ((15, -220, 55), (0, 5, 36), 42),
        "Tour5": ((30, -260, 70), (30, 10, 42), 45),
        "Tour6": ((160, 160, 80), (0, 0, 35), 40),
    }
    for name, (pos, target, lens) in camera_defs.items():
        cam_data = bpy.data.cameras.new(f"CAM-Narihuala_{name}")
        cam_data.lens = lens
        cam = bpy.data.objects.new(f"CAM-Narihuala_{name}", cam_data)
        scene.collection.objects.link(cam)
        cam.location = pos
        cam.rotation_euler = (Vector(target) - cam.location).to_track_quat("-Z", "Y").to_euler()
    scene.camera = bpy.data.objects["CAM-Narihuala_Hero"]
    later = bpy.data.collections.get("COL-Narihuala_Later")
    if later:
        later.hide_render = True
        later.hide_viewport = True
        for obj in later.objects:
            obj.hide_render = True
            obj.hide_set(True)
    scene.render.filepath = HERO
    bpy.ops.render.render(write_still=True)

    os.makedirs(os.path.dirname(OUT_BLEND), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
    for name in ("City", "Terrain", "Props", "Reference", "Later"):
        col = bpy.data.collections.get(f"COL-Narihuala_{name}")
        count = sum(len(o.data.loop_triangles) for o in col.objects if o.type == "MESH") if col else 0
        print(f"NARIHUALA_{name.upper()}_TRIS {count}")
    print("NARIHUALA_BLOCKOUT_OK", OUT_BLEND, HERO)


if __name__ == "__main__":
    main()
