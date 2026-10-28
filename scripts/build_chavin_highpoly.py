"""Genera el pase high-poly v0.1 de Chavín sobre la fuente Portada v0.1.

Uso:
  blender --background blender/chavin/chavin_portada_v0.1.blend \
    --python scripts/build_chavin_highpoly.py -- \
    --out-blend blender/chavin/chavin_highpoly_v0.1.blend

El pase añade detalle geométrico interpretativo en Lanzón, Portada y fachada.
No sustituye un levantamiento ni una reproducción iconográfica.
"""

import argparse
import math
import random
import sys

import bpy
from mathutils import Matrix, Vector


def parse_args():
    argv = sys.argv
    argv = argv[argv.index("--") + 1 :] if "--" in argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-blend", required=True)
    return parser.parse_args(argv)


def collection(name):
    coll = bpy.data.collections.get(name)
    if coll is None:
        raise RuntimeError(f"Falta la colección {name}")
    return coll


def activate(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def apply_modifier(obj, modifier):
    activate(obj)
    bpy.ops.object.modifier_apply(modifier=modifier.name)


def bevel(obj, width=0.01, segments=2):
    modifier = obj.modifiers.new("Bevel", "BEVEL")
    modifier.width = width
    modifier.segments = segments
    modifier.limit_method = "ANGLE"
    apply_modifier(obj, modifier)


def mark(obj, exclude=True):
    obj["chavin_highpoly"] = "v0.1"
    if exclude:
        obj["lod1_exclude"] = True


def add_box_uv(obj, scale=0.5):
    mesh = obj.data
    if mesh.uv_layers:
        return
    uv_layer = mesh.uv_layers.new(name="UVMap")
    for polygon in mesh.polygons:
        normal = polygon.normal
        axis = 0
        if abs(normal.y) > abs(normal[axis]):
            axis = 1
        if abs(normal.z) > abs(normal[axis]):
            axis = 2
        for loop_index in polygon.loop_indices:
            vertex = mesh.vertices[mesh.loops[loop_index].vertex_index]
            if axis == 0:
                uv = (vertex.co.y * scale, vertex.co.z * scale)
            elif axis == 1:
                uv = (vertex.co.x * scale, vertex.co.z * scale)
            else:
                uv = (vertex.co.x * scale, vertex.co.y * scale)
            uv_layer.data[loop_index].uv = uv


def mesh_object(name, verts, faces, material, collection_name, exclude=True):
    mesh = bpy.data.meshes.new("MESH-" + name[4:])
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    collection(collection_name).objects.link(obj)
    if material is not None:
        obj.data.materials.append(material)
    add_box_uv(obj)
    mark(obj, exclude)
    return obj


def box(name, center, size, material, collection_name, rotation=(0, 0, 0),
        bevel_width=0.012, segments=2, exclude=True):
    sx, sy, sz = (value * 0.5 for value in size)
    verts = [
        (-sx, -sy, -sz), (sx, -sy, -sz), (sx, sy, -sz), (-sx, sy, -sz),
        (-sx, -sy, sz), (sx, -sy, sz), (sx, sy, sz), (-sx, sy, sz),
    ]
    faces = [
        (0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
        (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7),
    ]
    rot = Matrix.Rotation(rotation[0], 4, "X")
    rot @= Matrix.Rotation(rotation[1], 4, "Y")
    rot @= Matrix.Rotation(rotation[2], 4, "Z")
    mat = Matrix.Translation(Vector(center)) @ rot
    verts = [tuple(mat @ Vector(v)) for v in verts]
    obj = mesh_object(name, verts, faces, material, collection_name, exclude)
    if bevel_width > 0:
        bevel(obj, bevel_width, segments)
    return obj


def ellipsoid(name, center, radii, material, collection_name,
              segments=24, rings=12, rotation=(0, 0, 0), exclude=True):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=segments, ring_count=rings, radius=1.0, location=center
    )
    obj = bpy.context.object
    obj.name = name
    obj.data.name = "MESH-" + name[4:]
    obj.dimensions = tuple(value * 2.0 for value in radii)
    obj.rotation_euler = rotation
    activate(obj)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    for coll in list(obj.users_collection):
        coll.objects.unlink(obj)
    collection(collection_name).objects.link(obj)
    obj.data.materials.append(material)
    mark(obj, exclude)
    return obj


def cone_between(name, start, end, radius_start, radius_end, material,
                 collection_name, vertices=16, exclude=True):
    start = Vector(start)
    end = Vector(end)
    direction = end - start
    length = direction.length
    midpoint = (start + end) * 0.5
    bpy.ops.mesh.primitive_cone_add(
        vertices=vertices,
        radius1=radius_start,
        radius2=radius_end,
        depth=length,
        location=midpoint,
    )
    obj = bpy.context.object
    obj.name = name
    obj.data.name = "MESH-" + name[4:]
    obj.rotation_mode = "QUATERNION"
    obj.rotation_quaternion = Vector((0.0, 0.0, 1.0)).rotation_difference(
        direction.normalized()
    )
    activate(obj)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    for coll in list(obj.users_collection):
        coll.objects.unlink(obj)
    collection(collection_name).objects.link(obj)
    obj.data.materials.append(material)
    mark(obj, exclude)
    return obj


def tube(name, points, radius, material, collection_name, sides=8, exclude=True):
    points = [Vector(point) for point in points]
    verts = []
    faces = []
    rings = []
    for index, point in enumerate(points):
        if index == 0:
            tangent = (points[1] - point).normalized()
        elif index == len(points) - 1:
            tangent = (point - points[index - 1]).normalized()
        else:
            tangent = (points[index + 1] - points[index - 1]).normalized()
        normal = tangent.cross(Vector((0.0, 0.0, 1.0)))
        if normal.length < 1e-5:
            normal = tangent.cross(Vector((0.0, 1.0, 0.0)))
        normal.normalize()
        binormal = tangent.cross(normal).normalized()
        ring = []
        for side in range(sides):
            angle = math.tau * side / sides
            offset = normal * (math.cos(angle) * radius) + binormal * (
                math.sin(angle) * radius
            )
            ring.append(len(verts))
            verts.append(tuple(point + offset))
        rings.append(ring)
    for index in range(len(rings) - 1):
        for side in range(sides):
            next_side = (side + 1) % sides
            faces.append(
                (rings[index][side], rings[index][next_side],
                 rings[index + 1][next_side], rings[index + 1][side])
            )
    faces.append(tuple(reversed(rings[0])))
    faces.append(tuple(rings[-1]))
    return mesh_object(name, verts, faces, material, collection_name, exclude)


def outline_plate(name, outline, x_center, thickness, material, collection_name,
                  bevel_width=0.006, segments=2, exclude=True):
    half = thickness * 0.5
    count = len(outline)
    verts = [(x_center + half, y, z) for y, z in outline]
    verts += [(x_center - half, y, z) for y, z in outline]
    faces = [tuple(range(count)), tuple(range(count, count * 2))[::-1]]
    for index in range(count):
        nxt = (index + 1) % count
        faces.append((index, nxt, count + nxt, count + index))
    obj = mesh_object(name, verts, faces, material, collection_name, exclude)
    bevel(obj, bevel_width, segments)
    return obj


def target_rotation(camera, target):
    direction = Vector(target) - camera.location
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def add_camera(name, location, target, lens=70):
    bpy.ops.object.camera_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.data.name = "DATA-" + name[4:]
    obj.data.lens = lens
    target_rotation(obj, target)
    for coll in list(obj.users_collection):
        coll.objects.unlink(obj)
    collection("COL-Chavin_Cameras").objects.link(obj)
    return obj


def remove_existing_falcons():
    for obj in list(bpy.data.objects):
        if obj.name.startswith("GEO-Chavin_Portada_Falcon"):
            bpy.data.objects.remove(obj, do_unlink=True)


FALCON_OUTLINE = [
    (-0.205, -0.025), (-0.185, 0.045), (-0.145, 0.085),
    (-0.090, 0.110), (-0.020, 0.135), (0.045, 0.142),
    (0.100, 0.130), (0.135, 0.105), (0.160, 0.075),
    (0.195, 0.055), (0.235, 0.025), (0.255, 0.000),
    (0.205, -0.010), (0.175, -0.035), (0.170, -0.075),
    (0.125, -0.095), (0.070, -0.105), (0.030, -0.130),
    (-0.010, -0.150), (-0.045, -0.130), (-0.085, -0.155),
    (-0.105, -0.110), (-0.145, -0.115), (-0.170, -0.080),
]


def add_falcon(index, y_center, light, dark):
    x = 36.025
    z = 6.380
    prefix = f"GEO-Chavin_Portada_Falcon_{index:02d}"
    outline = [(y_center + y, z + zz) for y, zz in FALCON_OUTLINE]
    outline_plate(prefix, outline, x, 0.024, light, "COL-Chavin_Portada", 0.005, 2, False)

    wing_outline = [
        (y_center + 0.070, z + 0.095),
        (y_center + 0.010, z + 0.080),
        (y_center - 0.060, z + 0.055),
        (y_center - 0.130, z + 0.030),
        (y_center - 0.195, z + 0.005),
        (y_center - 0.178, z - 0.038),
        (y_center - 0.150, z - 0.018),
        (y_center - 0.142, z - 0.060),
        (y_center - 0.112, z - 0.030),
        (y_center - 0.104, z - 0.075),
        (y_center - 0.074, z - 0.040),
        (y_center - 0.066, z - 0.085),
        (y_center - 0.036, z - 0.045),
        (y_center - 0.028, z - 0.082),
        (y_center + 0.005, z - 0.045),
        (y_center + 0.025, z - 0.072),
        (y_center + 0.052, z - 0.030),
        (y_center + 0.076, z - 0.005),
    ]
    outline_plate(
        f"{prefix}_Wing", wing_outline, x + 0.014, 0.012, light,
        "COL-Chavin_Portada", 0.003, 1,
    )
    for covert in range(3):
        angle = math.radians(-28 + covert * 9)
        yy = y_center + 0.030 - covert * 0.045
        zz = z + 0.070 - covert * 0.012
        box(
            f"{prefix}_Covert_{covert + 1}",
            (x + 0.021, yy, zz),
            (0.008, 0.026, 0.080),
            light,
            "COL-Chavin_Portada",
            rotation=(angle, 0.0, 0.0),
            bevel_width=0.002,
            segments=1,
        )

    ellipsoid(
        f"{prefix}_Head", (x + 0.012, y_center + 0.130, z + 0.072),
        (0.018, 0.050, 0.046), light, "COL-Chavin_Portada", 24, 12,
    )
    ellipsoid(
        f"{prefix}_Eye", (x + 0.032, y_center + 0.155, z + 0.087),
        (0.009, 0.012, 0.012), dark, "COL-Chavin_Portada", 20, 10,
    )
    cone_between(
        f"{prefix}_Beak",
        (x + 0.024, y_center + 0.170, z + 0.055),
        (x + 0.024, y_center + 0.252, z + 0.028),
        0.022, 0.001, light, "COL-Chavin_Portada", 16,
    )
    cone_between(
        f"{prefix}_Beak_Lower",
        (x + 0.024, y_center + 0.170, z + 0.038),
        (x + 0.024, y_center + 0.220, z + 0.012),
        0.014, 0.001, light, "COL-Chavin_Portada", 12,
    )

    for crest in range(3):
        cone_between(
            f"{prefix}_Crest_{crest + 1}",
            (x + 0.012, y_center + 0.078 + crest * 0.020, z + 0.108),
            (x + 0.012, y_center + 0.052 + crest * 0.020, z + 0.165),
            0.008, 0.001, light, "COL-Chavin_Portada", 10,
        )

    for foot in range(2):
        base_y = y_center + (0.020 if foot == 0 else 0.080)
        for claw in range(3):
            cone_between(
                f"{prefix}_Talon_{foot + 1}_{claw + 1}",
                (x + 0.018, base_y + (claw - 1) * 0.014, z - 0.134),
                (x + 0.018, base_y + (claw - 1) * 0.026 - 0.012, z - 0.185),
                0.007, 0.001, light, "COL-Chavin_Portada", 8,
            )

    for tail in range(3):
        box(
            f"{prefix}_Tail_{tail + 1}",
            (x + 0.012, y_center - 0.200, z - 0.038 + (tail - 1) * 0.022),
            (0.010, 0.060, 0.014),
            light,
            "COL-Chavin_Portada",
            rotation=(0.0, math.radians(-12 + tail * 12), 0.0),
            bevel_width=0.002,
            segments=1,
        )


def add_column_details(sign, suffix, stone, dark):
    y = sign * 1.600
    x = 35.870
    z = 5.300
    prefix = f"GEO-Chavin_Portada_Column_{suffix}"
    ellipsoid(
        f"{prefix}_HP_Eye_1", (x + 0.014, y - 0.062, z + 0.100),
        (0.014, 0.030, 0.024), dark, "COL-Chavin_Portada", 20, 10,
    )
    ellipsoid(
        f"{prefix}_HP_Eye_2", (x + 0.014, y + 0.062, z + 0.100),
        (0.014, 0.030, 0.024), dark, "COL-Chavin_Portada", 20, 10,
    )
    box(
        f"{prefix}_HP_Nose", (x + 0.022, y, z + 0.020),
        (0.050, 0.052, 0.115), stone, "COL-Chavin_Portada",
        bevel_width=0.010, segments=2,
    )
    box(
        f"{prefix}_HP_Brow_1", (x + 0.014, y - 0.065, z + 0.145),
        (0.020, 0.105, 0.024), stone, "COL-Chavin_Portada",
        rotation=(0.0, 0.0, math.radians(-12)), bevel_width=0.006,
    )
    box(
        f"{prefix}_HP_Brow_2", (x + 0.014, y + 0.065, z + 0.145),
        (0.020, 0.105, 0.024), stone, "COL-Chavin_Portada",
        rotation=(0.0, 0.0, math.radians(12)), bevel_width=0.006,
    )
    box(
        f"{prefix}_HP_Mouth", (x + 0.020, y, z - 0.095),
        (0.040, 0.180, 0.040), dark, "COL-Chavin_Portada",
        bevel_width=0.008, segments=2,
    )
    for side in (-1, 1):
        cone_between(
            f"{prefix}_HP_Fang_{side}", (x + 0.037, y + side * 0.055, z - 0.078),
            (x + 0.037, y + side * 0.048, z - 0.125),
            0.012, 0.001, stone, "COL-Chavin_Portada", 10,
        )
        ellipsoid(
            f"{prefix}_HP_Ear_{side}", (x + 0.006, y + side * 0.135, z + 0.055),
            (0.020, 0.038, 0.055), stone, "COL-Chavin_Portada", 16, 8,
        )

    for side in (-1, 1):
        points = []
        for step in range(13):
            t = step / 12.0
            points.append((
                x + 0.012 + 0.010 * math.sin(t * math.tau),
                y + side * (0.165 + 0.055 * math.sin(t * math.tau * 1.5)),
                3.95 + t * 2.05,
            ))
        tube(
            f"{prefix}_HP_Serpent_{side}", points, 0.028, dark,
            "COL-Chavin_Portada", 8,
        )

    for band in (3.95, 4.15, 6.02):
        bpy.ops.mesh.primitive_torus_add(
            major_segments=48, minor_segments=6,
            major_radius=0.315, minor_radius=0.012,
            location=(35.550, y, band),
        )
        obj = bpy.context.object
        obj.name = f"{prefix}_HP_Band_{band:.2f}"
        obj.data.name = "MESH-" + obj.name[4:]
        activate(obj)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        for coll in list(obj.users_collection):
            coll.objects.unlink(obj)
        collection("COL-Chavin_Portada").objects.link(obj)
        obj.data.materials.append(stone)
        mark(obj, True)


def add_portada_details(light, dark):
    remove_existing_falcons()
    for obj in list(bpy.data.objects):
        if obj.name.startswith("GEO-Chavin_Portada_Column_") and "_Serpent_" in obj.name:
            bpy.data.objects.remove(obj, do_unlink=True)
    positions = (-2.330, -1.810, -0.930, -0.430, 0.430, 0.930, 1.810, 2.330)
    for index, y in enumerate(positions, start=1):
        add_falcon(index, y, light, dark)
    add_column_details(-1, "S", light, dark)
    add_column_details(1, "N", dark, light)

    for index, y in enumerate((0.0,), start=1):
        box(
            f"GEO-Chavin_Portada_HP_Frieze_Molding_Low_{index}",
            (36.060, y, 6.105), (0.080, 6.400, 0.075), light,
            "COL-Chavin_Portada", bevel_width=0.012, segments=2,
        )
        box(
            f"GEO-Chavin_Portada_HP_Frieze_Molding_High_{index}",
            (36.055, y, 6.675), (0.070, 6.750, 0.060), light,
            "COL-Chavin_Portada", bevel_width=0.010, segments=2,
        )
    for sign, suffix in ((-1, "S"), (1, "N")):
        for row in range(3):
            y = sign * 2.350
            z = 4.180 + row * 0.755
            box(
                f"GEO-Chavin_Portada_HP_Jamb_{suffix}_Joint_{row + 1}",
                (35.560, y, z + 0.390), (0.020, 0.890, 0.025), dark,
                "COL-Chavin_Portada", bevel_width=0.002, segments=1,
            )


def lanzon_front_x(z):
    return 0.485 - (z - 3.0) * (0.485 - 0.180) / 4.5


def add_lanzon_details(stone, dark):
    y0 = 62.0
    x_face = lanzon_front_x(6.55) + 0.020
    for sign in (-1, 1):
        ellipsoid(
            f"GEO-Chavin_Lanzon_HP_Eye_{sign}",
            (x_face, y0 + sign * 0.145, 6.565), (0.022, 0.080, 0.050),
            stone, "COL-Chavin_Details", 24, 12,
        )
        ellipsoid(
            f"GEO-Chavin_Lanzon_HP_Pupil_{sign}",
            (x_face + 0.026, y0 + sign * 0.145, 6.565), (0.016, 0.030, 0.030),
            dark, "COL-Chavin_Details", 16, 8,
        )
        ellipsoid(
            f"GEO-Chavin_Lanzon_HP_Brow_{sign}",
            (x_face - 0.008, y0 + sign * 0.150, 6.660),
            (0.026, 0.115, 0.030), stone, "COL-Chavin_Details", 24, 10,
            rotation=(math.radians(sign * 10), 0.0, 0.0),
        )
        ellipsoid(
            f"GEO-Chavin_Lanzon_HP_Ear_{sign}",
            (lanzon_front_x(6.50) + 0.010, y0 + sign * 0.245, 6.500),
            (0.025, 0.070, 0.085), stone, "COL-Chavin_Details", 20, 10,
        )

    box(
        "GEO-Chavin_Lanzon_HP_Nose",
        (lanzon_front_x(6.32) + 0.055, y0, 6.340),
        (0.150, 0.110, 0.330), stone, "COL-Chavin_Details",
        rotation=(0.0, math.radians(-4), 0.0), bevel_width=0.030, segments=2,
    )
    box(
        "GEO-Chavin_Lanzon_HP_Mouth",
        (lanzon_front_x(6.08) + 0.040, y0, 6.080),
        (0.075, 0.500, 0.190), dark, "COL-Chavin_Details",
        rotation=(0.0, math.radians(-4), 0.0), bevel_width=0.020, segments=2,
    )
    for lip_z, lip_h in ((6.180, 0.040), (5.985, 0.030)):
        box(
            f"GEO-Chavin_Lanzon_HP_Lip_{lip_z:.2f}",
            (lanzon_front_x(lip_z) + 0.060, y0, lip_z),
            (0.090, 0.500, lip_h), stone, "COL-Chavin_Details",
            rotation=(0.0, math.radians(-4), 0.0), bevel_width=0.012, segments=2,
        )
    for sign in (-1, 1):
        for side in (-1, 1):
            cone_between(
                f"GEO-Chavin_Lanzon_HP_Fang_{sign}_{side}",
                (lanzon_front_x(6.14) + 0.080, y0 + side * 0.120 + sign * 0.030, 6.145),
                (lanzon_front_x(6.05) + 0.090, y0 + side * 0.105 + sign * 0.030, 6.040),
                0.022, 0.002, stone, "COL-Chavin_Details", 12,
            )

    for side in (-1, 1):
        points = []
        for step in range(11):
            t = step / 10.0
            z = 6.85 - t * 2.55
            points.append((
                lanzon_front_x(z) + 0.020,
                y0 + side * (0.180 + 0.070 * math.sin(t * math.pi * 2.0)),
                z,
            ))
        tube(
            f"GEO-Chavin_Lanzon_HP_Hair_{side}", points, 0.030, stone,
            "COL-Chavin_Details", 8,
        )

    for index, z in enumerate((4.70, 5.05, 5.40, 5.75), start=1):
        points = []
        for step in range(13):
            t = step / 12.0
            y = y0 - 0.340 + t * 0.680
            points.append((
                lanzon_front_x(z + 0.020 * math.sin(t * math.pi * 2.0)) + 0.018,
                y,
                z + 0.022 * math.sin(t * math.pi * 2.0 + index),
            ))
        tube(
            f"GEO-Chavin_Lanzon_HP_Band_{index}", points, 0.024,
            dark if index % 2 else stone, "COL-Chavin_Details", 8,
        )

    for sign in (-1, 1):
        box(
            f"GEO-Chavin_Lanzon_HP_Arm_{sign}",
            (lanzon_front_x(5.45) + 0.015, y0 + sign * 0.330, 5.480),
            (0.060, 0.100, 0.950), stone, "COL-Chavin_Details",
            rotation=(math.radians(sign * 8), math.radians(-5), 0.0),
            bevel_width=0.020, segments=2,
        )
        for claw in range(3):
            cone_between(
                f"GEO-Chavin_Lanzon_HP_Claw_{sign}_{claw}",
                (lanzon_front_x(5.05) + 0.045, y0 + sign * (0.300 + claw * 0.028), 5.060),
                (lanzon_front_x(4.99) + 0.050, y0 + sign * (0.285 + claw * 0.032), 4.950),
                0.012, 0.001, stone, "COL-Chavin_Details", 8,
            )


ASHLAR_TONES = (
    (0.255, 0.220, 0.145, 1.0),
    (0.290, 0.250, 0.165, 1.0),
    (0.325, 0.280, 0.185, 1.0),
)


def make_ashlar_materials():
    materials = []
    for index, color in enumerate(ASHLAR_TONES):
        name = f"MAT-Chavin_Ashlar_HP_{'ABC'[index]}"
        material = bpy.data.materials.get(name)
        if material is None:
            material = bpy.data.materials.new(name)
            material.use_nodes = True
            material.diffuse_color = color
            bsdf = next(
                node
                for node in material.node_tree.nodes
                if node.type == "BSDF_PRINCIPLED"
            )
            bsdf.inputs["Base Color"].default_value = color
            bsdf.inputs["Roughness"].default_value = 0.88
            bsdf.inputs["Metallic"].default_value = 0.0
            material["chavin:source"] = "scripts/build_chavin_highpoly.py"
        materials.append(material)
    return materials


def ashlar_material(materials, row, u):
    return materials[(row * 7 + int((u + 200.0) * 10.0)) % len(materials)]


def add_facade_blocks(materials):
    for tier, (x_front, z_bottom, z_top, y_half) in enumerate((
        (35.015, 3.05, 8.85, 10.0),
        (29.015, 9.05, 14.85, 9.0),
        (23.015, 15.05, 20.85, 8.0),
        (17.015, 21.05, 25.45, 6.0),
    ), start=1):
        row = 0
        z = z_bottom
        while z < z_top - 0.20:
            height = 0.62
            offset = 0.0 if row % 2 == 0 else 0.64
            y = -y_half + offset
            while y < y_half - 0.20:
                width = 1.28
                cy = y + width * 0.5
                cz = z + height * 0.5
                skip = tier == 1 and -3.55 < cy < 3.55 and 3.20 < cz < 7.10
                if not skip and y + width < y_half:
                    box(
                        f"GEO-Chavin_Facade_HP_T{tier}_{row:02d}_{int((cy + 100) * 10):04d}",
                        (x_front - 0.11, cy, cz), (0.30, width - 0.004, height - 0.004),
                        ashlar_material(materials, row, cy),
                        "COL-Chavin_Architecture", bevel_width=0.004,
                        segments=1,
                    )
                y += width
            z += height
            row += 1


def add_rock(name, center, scale, material):
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=2, radius=1.0, location=center,
    )
    obj = bpy.context.object
    obj.name = name
    obj.data.name = "MESH-" + name[4:]
    obj.dimensions = scale
    obj.rotation_euler = (
        random.uniform(0.0, math.tau),
        random.uniform(0.0, math.tau),
        random.uniform(0.0, math.tau),
    )
    activate(obj)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    for coll in list(obj.users_collection):
        coll.objects.unlink(obj)
    collection("COL-Chavin_Terrain").objects.link(obj)
    obj.data.materials.append(material)
    mark(obj, True)
    return obj


def add_wall_band(prefix, axis, fixed, u_min, u_max, z_bottom, z_top, materials):
    height = 0.62
    width = 1.28
    row = 0
    z = z_bottom
    while z < z_top - 0.20:
        offset = 0.0 if row % 2 == 0 else width * 0.5
        u = u_min + offset
        while u < u_max - 0.20:
            cu = u + width * 0.5
            cz = z + height * 0.5
            if u + width < u_max:
                if axis == "x":
                    center = (fixed - 0.11, cu, cz)
                    size = (0.30, width - 0.004, height - 0.004)
                else:
                    center = (cu, fixed - 0.11, cz)
                    size = (width - 0.004, 0.30, height - 0.004)
                box(
                    f"{prefix}_{row:02d}_{int((cu + 200) * 10):04d}",
                    center, size, ashlar_material(materials, row, cu),
                    "COL-Chavin_Architecture", bevel_width=0.004, segments=1,
                )
            u += width
        z += height
        row += 1


def add_secondary_facade_blocks(materials):
    for tier, (y_front, z_bottom, z_top, x_half) in enumerate((
        (-40.015, 3.05, 8.85, 35.0),
        (-33.015, 9.05, 14.85, 29.0),
        (-26.015, 15.05, 20.85, 23.0),
        (-19.015, 21.05, 25.45, 17.0),
    ), start=1):
        add_wall_band(
            f"GEO-Chavin_Facade_HP_A_S_T{tier}", "y", y_front,
            -x_half, x_half, z_bottom, z_top, materials,
        )
    add_wall_band(
        "GEO-Chavin_Facade_HP_B_E", "x", 14.015,
        52.0, 82.0, 9.05, 14.85, materials,
    )
    add_wall_band(
        "GEO-Chavin_Facade_HP_B_S", "y", 52.015,
        -24.0, 14.0, 9.05, 14.85, materials,
    )


def add_terrain_details(stone, earth):
    rng = random.Random(731)
    for index in range(120):
        y = rng.uniform(-210.0, 240.0)
        x = 91.0 + rng.uniform(-4.0, 4.0)
        z = -1.0 + rng.uniform(-0.2, 0.2)
        scale = (rng.uniform(0.5, 2.4), rng.uniform(0.4, 1.8), rng.uniform(0.3, 0.9))
        add_rock(f"GEO-Chavin_Rock_Mosna_{index:03d}", (x, y, z), scale, stone)
    for index in range(90):
        x = rng.uniform(-190.0, 92.0)
        y = -130.0 + rng.uniform(-4.0, 4.0)
        z = -1.0 + rng.uniform(-0.2, 0.2)
        scale = (rng.uniform(0.4, 1.9), rng.uniform(0.4, 2.2), rng.uniform(0.3, 0.8))
        add_rock(f"GEO-Chavin_Rock_Wacheqsa_{index:03d}", (x, y, z), scale, stone)
    for index in range(36):
        angle = rng.uniform(0.0, math.tau)
        radius = rng.uniform(145.0, 210.0)
        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        z = rng.uniform(-0.5, 2.0)
        scale = (rng.uniform(0.6, 2.8), rng.uniform(0.5, 2.2), rng.uniform(0.4, 1.2))
        add_rock(f"GEO-Chavin_Rock_Plateau_{index:03d}", (x, y, z), scale, earth)

    texture = bpy.data.textures.new("TEX-Chavin_HP_Hill", "CLOUDS")
    texture.noise_scale = 14.0
    texture.noise_depth = 2
    for name, levels, strength in (
        ("GEO-Chavin_Hill_NW", 2, 1.8),
        ("GEO-Chavin_Hill_NE", 2, 1.8),
        ("GEO-Chavin_Hill_SW", 2, 1.8),
        ("GEO-Chavin_Hill_SE", 2, 1.8),
        ("GEO-Chavin_Hill_Cochas", 2, 3.2),
    ):
        obj = bpy.data.objects[name]
        subdiv = obj.modifiers.new("HP_Subdivision", "SUBSURF")
        subdiv.subdivision_type = "SIMPLE"
        subdiv.levels = levels
        subdiv.render_levels = levels
        apply_modifier(obj, subdiv)
        displace = obj.modifiers.new("HP_Displace", "DISPLACE")
        displace.texture = texture
        displace.strength = strength
        displace.mid_level = 0.5
        apply_modifier(obj, displace)
        obj["chavin_highpoly"] = "v0.1"
        print("HILL_DETAIL", name, len(obj.data.polygons))


def add_qa_cameras():
    bpy.ops.object.light_add(type="POINT", location=(1.9, 62.0, 6.1))
    light = bpy.context.object
    light.name = "LGT-Chavin_HP_LanzonFill"
    light.data.name = "DATA-LGT-Chavin_HP_LanzonFill"
    light.data.energy = 70.0
    light.data.color = (1.0, 0.82, 0.62)
    light.data.shadow_soft_size = 0.35
    for coll in list(light.users_collection):
        coll.objects.unlink(light)
    collection("COL-Chavin_Lights").objects.link(light)
    add_camera(
        "CAM-Chavin_HP_Portada",
        (39.5, -1.8, 6.3), (35.9, -1.0, 5.9), 55,
    )
    add_camera(
        "CAM-Chavin_HP_Falcon",
        (37.1, -2.4, 6.45), (36.03, -2.4, 6.38), 85,
    )
    add_camera(
        "CAM-Chavin_HP_Lanzon",
        (7.3, 62.0, 4.45), (0.15, 62.0, 5.30), 35,
    )
    add_camera(
        "CAM-Chavin_HP_LanzonFace",
        (1.75, 62.0, 4.75), (0.10, 62.0, 6.35), 28,
    )
    add_camera(
        "CAM-Chavin_HP_Facade",
        (40.0, -8.0, 8.0), (35.0, -1.0, 5.8), 45,
    )


def main():
    args = parse_args()
    bpy.ops.object.mode_set(mode="OBJECT") if bpy.context.object and bpy.context.object.mode != "OBJECT" else None
    for obj in bpy.data.objects:
        obj.hide_set(False)
        obj.hide_render = False
    light = bpy.data.materials["MAT-Chavin_Portada_Light"]
    dark = bpy.data.materials["MAT-Chavin_Portada_Dark"]
    lanzon = bpy.data.materials["MAT-Chavin_Lanzon"]
    gallery_dark = bpy.data.materials["MAT-Chavin_GalleryDark"]
    stone = bpy.data.materials["MAT-Chavin_Stone_Tiled"]
    ashlar = make_ashlar_materials()
    earth = bpy.data.materials["MAT-Chavin_Earth"]
    add_portada_details(light, dark)
    add_lanzon_details(lanzon, gallery_dark)
    add_facade_blocks(ashlar)
    add_secondary_facade_blocks(ashlar)
    add_terrain_details(stone, earth)
    add_qa_cameras()
    bpy.context.scene.camera = bpy.data.objects.get("CAM-Chavin_HP_Portada")
    bpy.ops.wm.save_as_mainfile(filepath=args.out_blend)
    meshes = [obj for obj in bpy.data.objects if obj.type == "MESH"]
    for obj in meshes:
        obj.data.calc_loop_triangles()
    print(
        "CHAVIN_HIGHPOLY_SAVED",
        args.out_blend,
        "meshes", len(meshes),
        "tris", sum(len(obj.data.loop_triangles) for obj in meshes),
    )


if __name__ == "__main__":
    main()
