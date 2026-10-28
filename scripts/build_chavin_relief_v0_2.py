"""Rehace el relieve del Lanzón y del friso de la Portada como superficies talladas.

Uso:
  blender --background blender/chavin/chavin_highpoly_v0.1.blend \
    --python scripts/build_chavin_relief_v0_2.py -- \
    --out-blend blender/chavin/chavin_highpoly_v0.2.blend

Parte de la escena high-poly v0.1: elimina las primitivas pegadas del Lanzón,
las falcónidas planas y los detalles de columna, y construye mallas de altura
integradas en las superficies. No añade texturas nuevas.
"""

import argparse
import math
import sys

import bmesh
import bpy

FRIEZE_X = 36.025
FRIEZE_Z0 = 6.14
FRIEZE_Z1 = 6.66
LANZON_Z0 = 5.55
LANZON_Z1 = 7.10
LANZON_Y = 0.42
LANZON_Y0 = 62.0
FALCON_POSITIONS = (-2.330, -1.810, -0.930, -0.430, 0.430, 0.930, 1.810, 2.330)


def parse_args():
    argv = sys.argv
    argv = argv[argv.index("--") + 1 :] if "--" in argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-blend", required=True)
    parser.add_argument("--step", type=float, default=0.012)
    return parser.parse_args(argv)


def clamp01(value):
    return max(0.0, min(1.0, value))


def smoothstep(edge0, edge1, value):
    if edge1 == edge0:
        return 0.0
    t = clamp01((value - edge0) / (edge1 - edge0))
    return t * t * (3.0 - 2.0 * t)


def segment_distance(px, py, ax, ay, bx, by):
    dx = bx - ax
    dy = by - ay
    length_sq = dx * dx + dy * dy
    if length_sq <= 1e-12:
        return math.hypot(px - ax, py - ay)
    t = clamp01(((px - ax) * dx + (py - ay) * dy) / length_sq)
    return math.hypot(px - (ax + dx * t), py - (ay + dy * t))


def polyline_mask(px, py, points, width):
    distance = min(
        segment_distance(px, py, ax, ay, bx, by)
        for (ax, ay), (bx, by) in zip(points, points[1:])
    )
    return 1.0 - smoothstep(0.0, width, distance)


def ellipse_mask(px, py, cx, cy, rx, ry, edge=0.22):
    sdf = math.hypot((px - cx) / rx, (py - cy) / ry)
    return 1.0 - smoothstep(1.0 - edge, 1.0, sdf)


def ellipse_distance(px, py, cx, cy, rx, ry):
    return math.hypot((px - cx) / rx, (py - cy) / ry)


def point_in_polygon(px, py, points):
    inside = False
    count = len(points)
    for index in range(count):
        ax, ay = points[index]
        bx, by = points[(index + 1) % count]
        if (ay > py) != (by > py):
            cross_x = ax + (py - ay) * (bx - ax) / (by - ay)
            if px < cross_x:
                inside = not inside
    return inside


def polygon_distance(px, py, points):
    distance = min(
        segment_distance(px, py, ax, ay, bx, by)
        for (ax, ay), (bx, by) in zip(points, points[1:] + points[:1])
    )
    return distance if point_in_polygon(px, py, points) else -distance


def plateau(distance, edge=0.004):
    return smoothstep(0.0, edge, distance)


def rotated(px, py, angle):
    cosine = math.cos(angle)
    sine = math.sin(angle)
    return px * cosine - py * sine, px * sine + py * cosine


def lanzon_front_x(z):
    return 0.485 - (z - 3.0) * (0.485 - 0.180) / 4.5


def ellipse_ring_mask(y, z, cy, cz, ry, rz, width):
    sdf = ellipse_distance(y, z, cy, cz, ry, rz)
    return 1.0 - smoothstep(0.0, width, abs(sdf - 1.0))


def lanzon_mouth_mask(y, z):
    t = min(abs(y), 0.300) / 0.300
    center = 6.035 + 0.060 * t * t
    half = 0.052 * (1.0 - 0.30 * t * t)
    band = smoothstep(center - half - 0.006, center - half + 0.006, z)
    band *= 1.0 - smoothstep(center + half - 0.006, center + half + 0.006, z)
    return band * (1.0 - smoothstep(0.285, 0.305, abs(y)))


def lanzon_height(y, z):
    height = 0.0

    face = (abs(y) / 0.385) ** 4 + (abs(z - 6.50) / 0.650) ** 4
    height -= 0.012 * (1.0 - smoothstep(0.0, 0.10, abs(face - 1.0)))

    for sign in (-1, 1):
        eye_y = sign * 0.160
        eye_z = 6.550
        height -= 0.016 * ellipse_ring_mask(y, z, eye_y, eye_z, 0.100, 0.078, 0.12)
        height -= 0.014 * ellipse_ring_mask(y, z, eye_y, eye_z, 0.058, 0.047, 0.12)

        brow = (
            (sign * 0.330, 6.655),
            (sign * 0.270, 6.710),
            (sign * 0.205, 6.745),
            (sign * 0.135, 6.720),
            (sign * 0.065, 6.740),
        )
        height -= 0.016 * polyline_mask(y, z, brow, 0.014)
        height -= 0.010 * ellipse_ring_mask(y, z, sign * 0.338, 6.650, 0.030, 0.024, 0.30)
        for fork in (-1, 1):
            height -= 0.010 * polyline_mask(
                y, z,
                ((sign * 0.338, 6.650), (sign * 0.370, 6.665 + fork * 0.022)),
                0.008,
            )

        pendant_y = sign * 0.338
        height -= 0.010 * ellipse_ring_mask(y, z, pendant_y, 6.445, 0.047, 0.050, 0.18)
        height -= 0.010 * ellipse_mask(y, z, pendant_y, 6.445, 0.018, 0.018, 0.40)

        hair = (
            (sign * 0.300, 6.960),
            (sign * 0.350, 6.860),
            (sign * 0.312, 6.760),
            (sign * 0.352, 6.660),
        )
        height -= 0.012 * polyline_mask(y, z, hair, 0.010)
        hair2 = (
            (sign * 0.260, 6.930),
            (sign * 0.300, 6.840),
            (sign * 0.265, 6.740),
        )
        height -= 0.010 * polyline_mask(y, z, hair2, 0.009)

    nose_top = 6.530
    nose_bottom = 6.120
    if nose_bottom - 0.02 < z < nose_top + 0.02:
        t = clamp01((z - nose_bottom) / (nose_top - nose_bottom))
        half_width = 0.095 - 0.045 * t
        side = 1.0 - smoothstep(0.0, 0.010, abs(y) - half_width)
        vertical = smoothstep(0.0, 0.012, z - nose_bottom) * (
            1.0 - smoothstep(0.0, 0.012, nose_top - z)
        )
        nose = side * vertical
        height += 0.036 * nose
        height += 0.008 * nose * (1.0 - smoothstep(0.0, 0.008, abs(y)))
        height -= 0.012 * ellipse_ring_mask(y, z, 0.082, 6.155, 0.032, 0.030, 0.30)
        height -= 0.012 * ellipse_ring_mask(y, z, -0.082, 6.155, 0.032, 0.030, 0.30)
        height -= 0.012 * ellipse_mask(y, z, 0.050, 6.135, 0.016, 0.014, 0.40)
        height -= 0.012 * ellipse_mask(y, z, -0.050, 6.135, 0.016, 0.014, 0.40)
    height -= 0.012 * polyline_mask(y, z, ((0.0, 6.530), (0.0, 6.640)), 0.009)

    mouth = lanzon_mouth_mask(y, z)
    height -= 0.030 * mouth

    t = min(abs(y), 0.300) / 0.300
    center = 6.035 + 0.060 * t * t
    half = 0.052 * (1.0 - 0.30 * t * t)
    for edge_z, offset, width in (
        (center + half, 0.012, 0.012),
        (center - half, -0.010, 0.010),
    ):
        lip = 1.0 - smoothstep(0.0, width, abs(z - edge_z - offset))
        lip *= 1.0 - smoothstep(0.270, 0.300, abs(y))
        height -= 0.014 * lip

    for fang_y in (-0.105, 0.105):
        base_z = 6.120
        tip_z = 6.025
        if tip_z <= z <= base_z:
            t = (z - tip_z) / (base_z - tip_z)
            half_width = 0.008 + 0.018 * t
            height += 0.036 * (
                1.0 - smoothstep(0.0, 0.0025, abs(y - fang_y) - half_width)
            )
    for incisor_y in (-0.045, 0.045):
        base_z = 6.105
        tip_z = 6.065
        if tip_z <= z <= base_z:
            t = (z - tip_z) / (base_z - tip_z)
            half_width = 0.007 + 0.008 * t
            height += 0.016 * (
                1.0 - smoothstep(0.0, 0.002, abs(y - incisor_y) - half_width)
            )

    height -= 0.010 * ellipse_mask(y, z, 0.0, 5.905, 0.13, 0.045, 0.40)
    return max(-0.040, min(0.040, height))


def lanzon_dark(y, z):
    for sign in (-1, 1):
        if ellipse_distance(y, z, sign * 0.160, 6.562, 0.026, 0.022) <= 1.0:
            return True
    if ellipse_distance(y, z, 0.050, 6.135, 0.012, 0.010) <= 1.0:
        return True
    if ellipse_distance(y, z, -0.050, 6.135, 0.012, 0.010) <= 1.0:
        return True
    if lanzon_mouth_mask(y, z) > 0.55 and lanzon_height(y, z) < -0.012:
        return True
    return False


FALCON_BODY = [
    (-0.205, -0.025), (-0.185, 0.045), (-0.145, 0.085),
    (-0.090, 0.110), (-0.020, 0.135), (0.045, 0.142),
    (0.100, 0.130), (0.135, 0.105), (0.160, 0.075),
    (0.195, 0.055), (0.235, 0.025), (0.255, 0.000),
    (0.205, -0.010), (0.175, -0.035), (0.170, -0.045),
    (0.125, -0.055), (0.070, -0.060), (0.030, -0.075),
    (-0.010, -0.090), (-0.045, -0.075), (-0.085, -0.095),
    (-0.105, -0.060), (-0.145, -0.065), (-0.170, -0.040),
]

FALCON_WING = [
    (0.070, 0.095), (0.010, 0.080), (-0.060, 0.055),
    (-0.130, 0.030), (-0.195, 0.005), (-0.178, -0.038),
    (-0.150, -0.018), (-0.142, -0.060), (-0.112, -0.030),
    (-0.104, -0.075), (-0.074, -0.040), (-0.066, -0.085),
    (-0.036, -0.045), (-0.028, -0.082), (0.005, -0.045),
    (0.025, -0.072), (0.052, -0.030), (0.076, -0.005),
]


def falcon_local(y, z, index):
    y_center = FALCON_POSITIONS[index]
    side = -1.0 if y_center < 0 else 1.0
    angle = (-0.10, 0.07, -0.04, 0.09, -0.07, 0.04, -0.09, 0.10)[index]
    scale = (1.00, 0.96, 1.04, 0.98, 1.02, 0.97, 1.05, 0.99)[index]
    a = (y - y_center) * side
    b = z - 6.380
    a, b = rotated(a, b, angle)
    return a / scale, b / scale


def falcon_height(y, z, index):
    a, b = falcon_local(y, z, index)
    body = plateau(polygon_distance(a, b, FALCON_BODY), 0.004)
    wing = plateau(polygon_distance(a, b, FALCON_WING), 0.004)
    head = ellipse_mask(a, b, 0.140, 0.075, 0.058, 0.050, 0.30)

    height = 0.016 * body
    height += 0.010 * wing
    height += 0.005 * head

    for feather in range(4):
        start = (0.020, 0.020 + feather * 0.017)
        end = (-0.145, -0.025 + feather * 0.017)
        height -= 0.007 * polyline_mask(a, b, (start, end), 0.006) * wing

    for tail in range(3):
        start = (-0.175, -0.010 + tail * 0.012)
        end = (-0.260, -0.040 + tail * 0.016)
        height -= 0.004 * polyline_mask(a, b, (start, end), 0.006) * body

    eye = ellipse_mask(a, b, 0.158, 0.086, 0.031, 0.024, 0.35)
    height -= 0.012 * eye
    height += 0.002 * max(
        0.0,
        ellipse_mask(a, b, 0.158, 0.086, 0.042, 0.034, 0.30)
        - ellipse_mask(a, b, 0.158, 0.086, 0.030, 0.023, 0.30),
    )

    beak = 1.0 - smoothstep(0.0, 0.004, abs(b - 0.020 - (a - 0.190) * 0.22) - 0.020)
    beak *= smoothstep(0.185, 0.200, a) * (1.0 - smoothstep(0.255, 0.270, a))
    height += 0.006 * beak

    for crest in range(3):
        start = (0.115 + crest * 0.010, 0.105)
        end = (0.090 + crest * 0.020, 0.160 + crest * 0.005)
        height += 0.004 * polyline_mask(a, b, (start, end), 0.007)

    for leg in range(2):
        start = (-0.010 + leg * 0.060, -0.070)
        end = (-0.040 + leg * 0.060, -0.145)
        height += 0.005 * polyline_mask(a, b, (start, end), 0.008)
        for claw in range(3):
            tip = (end[0] - 0.018 + claw * 0.018, end[1] - 0.022)
            height += 0.004 * polyline_mask(a, b, (end, tip), 0.005)

    return max(0.0, min(0.036, height))


def falcon_dark(y, z, index):
    a, b = falcon_local(y, z, index)
    return ellipse_distance(a, b, 0.158, 0.086, 0.008, 0.007) <= 1.0


def build_relief(name, u0, u1, v0, v1, step, height, project, materials,
                 collection_name, dark=None, us=None, vs=None, angle=40.0, target_tris=None):
    us = us or [u0 + (u1 - u0) * i / max(2, round((u1 - u0) / step))
                for i in range(max(2, round((u1 - u0) / step)) + 1)]
    vs = vs or [v0 + (v1 - v0) * j / max(2, round((v1 - v0) / step))
                for j in range(max(2, round((v1 - v0) / step)) + 1)]
    nu = len(us) - 1
    nv = len(vs) - 1
    front = []
    for v in vs:
        for u in us:
            front.append(project(u, v, height(u, v)))
    stride = nu + 1
    faces = []
    material_indices = []
    for j in range(nv):
        for i in range(nu):
            a = j * stride + i
            faces.append((a, a + 1, a + stride + 1, a + stride))
            uc = (us[i] + us[i + 1]) * 0.5
            vc = (vs[j] + vs[j + 1]) * 0.5
            material_indices.append(0)
    front_count = len(faces)

    mesh = bpy.data.meshes.new("MESH-" + name[4:])
    mesh.from_pydata(front, [], faces)
    mesh.update()
    mesh.validate()
    obj = bpy.data.objects.new(name, mesh)
    bpy.data.collections[collection_name].objects.link(obj)
    for material in materials:
        mesh.materials.append(material)
    for index, polygon in enumerate(mesh.polygons):
        polygon.material_index = material_indices[index]
        polygon.use_smooth = index < front_count
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    if target_tris:
        mesh.calc_loop_triangles()
        current = len(mesh.loop_triangles)
        if current > target_tris:
            modifier = obj.modifiers.new("ReliefDecimate", "DECIMATE")
            modifier.decimate_type = "COLLAPSE"
            modifier.ratio = target_tris / current
            modifier.use_collapse_triangulate = True
            bpy.ops.object.modifier_apply(modifier=modifier.name)
            mesh = obj.data
    if dark:
        for polygon in mesh.polygons:
            center = polygon.center
            polygon.material_index = 1 if dark(center.y, center.z) else 0
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(angle))
    obj["chavin_highpoly"] = "v0.2"
    obj["lod1_exclude"] = True
    obj["units"] = "meters"
    print("RELIEF", name, "faces", len(faces), "step", step)
    return obj


def remove_objects(prefixes):
    removed = 0
    for obj in list(bpy.data.objects):
        if any(obj.name.startswith(prefix) for prefix in prefixes):
            bpy.data.objects.remove(obj, do_unlink=True)
            removed += 1
    print("REMOVED", removed)


def main():
    args = parse_args()
    remove_objects((
        "GEO-Chavin_Lanzon_HP_",
        "GEO-Chavin_Portada_Falcon",
        "GEO-Chavin_Portada_Column_S_HP_",
        "GEO-Chavin_Portada_Column_N_HP_",
        "GEO-Chavin_Portada_Column_S_Relief",
        "GEO-Chavin_Portada_Column_N_Relief",
        "GEO-Chavin_Portada_Column_S_Eye_",
        "GEO-Chavin_Portada_Column_N_Eye_",
        "GEO-Chavin_Portada_Column_S_Fang_",
        "GEO-Chavin_Portada_Column_N_Fang_",
    ))

    base = bpy.data.objects["GEO-Chavin_Lanzon"]
    plain = base.copy()
    plain.data = base.data.copy()
    plain.name = "GEO-Chavin_Lanzon_Plain"
    for collection in base.users_collection:
        collection.objects.link(plain)
    plain["lod0_exclude"] = True
    plain["chavin_highpoly"] = "v0.2"
    plain.hide_render = True
    plain.hide_viewport = True
    base["lod1_exclude"] = True
    bm = bmesh.new()
    bm.from_mesh(base.data)
    bm.faces.ensure_lookup_table()
    front = max(
        (face for face in bm.faces if face.normal.x > 0.99),
        key=lambda face: face.calc_area(),
    )
    bmesh.ops.delete(bm, geom=[front], context="FACES")
    bm.to_mesh(base.data)
    bm.free()
    base.data.update()
    print("LANZON_FRONT_CUT", base.name, "plain", plain.name)

    lanzon = bpy.data.materials["MAT-Chavin_Lanzon"]
    gallery_dark = bpy.data.materials["MAT-Chavin_GalleryDark"]
    shadow = bpy.data.materials.get("MAT-Chavin_Lanzon_Shadow")
    if shadow is None:
        shadow = bpy.data.materials.new("MAT-Chavin_Lanzon_Shadow")
    shadow.use_nodes = True
    shadow_bsdf = next(node for node in shadow.node_tree.nodes if node.type == "BSDF_PRINCIPLED")
    shadow_bsdf.inputs["Base Color"].default_value = (0.060, 0.052, 0.045, 1.0)
    shadow_bsdf.inputs["Roughness"].default_value = 0.9
    shadow_bsdf.inputs["Metallic"].default_value = 0.0
    light = bpy.data.materials["MAT-Chavin_Portada_Light"]
    dark = bpy.data.materials["MAT-Chavin_Portada_Dark"]

    def axis_steps(start, end, dense_start, dense_end, dense_step, sparse_step):
        values = []
        value = start
        while value < dense_start - 1e-6:
            values.append(value)
            value += sparse_step
        value = dense_start
        while value < dense_end - 1e-6:
            values.append(value)
            value += dense_step
        value = dense_end
        while value < end - 1e-6:
            values.append(value)
            value += sparse_step
        values.append(end)
        return values

    lanzon_us = axis_steps(-0.49, 0.49, -LANZON_Y, LANZON_Y, 0.0045, 0.04)
    lanzon_vs = axis_steps(3.0, 7.5, LANZON_Z0, LANZON_Z1, 0.0045, 0.05)
    def lanzon_dark_world(y, z):
        return lanzon_dark(y - LANZON_Y0, z)

    build_relief(
        "GEO-Chavin_Lanzon_HP_FaceRelief",
        -0.49, 0.49, 3.0, 7.5, args.step,
        lanzon_height,
        lambda u, v, h: (lanzon_front_x(v) + h, LANZON_Y0 + u, v),
        (lanzon, shadow), "COL-Chavin_Details", None,
        us=lanzon_us, vs=lanzon_vs, angle=46.0, target_tris=36000,
    )

    for suffix, (u0, u1) in (("S", (-3.20, -0.02)), ("N", (0.02, 3.20))):
        def height(u, v, u0=u0, u1=u1):
            if not (u0 <= u <= u1):
                return 0.0
            result = 0.0
            for index, center in enumerate(FALCON_POSITIONS):
                if abs(u - center) < 0.34:
                    result = max(result, falcon_height(u, v, index))
            return result

        def is_dark(u, v, u0=u0, u1=u1):
            if not (u0 <= u <= u1):
                return False
            return any(
                abs(u - center) < 0.34 and falcon_dark(u, v, index)
                for index, center in enumerate(FALCON_POSITIONS)
            )

        build_relief(
            f"GEO-Chavin_Portada_Frieze_HP_{suffix}",
            u0, u1, FRIEZE_Z0, FRIEZE_Z1, 0.0045,
            height,
            lambda u, v, h: (FRIEZE_X + 0.0005 + h, u, v),
            (light,), "COL-Chavin_Portada", None, angle=32.0, target_tris=28000,
        )

    bpy.context.scene.camera = bpy.data.objects.get("CAM-Chavin_HP_Portada")
    bpy.ops.wm.save_as_mainfile(filepath=args.out_blend)
    meshes = [obj for obj in bpy.data.objects if obj.type == "MESH"]
    for obj in meshes:
        obj.data.calc_loop_triangles()
    print(
        "CHAVIN_RELIEF_SAVED",
        args.out_blend,
        "meshes", len(meshes),
        "tris", sum(len(obj.data.loop_triangles) for obj in meshes),
    )


if __name__ == "__main__":
    main()
