"""Genera el blockout interpretativo v0.1 de Narihualá.

Uso:
  blender --background --python scripts/build_narihuala_blockout.py

El montículo este y la capilla se apoyan en la lectura libre de SIGRID 2018
(ortofoto 3,8 cm y DTM 0,19 m). El montículo oeste, la plaza de 60 x 40 m y
las rampas son inferencias explícitas a partir de RVM 2023, Mincetur 364 y
Fernández Villegas 1990. No se copia la ortofoto ni se presenta esto como un
levantamiento arqueológico.
"""

import math
import os
import random
import sys

import bpy
from mathutils import Vector

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import build_aypate_blockout as base  # noqa: E402

OUT_BLEND = os.path.join(ROOT, "blender", "narihuala", "narihuala_blockout_v0.1.blend")
HERO = "/tmp/narihuala_blockout_v0.1.jpg"
SEED = 8451
TERRAIN_SIZE = 600
TERRAIN_N = 100
PLAZA_Z = 30.0


def terrain_height(x, y):
    """Terreno de valle con dos montículos; el este sigue la lectura SIGRID."""
    base_z = 20.0 + 0.55 * math.sin(x * 0.018) * math.cos(y * 0.021)
    base_z += 0.35 * math.sin((x + y) * 0.047)
    core = math.exp(-((x / 165.0) ** 4 + ((y - 5.0) / 155.0) ** 4))
    east = 15.0 * math.exp(-(((x - 75.0) / 42.0) ** 2 + ((y - 5.0) / 50.0) ** 2))
    west = 8.0 * math.exp(-(((x + 95.0) / 38.0) ** 2 + ((y - 5.0) / 45.0) ** 2))
    return base_z + 8.0 * core + east + west


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
            uv.data[loop].uv = ((co.x + size / 2) / 42.0, (co.y + size / 2) / 42.0)
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
    base.box("GEO-Narihuala_Plaza", (60, 40, 0.5), (-10, 0, PLAZA_Z - 0.25), mats["sand"], "city", 6.0, 0.02)
    base.wall_x("GEO-Narihuala_Plaza_N", -40, 20, 20, PLAZA_Z + 0.1, 1.1, 0.8, mats["adobe"], [(0, 8.0)], "city")
    base.wall_x("GEO-Narihuala_Plaza_S", -40, 20, -20, PLAZA_Z + 0.1, 1.1, 0.8, mats["adobe"], [(0, 8.0)], "city")
    base.wall_y("GEO-Narihuala_Plaza_W", -40, -20, 20, PLAZA_Z + 0.1, 1.1, 0.8, mats["adobe"], [(-5, 8.0)], "city")
    base.wall_y("GEO-Narihuala_Plaza_E", 20, -20, 20, PLAZA_Z + 0.1, 1.1, 0.8, mats["adobe"], [(0, 8.0)], "city")

    # Montículo oeste: dos plataformas inferidas, ocultas en parte por el museo.
    base.box("GEO-Narihuala_West_Base", (75, 85, 4.0), (-95, 5, 30.0), mats["adobe"], "city", 8.0, 0.04)
    base.box("GEO-Narihuala_West_Mid", (55, 65, 4.0), (-95, 5, 33.0), mats["adobe"], "city", 8.0, 0.04)
    base.box("GEO-Narihuala_West_Top", (35, 45, 3.5), (-95, 5, 36.25), mats["adobe"], "city", 7.0, 0.04)
    base.stairs("GEO-Narihuala_West_Stairs", (-60, 5, 30.0), 4.0, 0.75, 0.30, 26, "x", mats["adobe"])
    base.wall_y("GEO-Narihuala_West_Front", -77.5, -35, 45, 37.5, 2.0, 0.9, mats["adobe"], [(5, 4.0)], "city")

    # Montículo este: tres plataformas y terraza superior, lectura SIGRID.
    base.box("GEO-Narihuala_East_Base", (100, 110, 5.0), (75, 5, 30.5), mats["adobe"], "city", 8.0, 0.04)
    base.box("GEO-Narihuala_East_Mid", (75, 85, 5.0), (75, 5, 34.5), mats["adobe"], "city", 8.0, 0.04)
    base.box("GEO-Narihuala_East_Top", (50, 60, 7.0), (75, 5, 41.5), mats["adobe"], "city", 7.0, 0.04)
    base.stairs("GEO-Narihuala_East_Stairs", (25, 5, 30.0), 5.0, 0.9, 0.55, 28, "x", mats["adobe"])
    base.wall_y("GEO-Narihuala_East_Front", 50, -25, 35, 45.0, 2.2, 1.0, mats["adobe"], [(5, 5.0)], "city")
    base.wall_y("GEO-Narihuala_East_Back", 100, -25, 35, 45.0, 2.2, 1.0, mats["adobe"], layer="city")
    base.wall_x("GEO-Narihuala_East_N", 50, 100, 35, 45.0, 2.2, 1.0, mats["adobe"], layer="city")
    base.wall_x("GEO-Narihuala_East_S", 50, 100, -25, 45.0, 2.2, 1.0, mats["adobe"], layer="city")

    # Rampas desde la plaza a los dos montículos.
    ramp("GEO-Narihuala_Ramp_East", (35, 0, 0), (22, 10, 5.0), 30.0, 33.0, "x", mats["sand"], "city")
    ramp("GEO-Narihuala_Ramp_West", (-70, 0, 0), (22, 10, 4.0), 30.0, 32.0, "x", mats["sand"], "city")

    # Sector II: tres hileras de muros paralelos y corredores.
    for i, y in enumerate((-8, 0, 8)):
        base.wall_x(f"GEO-Narihuala_SectorII_Wall_{i}", -40, 20, y, PLAZA_Z + 0.1, 1.4, 0.7, mats["adobe"], [(-20, 4.0)], "city")
    base.box("GEO-Narihuala_SectorII_Patio", (36, 22, 0.2), (-10, 0, PLAZA_Z + 0.1), mats["sand"], "props", 4.0, 0.01, True)

    # Camino de acceso desde el sur.
    for i in range(28):
        y = -235 + i * 7
        x = -10
        z = terrain_height(x, y) + 0.25
        base.box(f"GEO-Narihuala_Path_{i}", (8, 7.2, 0.18), (x, y, z), mats["sand"], "props", 3.0, 0.01, True)
    base.wall_y("GEO-Narihuala_Path_W", -17, -240, -40, 0, 0.8, 0.6, mats["adobe"], layer="props")

    # Capilla republicana: capa later, oculta por defecto.
    base.box("GEO-Narihuala_Chapel", (10, 16, 4.0), (75, 5, 45.0), mats["plaster"], "later", 4.0, 0.03)
    base.box("GEO-Narihuala_Chapel_Roof", (12, 18, 1.0), (75, 5, 47.5), mats["stone"], "later", 4.0, 0.02)
    base.box("GEO-Narihuala_Chapel_Door", (2.5, 0.4, 2.8), (75, -3.2, 44.8), mats["wood"], "later", 1.0, 0.01, True)

    # Rocas, arbustos y bosque seco.
    rng = random.Random(SEED)
    for i in range(70):
        angle = rng.uniform(0, math.tau)
        radius = rng.uniform(155, 290)
        x, y = math.cos(angle) * radius, math.sin(angle) * radius
        if abs(x) < 130 and abs(y) < 130:
            continue
        z = terrain_height(x, y)
        base.tree(f"GEO-Narihuala_Tree_{i}", x, y, z, rng.uniform(0.7, 1.25), mats, lod1_exclude=(i % 2 == 1))
    for i in range(45):
        x = rng.uniform(-150, 150)
        y = rng.uniform(-150, 150)
        if abs(x) < 105 and abs(y) < 100:
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
    for i in range(35):
        x = rng.uniform(-120, 120)
        y = rng.uniform(-120, 120)
        if abs(x) < 80 and abs(y) < 75:
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

    for i, (x, y) in enumerate(((-25, -8), (5, 10), (30, -5), (68, 20), (-95, 30), (75, -35))):
        base.human(f"GEO-Narihuala_Human_{i + 1}", x, y, terrain_height(x, y) + 0.15, mats)

    # Lighting.
    sun_data = bpy.data.lights.new("LGT-Narihuala_Sun", "SUN")
    sun_data.energy = 3.2
    sun_data.angle = math.radians(7)
    sun_data.color = (1.0, 0.90, 0.76)
    sun = bpy.data.objects.new("LGT-Narihuala_Sun", sun_data)
    scene.collection.objects.link(sun)
    sun.rotation_euler = (math.radians(42), math.radians(-18), math.radians(-38))
    fill_data = bpy.data.lights.new("LGT-Narihuala_Fill", "AREA")
    fill_data.energy = 1100
    fill_data.shape = "DISK"
    fill_data.size = 180
    fill_data.color = (0.65, 0.78, 0.90)
    fill = bpy.data.objects.new("LGT-Narihuala_Fill", fill_data)
    scene.collection.objects.link(fill)
    fill.location = (0, -180, 100)
    fill.rotation_euler = (Vector((0, 0, 10)) - fill.location).to_track_quat("-Z", "Y").to_euler()

    # Cameras: viewer x = model x * 0.08; viewer z = -model y * 0.08.
    camera_defs = {
        "Hero": ((170, -210, 75), (0, 0, 30), 45),
        "Tour1": ((0, -250, 12), (0, -180, 10), 42),
        "Tour2": ((-95, -230, 45), (-95, 5, 32), 42),
        "Tour3": ((-10, -170, 50), (-10, 0, 30), 40),
        "Tour4": ((30, -190, 50), (10, 0, 32), 42),
        "Tour5": ((75, -230, 55), (75, 0, 40), 45),
        "Tour6": ((180, 180, 80), (0, 0, 30), 40),
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
