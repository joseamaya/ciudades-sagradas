"""Genera el blockout v0.4 de Aypate con escala y lectura corregidas.

Uso:
  blender --background --python scripts/build_aypate_blockout_v0_3.py

El plano base es el levantamiento topográfico y arquitectónico publicado como
figura 1 en Campos Napán (2017). La escena usa +X = este y +Y = norte.
No copia la figura: solo usa sus relaciones espaciales.
"""

import math
import os
import random
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_aypate_blockout import *  # noqa: F403,E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_BLEND = os.path.join(ROOT, "blender", "aypate", "aypate_blockout_v0.4.blend")
HERO = "/tmp/aypate_blockout_v04.jpg"
SEED = 7319
PLAZA_Z = 8.0


def terrain_height(x, y):
    # Terraza monumental de ~500 x 300 m; el resto baja hacia el bosque.
    dx = max(0, abs(x) - 250)
    dy = max(0, abs(y + 20) - 150)
    d = math.hypot(dx, dy)
    plateau = 1.0 if d <= 0 else max(0.0, 1.0 - d / 120)
    # El Qhapaq Ñan y la fuente deben quedar sobre una rasante plana.
    corridor = 1.0 if abs(x + 78) < 30 and -285 < y < 55 else 0.0
    flat = max(plateau, corridor)
    z = PLAZA_Z - 7.0 * (1 - flat) + 0.22 * math.sin(x * 0.026) * math.cos(y * 0.021) * (1 - flat)
    hills = (
        38 * math.exp(-(((x - 300) / 110) ** 2 + ((y + 20) / 180) ** 2))
        + 30 * math.exp(-(((x + 310) / 120) ** 2 + ((y - 40) / 170) ** 2))
        + 44 * math.exp(-(((x + 30) / 180) ** 2 + ((y + 310) / 110) ** 2))
        + 24 * math.exp(-(((x - 20) / 160) ** 2 + ((y - 310) / 120) ** 2))
    )
    z += hills * (1 - flat)
    return z


def terrain_v03(mats):
    size = 600
    n = 110
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
            uv.data[loop].uv = ((co.x + size / 2) / 220.0, (co.y + size / 2) / 220.0)
    obj["layer"] = "terrain"
    return obj


PLAZA_POLY = [(-69.0, 44.0), (69.0, 32.0), (58.0, -50.0), (-58.0, -44.0)]


def plateau_polygon(name, points, z0, thickness, mat, layer="city"):
    verts = []
    for x, y in points:
        verts.append((x, y, z0))
    for x, y in points:
        verts.append((x, y, z0 + thickness))
    n = len(points)
    faces = []
    faces.append(tuple(range(n - 1, -1, -1)))
    faces.append(tuple(range(n, 2 * n)))
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
    mesh = bpy.data.meshes.new(f"MESH-{name}")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bucket(layer.title()).objects.link(obj)
    obj.data.materials.append(mat)
    obj["layer"] = layer
    obj["lod1_exclude"] = False
    return obj


def main():
    scene = clean_scene()
    for name in ("City", "Terrain", "Props", "Reference", "Later"):
        bucket(name)
    mats = make_materials()
    clay = texture_set("Clay", SEED + 80, (0.42, 0.25, 0.18), (0.62, 0.39, 0.26), "stone")
    mats["clay"] = material("MAT-Aypate_Clay", *clay)
    water_bsdf = next(n for n in mats["water"].node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    water_bsdf.inputs["Base Color"].default_value = (0.08, 0.32, 0.35, 1.0)
    water_bsdf.inputs["Roughness"].default_value = 0.12
    terrain_v03(mats)

    # Plaza Inca: 140 x 100 m, with the Qhapaq Ñan on its west side.
    plateau_polygon("GEO-Aypate_Plaza", PLAZA_POLY, PLAZA_Z - 0.075, 0.35, mats["clay"], "city")
    # Muro perimetral bajo documentado; los vanos coinciden con los accesos.
    wall_x("GEO-Aypate_Plaza_Parapet_S", -58, 58, -48, PLAZA_Z + 0.1, 0.85, 0.7, mats["stone"], [(0, 8.0)], "city")
    wall_x("GEO-Aypate_Plaza_Parapet_N", -69, 69, 38, PLAZA_Z + 0.1, 0.85, 0.7, mats["stone"], [(0, 8.0)], "city")
    wall_y("GEO-Aypate_Plaza_Parapet_W", -66, -45, 38, PLAZA_Z + 0.1, 0.85, 0.7, mats["stone"], [(0, 10.0)], "city")
    wall_y("GEO-Aypate_Plaza_Parapet_E", 60, -45, 32, PLAZA_Z + 0.1, 0.85, 0.7, mats["stone"], [(0, 10.0)], "city")
    box("GEO-Aypate_QhapaqNan", (8, 330, 0.18), (-78, -125, PLAZA_Z + 0.42), mats["stone_dark"], "city", 8.0, 0.02)
    box("GEO-Aypate_QhapaqNan_Alt", (6, 330, 0.16), (180, -80, PLAZA_Z + 0.38), mats["stone_dark"], "city", 8.0, 0.02)
    for i in range(18):
        box(f"GEO-Aypate_Path_Stone_{i}", (8, 2.0, 0.10), (-78, -245 + i * 12, PLAZA_Z + 0.52), mats["stone"], "props", 2.0, 0.01, True)

    # Ushnu: base de 30 m por lado, tres plataformas y terraza superior documentada.
    box("GEO-Aypate_Ushnu_Base", (30, 30, 1.4), (110, 45, PLAZA_Z + 0.7), mats["stone"], "city", 6.0, 0.04)
    box("GEO-Aypate_Ushnu_Tier1", (26, 26, 1.2), (110, 45, PLAZA_Z + 2.0), mats["stone"], "city", 6.0, 0.035)
    box("GEO-Aypate_Ushnu_Tier2", (22, 22, 1.2), (110, 45, PLAZA_Z + 3.2), mats["stone"], "city", 6.0, 0.03)
    box("GEO-Aypate_Ushnu_Top", (20.7, 23.7, 1.0), (110, 45, PLAZA_Z + 4.3), mats["stone"], "city", 5.0, 0.03)
    stairs("GEO-Aypate_Ushnu_Stairs", (88.75, 45, PLAZA_Z + 0.1), 4.0, 0.25, 0.20, 25, "x", mats["stone"])
    # Escalinata lateral este y patio oeste del frontis.
    stairs("GEO-Aypate_Ushnu_Lateral", (125.0, 31.0, PLAZA_Z + 0.1), 2.2, 0.24, 0.18, 6, "y", mats["stone"])
    box("GEO-Aypate_Ushnu_Patio", (10, 8, 0.12), (80, 45, PLAZA_Z + 0.12), mats["clay"], "props", 4.0, 0.01, True)
    wall_x("GEO-Aypate_Ushnu_Patio_N", 75, 85, 49, PLAZA_Z + 0.1, 0.7, 0.5, mats["stone_dark"], layer="props")
    wall_x("GEO-Aypate_Ushnu_Patio_S", 75, 85, 41, PLAZA_Z + 0.1, 0.7, 0.5, mats["stone_dark"], layer="props")
    box("GEO-Aypate_Ushnu_Receptacle", (6.6, 2.14, 0.25), (110, 45, PLAZA_Z + 5.25), mats["stone"], "props", 2.0, 0.02)
    box("GEO-Aypate_Ushnu_Receptacle_Water", (5.6, 1.35, 0.08), (110, 45, PLAZA_Z + 5.48), mats["water"], "props", 0, 0.0, True)

    # Kallanka: 115 x 12 m, eje N-S, 13 accesos hacia la plaza.
    box("GEO-Aypate_Kallanka_Platform", (14, 117, 0.7), (-101, -20, PLAZA_Z + 0.35), mats["stone"], "city", 8.0, 0.03)
    wall_y("GEO-Aypate_Kallanka_Front", -94, -77.5, 37.5, PLAZA_Z + 0.7, 3.0, 0.9, mats["stone"], [(i * 8.5, 1.4) for i in range(-6, 7)], "city")
    wall_y("GEO-Aypate_Kallanka_Back", -108, -77.5, 37.5, PLAZA_Z + 0.7, 3.0, 0.9, mats["stone"], layer="city")
    wall_x("GEO-Aypate_Kallanka_S", -108, -94, -77.5, PLAZA_Z + 0.7, 3.0, 0.9, mats["stone"], layer="city")
    wall_x("GEO-Aypate_Kallanka_N", -108, -94, 37.5, PLAZA_Z + 0.7, 3.0, 0.9, mats["stone"], layer="city")
    for i in range(-6, 7):
        box(f"GEO-Aypate_Kallanka_Step_{i}", (2.2, 1.8, 0.22), (-91.5, i * 8.5, PLAZA_Z + 0.15), mats["stone"], "props", 2.0, 0.01, True)

    # Acllawasi: south/southwest of the plaza, gate facing north.
    box("GEO-Aypate_Acllawasi_Platform", (100, 64, 0.55), (0, -135, PLAZA_Z + 0.28), mats["stone"], "city", 7.0, 0.03)
    wall_x("GEO-Aypate_Acllawasi_N", -50, 50, -103, PLAZA_Z + 0.55, 3.1, 1.0, mats["stone"], [(0, 4.0)], "city")
    wall_x("GEO-Aypate_Acllawasi_S", -50, 50, -167, PLAZA_Z + 0.55, 3.1, 1.0, mats["stone"], layer="city")
    wall_y("GEO-Aypate_Acllawasi_W", -50, -167, -103, PLAZA_Z + 0.55, 3.1, 1.0, mats["stone"], layer="city")
    wall_y("GEO-Aypate_Acllawasi_E", 50, -167, -103, PLAZA_Z + 0.55, 3.1, 1.0, mats["stone"], layer="city")
    # Cuatro canchas: patios separados por muros internos, sin techos.
    box("GEO-Aypate_Acllawasi_Patio", (64, 38, 0.12), (0, -135, PLAZA_Z + 0.62), mats["clay"], "props", 6.0, 0.01, True)
    wall_x("GEO-Aypate_Acllawasi_Mid", -50, 50, -135, PLAZA_Z + 0.55, 2.0, 0.8, mats["stone"], [(0, 6.0)], "city")
    wall_y("GEO-Aypate_Acllawasi_Cross", 0, -167, -103, PLAZA_Z + 0.55, 2.0, 0.8, mats["stone"], [(-135, 6.0)], "city")
    for i, (x, y) in enumerate(((-28, -145), (28, -145), (-28, -119), (28, -119))):
        box(f"GEO-Aypate_Acllawasi_Room_{i}", (18, 14, 2.2), (x, y, PLAZA_Z + 1.65), mats["stone"], "city", 4.0, 0.025)
    for i, x in enumerate((-2.2, 2.2)):
        box(f"GEO-Aypate_Acllawasi_Jamb_{i}", (1.2, 1.0, 3.2), (x, -103, PLAZA_Z + 2.15), mats["stone_dark"], "props", 2.0, 0.03)
    box("GEO-Aypate_Acllawasi_Lintel", (5.8, 1.4, 0.7), (0, -103, PLAZA_Z + 4.0), mats["stone_dark"], "props", 2.0, 0.03)

    # Palace: northwest of the kallanka, secondary.
    box("GEO-Aypate_Palace_Platform", (64, 52, 0.5), (-100, 92, PLAZA_Z + 0.25), mats["stone"], "city", 7.0, 0.025)
    for i in range(3):
        box(f"GEO-Aypate_Palace_Room_{i}", (15, 9, 2.1), (-124 + i * 24, 108, PLAZA_Z + 1.6), mats["stone"], "city", 4.0, 0.02)
    box("GEO-Aypate_Palace_Patio", (50, 22, 0.2), (-100, 88, PLAZA_Z + 0.2), mats["moss"], "props", 5.0, 0.01, True)

    # Colcas: large elongated stores north of the plaza, beside the internal path.
    for i in range(3):
        box(f"GEO-Aypate_Colca_{i}", (52, 7, 2.4), (-5, 138 + i * 11, PLAZA_Z + 1.25), mats["stone"], "city", 4.0, 0.02)

    # Control kancha at the south entrance.
    wall_x("GEO-Aypate_Control_N", -90, -66, -225, PLAZA_Z + 0.1, 2.1, 0.7, mats["stone"], [(-78, 1.8)], "city")
    wall_x("GEO-Aypate_Control_S", -90, -66, -245, PLAZA_Z + 0.1, 2.1, 0.7, mats["stone"], [(-78, 1.8)], "city")
    wall_y("GEO-Aypate_Control_W", -90, -245, -225, PLAZA_Z + 0.1, 2.1, 0.7, mats["stone"], layer="city")
    wall_y("GEO-Aypate_Control_E", -66, -245, -225, PLAZA_Z + 0.1, 2.1, 0.7, mats["stone"], layer="city")

    # Sunken ritual fountain, east/northeast of the ushnu.
    box("GEO-Aypate_Fountain_Floor", (8, 6, 0.25), (145, 20, PLAZA_Z + 0.30), mats["stone_dark"], "city", 3.0, 0.02)
    for name, size, loc in (
        ("N", (8, 0.8, 1.2), (145, 23, PLAZA_Z + 0.90)),
        ("S", (8, 0.8, 1.2), (145, 17, PLAZA_Z + 0.90)),
        ("W", (0.8, 6, 1.2), (141, 20, PLAZA_Z + 0.90)),
        ("E", (0.8, 6, 1.2), (149, 20, PLAZA_Z + 0.90)),
    ):
        box(f"GEO-Aypate_Fountain_Wall_{name}", size, loc, mats["stone"], "city", 3.0, 0.02)
    box("GEO-Aypate_Fountain_Water", (6.6, 4.6, 0.08), (145, 20, PLAZA_Z + 0.52), mats["water"], "props", 0, 0.0)
    for i in range(3):
        box(f"GEO-Aypate_Fountain_Niche_{i}", (0.35, 0.9, 0.55), (141.25, 18.5 + i * 1.5, PLAZA_Z + 1.15), mats["stone_dark"], "props", 1.0, 0.005, True)

    # Agricultural terraces on the east slope.
    for i in range(5):
        z = PLAZA_Z - 1.0 - i * 1.05
        x = 232 + i * 12
        box(f"GEO-Aypate_Terrace_{i}", (8, 140, 1.15), (x, -10, z), mats["stone"], "terrain", 5.0, 0.02)
        box(f"GEO-Aypate_Terrace_Soil_{i}", (18, 140, 0.25), (x + 13, -10, z + 0.35), mats["moss"], "terrain", 6.0, 0.01, True)

    # Cloud forest and rocks; deterministic placement.
    rng = random.Random(SEED)
    for i in range(140):
        angle = rng.uniform(0, math.tau)
        radius = rng.uniform(165, 300)
        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        if abs(x) < 225 and abs(y + 20) < 175:
            continue
        if abs(x + 78) < 18 and -300 < y < 60:
            continue
        z = terrain_height(x, y)
        tree(f"GEO-Aypate_Tree_{i}", x, y, z, rng.uniform(0.75, 1.35), mats, lod1_exclude=(i % 2 == 1))
    for i in range(90):
        angle = rng.uniform(0, math.tau)
        radius = rng.uniform(115, 210)
        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        if abs(x) < 170 and abs(y + 20) < 145:
            continue
        if abs(x + 78) < 18 and -300 < y < 60:
            continue
        z = terrain_height(x, y)
        tree(f"GEO-Aypate_Forest_{i}", x, y, z, rng.uniform(0.65, 1.1), mats, lod1_exclude=(i % 3 == 0))
    for i in range(65):
        angle = rng.uniform(0, math.tau)
        radius = rng.uniform(150, 300)
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
    for i in range(34):
        x = rng.uniform(-145, 145)
        y = rng.uniform(-170, 55)
        if abs(x) < 72 and abs(y) < 52:
            continue
        if abs(x) < 62 and -175 < y < -95:
            continue
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=rng.uniform(0.3, 0.8), location=(x, y, PLAZA_Z + 0.4))
        shrub = bpy.context.object
        shrub.name = f"GEO-Aypate_Shrub_{i}"
        shrub.scale.z = rng.uniform(0.35, 0.7)
        shrub.data.materials.append(mats["leaf_dark"] if i % 2 else mats["leaf"])
        shrub["layer"] = "props"
        shrub["lod1_exclude"] = True
        add_to(shrub, bucket("Props"))

    for i, (x, y) in enumerate(((16, -8), (-22, 12), (88, 36), (-72, -12), (5, -120), (145, 12))):
        human(f"GEO-Aypate_Human_{i + 1}", x, y, PLAZA_Z + 0.15, mats)

    # Lighting.
    sun_data = bpy.data.lights.new("LGT-Aypate_Sun", "SUN")
    sun_data.energy = 3.2
    sun_data.angle = math.radians(8)
    sun_data.color = (1.0, 0.91, 0.78)
    sun = bpy.data.objects.new("LGT-Aypate_Sun", sun_data)
    scene.collection.objects.link(sun)
    sun.rotation_euler = (math.radians(38), math.radians(-22), math.radians(-42))
    fill_data = bpy.data.lights.new("LGT-Aypate_Fill", "AREA")
    fill_data.energy = 1400
    fill_data.shape = "DISK"
    fill_data.size = 200
    fill_data.color = (0.62, 0.76, 0.88)
    fill = bpy.data.objects.new("LGT-Aypate_Fill", fill_data)
    scene.collection.objects.link(fill)
    fill.location = (0, -180, 110)
    fill.rotation_euler = (Vector((0, 0, 6)) - fill.location).to_track_quat("-Z", "Y").to_euler()
    fill2_data = bpy.data.lights.new("LGT-Aypate_FillWest", "AREA")
    fill2_data.energy = 700
    fill2_data.shape = "DISK"
    fill2_data.size = 160
    fill2_data.color = (0.70, 0.80, 0.88)
    fill2 = bpy.data.objects.new("LGT-Aypate_FillWest", fill2_data)
    scene.collection.objects.link(fill2)
    fill2.location = (-180, -80, 90)
    fill2.rotation_euler = (Vector((0, 0, 6)) - fill2.location).to_track_quat("-Z", "Y").to_euler()

    # Cameras: +Y is north; viewer z = -model y * scale.
    camera_defs = {
        "Hero": ((70, -5, 18), (110, 45, 8), 50),
        "Tour1": ((-78, -200, 9), (-78, -150, 8), 42),
        "Tour2": ((20, -20, 10), (110, 45, 7), 40),
        "Tour3": ((75, 15, 12), (110, 45, 8), 45),
        "Tour4": ((-101, -70, 10), (-101, 20, 6), 35),
        "Tour5": ((0, -75, 16), (0, -135, 8), 40),
        "Tour6": ((135, 30, 10), (145, 20, 8), 45),
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


if __name__ == "__main__":
    main()
