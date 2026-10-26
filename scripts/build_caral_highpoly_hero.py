"""High-poly de Plaza Mayor, Anfiteatro y Altar Circular (v2, Fase B).

Uso:
    blender --background blender/caral/caral_remaster_v2.blend \
      --python scripts/build_caral_highpoly_hero.py

Se ejecuta sobre la escena que ya contiene el high-poly del Mayor.
No exporta GLB ni modifica public/.
"""

import argparse
import json
import math
import random
import sys

import bmesh
import bpy
from mathutils import Vector


SEED = 1270
HIGH_ROOT = "COL-Caral_HighPoly"
LOW_ROOT = "COL-Caral_LowPoly"
EXCLUDED = {
    "COL-Caral_GameExport",
    "COL-Caral_ScenarioCityExport",
    "COL-Caral_Gameplay",
    "COL-Caral_Cameras",
    "COL-Caral_Lights",
}
TAU = math.tau


def parse_args():
    argv = sys.argv
    argv = argv[argv.index("--") + 1 :] if "--" in argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-save", action="store_true")
    return parser.parse_args(argv)


def ensure_collection(name, parent):
    collection = bpy.data.collections.get(name)
    if collection is None:
        collection = bpy.data.collections.new(name)
    if collection.name not in parent.children:
        parent.children.link(collection)
    return collection


def move_to_collection(obj, collection):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    collection.objects.link(obj)


def evaluated_tris(obj, depsgraph):
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh()
    mesh.calc_loop_triangles()
    count = len(mesh.loop_triangles)
    evaluated.to_mesh_clear()
    return count


def bounds(obj):
    points = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    low = Vector(tuple(min(p[i] for p in points) for i in range(3)))
    high = Vector(tuple(max(p[i] for p in points) for i in range(3)))
    return low, high


def in_low_collection(obj):
    return any(collection.name.startswith(LOW_ROOT) for collection in obj.users_collection)


def set_metadata(obj, sublayer, evidence="inferido", source="UNESCO 1269"):
    obj["layer"] = "city"
    obj["sublayer"] = sublayer
    obj["lod"] = 0
    obj["units"] = "meters"
    obj["source"] = source
    obj["evidence"] = evidence


def template_from_bmesh(operation, jitter=0.0, seed=0):
    rng = random.Random(seed)
    bm = bmesh.new()
    operation(bm)
    if jitter:
        for vert in bm.verts:
            if rng.random() < 0.45:
                vert.co += Vector(
                    (
                        rng.uniform(-jitter, jitter),
                        rng.uniform(-jitter, jitter),
                        rng.uniform(-jitter, jitter),
                    )
                )
    bmesh.ops.triangulate(bm, faces=list(bm.faces))
    bm.verts.ensure_lookup_table()
    bm.verts.index_update()
    verts = [vert.co.copy() for vert in bm.verts]
    faces = [tuple(vert.index for vert in face.verts) for face in bm.faces]
    bm.free()
    return verts, faces


def bevel_cube_template(seed):
    def operation(bm):
        bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.bevel(
            bm,
            geom=list(bm.edges),
            offset=0.055,
            segments=1,
            affect="EDGES",
        )

    return template_from_bmesh(operation, jitter=0.012, seed=seed)


def plain_cube_template():
    return template_from_bmesh(lambda bm: bmesh.ops.create_cube(bm, size=1.0))


class MeshAccumulator:
    def __init__(self):
        self.vertices = []
        self.faces = []

    def add_template(self, template, center, dimensions, tangent, normal, rng, jitter=0.0):
        source_vertices, source_faces = template
        origin = len(self.vertices)
        center = Vector(center)
        tangent = Vector(tangent).normalized()
        normal = Vector(normal).normalized()
        up = Vector((0.0, 0.0, 1.0))
        sx, sy, sz = dimensions
        for source in source_vertices:
            dx = source.x * sx
            dy = source.y * sy
            dz = source.z * sz
            if jitter:
                dx += rng.uniform(-jitter, jitter)
                dy += rng.uniform(-jitter, jitter) * 0.5
                dz += rng.uniform(-jitter, jitter) * 0.5
            point = center + tangent * dx + normal * dy + up * dz
            self.vertices.append(tuple(point))
        for face in source_faces:
            self.faces.append(tuple(origin + index for index in face))

    def add_ring(self, center, r_out, r_in, z0, z1, segments=128, start=0.0, end=TAU, caps=False):
        cx, cy = center
        closed = abs((end - start) - TAU) < 1e-6
        count = segments if closed else segments + 1
        radius = (r_out, r_in)
        base = len(self.vertices)
        for index in range(count):
            angle = start + (end - start) * index / segments
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)
            for r in radius:
                self.vertices.append((cx + cos_a * r, cy + sin_a * r, z0))
                self.vertices.append((cx + cos_a * r, cy + sin_a * r, z1))
        for index in range(segments):
            current = base + index * 4
            following = base + ((index + 1) % count) * 4 if closed else current + 4
            ob0, ot0, ib0, it0 = current, current + 1, current + 2, current + 3
            ob1, ot1, ib1, it1 = following, following + 1, following + 2, following + 3
            self.faces.extend(
                [
                    (ob0, ob1, ot1, ot0),
                    (ib1, ib0, it0, it1),
                    (it0, ot0, ot1, it1),
                    (ib1, ib0, ob0, ob1),
                ]
            )
        if caps and not closed:
            first = base
            last = base + segments * 4
            self.faces.extend(
                [
                    (first + 2, first + 3, first + 1, first),
                    (last + 2, last + 3, last + 1, last),
                ]
            )

    def create_object(self, name, material, collection, sublayer, smooth=False, evidence="inferido", source="UNESCO 1269"):
        mesh = bpy.data.meshes.new(name + "_Mesh")
        mesh.from_pydata(self.vertices, [], self.faces)
        mesh.update()
        bm = bmesh.new()
        bm.from_mesh(mesh)
        bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
        bm.to_mesh(mesh)
        bm.free()
        mesh.update()
        if material is not None:
            mesh.materials.append(material)
        uv = mesh.uv_layers.new(name="UVMap")
        for polygon in mesh.polygons:
            polygon.use_smooth = smooth
            normal = polygon.normal
            axis = max(range(3), key=lambda i: abs(normal[i]))
            for loop_index in polygon.loop_indices:
                vertex = mesh.vertices[mesh.loops[loop_index].vertex_index].co
                if axis == 0:
                    coord = (vertex.y * 0.0625, vertex.z * 0.0625)
                elif axis == 1:
                    coord = (vertex.x * 0.0625, vertex.z * 0.0625)
                else:
                    coord = (vertex.x * 0.0625, vertex.y * 0.0625)
                uv.data[loop_index].uv = coord
        obj = bpy.data.objects.new(name, mesh)
        collection.objects.link(obj)
        set_metadata(obj, sublayer, evidence, source)
        mesh.calc_loop_triangles()
        print(f"MESH {name} verts={len(mesh.vertices)} tris={len(mesh.loop_triangles)}")
        return obj


def add_rect_patch(
    stone_acc,
    weathered_acc,
    mortar_acc,
    origin,
    tangent,
    normal,
    z0,
    z1,
    length,
    budget,
    rng,
    templates,
    plain,
    row_height=0.34,
):
    origin = Vector(origin)
    tangent = Vector(tangent).normalized()
    normal = Vector(normal).normalized()
    rows = max(2, round((z1 - z0) / row_height))
    actual_row = (z1 - z0) / rows
    per_row = max(2, round(budget / rows))
    patch_length = min(length, per_row * 0.95)
    used = 0
    for row in range(rows):
        left_shift = rng.uniform(-0.18, 0.18)
        right_shift = rng.uniform(-0.18, 0.18)
        row_length = max(0.6, patch_length + right_shift - left_shift)
        z = z0 + (row + 0.5) * actual_row
        mortar_center = origin + tangent * (left_shift + row_length * 0.5) + normal * 0.008
        mortar_center.z = z
        mortar_acc.add_template(
            plain,
            mortar_center,
            (row_length, 0.022, actual_row * 0.98),
            tangent,
            normal,
            rng,
        )
        cursor = max(0.0, left_shift)
        limit = left_shift + row_length
        while cursor < limit - 0.18 and used < budget:
            block_length = min(rng.uniform(0.42, 1.25), limit - cursor)
            if block_length < 0.2:
                break
            edge = min(cursor - left_shift, limit - cursor)
            if rng.random() < (0.22 if edge < 0.7 else 0.06):
                cursor += block_length + rng.uniform(0.02, 0.04)
                continue
            depth = rng.uniform(0.05, 0.15)
            center = origin + tangent * (cursor + block_length * 0.5)
            center += normal * (0.012 + depth * 0.5)
            center.z = z + rng.uniform(-0.028, 0.028)
            target = weathered_acc if rng.random() < 0.16 else stone_acc
            target.add_template(
                rng.choice(templates),
                center,
                (max(0.2, block_length - 0.025), depth, actual_row * rng.uniform(0.78, 0.96)),
                tangent,
                normal,
                rng,
                jitter=0.012,
            )
            used += 1
            cursor += block_length + rng.uniform(0.02, 0.04)
    return used


def add_arc_patch(
    stone_acc,
    weathered_acc,
    mortar_acc,
    center,
    radius,
    z0,
    z1,
    arc_start,
    arc_end,
    budget,
    inward,
    rng,
    templates,
    plain,
    row_height=0.34,
):
    rows = max(2, round((z1 - z0) / row_height))
    actual_row = (z1 - z0) / rows
    per_row = max(2, round(budget / rows))
    arc_length = abs(arc_end - arc_start) * radius
    patch_angle = min(abs(arc_end - arc_start), per_row * 0.95 / radius)
    max_start = min(arc_start, arc_end) + max(0.0, abs(arc_end - arc_start) - patch_angle)
    row_angle = min_start = rng.uniform(min(arc_start, arc_end), max_start)
    used = 0
    for row in range(rows):
        local_start = min_start + rng.uniform(-0.008, 0.008)
        local_end = local_start + patch_angle
        z = z0 + (row + 0.5) * actual_row
        cursor_angle = local_start
        while cursor_angle < local_end and used < budget:
            block_angle = min(rng.uniform(0.42, 1.2) / radius, local_end - cursor_angle)
            if block_angle * radius < 0.2:
                break
            mid_angle = cursor_angle + block_angle * 0.5
            radial = Vector((math.cos(mid_angle), math.sin(mid_angle), 0.0))
            tangent = Vector((-math.sin(mid_angle), math.cos(mid_angle), 0.0))
            normal = -radial if inward else radial
            surface = Vector((center[0], center[1], 0.0)) + radial * radius
            edge = min(cursor_angle - local_start, local_end - cursor_angle) * radius
            if rng.random() < (0.22 if edge < 0.7 else 0.06):
                cursor_angle += block_angle
                continue
            depth = rng.uniform(0.05, 0.15)
            mortar_center = surface + normal * 0.008
            mortar_center.z = z
            mortar_acc.add_template(
                plain,
                mortar_center,
                (block_angle * radius * 0.98, 0.022, actual_row * 0.98),
                tangent,
                normal,
                rng,
            )
            stone_center = surface + normal * (0.012 + depth * 0.5)
            stone_center.z = z + rng.uniform(-0.028, 0.028)
            target = weathered_acc if rng.random() < 0.16 else stone_acc
            target.add_template(
                rng.choice(templates),
                stone_center,
                (block_angle * radius - 0.025, depth, actual_row * rng.uniform(0.78, 0.96)),
                tangent,
                normal,
                rng,
                jitter=0.012,
            )
            used += 1
            cursor_angle += block_angle
    return used


def add_quoins(acc, low, high, rng, templates, courses=4, size=0.62):
    count = 0
    course_h = (high.z - low.z) / courses
    for x in (low.x, high.x):
        for y in (low.y, high.y):
            for course in range(courses):
                center = Vector((x, y, low.z + (course + 0.5) * course_h))
                center.x += 0.025 if course % 2 else -0.025
                acc.add_template(
                    rng.choice(templates),
                    center,
                    (size, size, course_h - 0.035),
                    (1, 0, 0),
                    (0, 1, 0),
                    rng,
                    jitter=0.012,
                )
                count += 1
    return count


def add_stairs_from_bounds(acc, obj, rng, templates, plain, max_steps=18):
    low, high = bounds(obj)
    center_x = (low.x + high.x) * 0.5
    width = high.x - low.x
    depth = high.y - low.y
    height = high.z - low.z
    steps = max(4, min(max_steps, round(height / 0.32)))
    tread = depth / steps
    rise = height / steps
    count = 0
    for index in range(steps):
        front_y = low.y + index * tread
        top_z = low.z + (index + 1) * rise
        body_depth = high.y - front_y
        body_height = top_z - low.z
        center = Vector((center_x, (front_y + high.y) * 0.5, low.z + body_height * 0.5))
        acc.add_template(
            plain,
            center,
            (width, body_depth, body_height),
            (1, 0, 0),
            (0, 1, 0),
            rng,
        )
        cap_center = Vector((center_x, front_y + 0.07, top_z + 0.012))
        acc.add_template(
            rng.choice(templates),
            cap_center,
            (width - 0.05, 0.16, 0.085),
            (1, 0, 0),
            (0, 1, 0),
            rng,
            jitter=0.006,
        )
        count += 1
    return count


def duplicate_base(objects, skip_names, high_collection, low_collection, sublayer, source, prefix):
    for obj in objects:
        move_to_collection(obj, low_collection)
        obj["lod"] = 1
        obj["layer"] = "city"
        obj["sublayer"] = sublayer
        suffix = obj.name[len(prefix) :].lstrip("_")
        if suffix in skip_names:
            continue
        duplicate = obj.copy()
        duplicate.data = obj.data.copy()
        duplicate.name = f"GEO-Caral_HighPoly_{sublayer}_{suffix}"
        high_collection.objects.link(duplicate)
        set_metadata(duplicate, sublayer, "documentado", source)


def build_plaza(rng, templates, plain, high_root, low_root):
    sublayer = "plaza-mayor"
    high = ensure_collection(f"{HIGH_ROOT}_PlazaMayor", high_root)
    low = ensure_collection(f"{LOW_ROOT}_PlazaMayor", low_root)
    objects = [o for o in bpy.data.objects if o.type == "MESH" and o.name.startswith("GEO-Caral_PlazaMayor")]
    source = "UNESCO 1269 p. 351"
    skip = {
        "Anillo",
        "BandaRoja",
        "Cornisa",
        "Zocalo",
        "EscaleraExterior",
        "EscaleraInterior_N",
        "EscaleraInterior_S",
        "FogonAro",
    }
    duplicate_base(objects, skip, high, low, sublayer, source, "GEO-Caral_PlazaMayor_")

    field_acc = MeshAccumulator()
    weathered_acc = MeshAccumulator()
    mortar_acc = MeshAccumulator()
    ring_acc = MeshAccumulator()
    band_acc = MeshAccumulator()
    cornice_acc = MeshAccumulator()
    zocalo_acc = MeshAccumulator()
    fogon_acc = MeshAccumulator()
    stairs_acc = MeshAccumulator()

    center = (0.0, 62.9)
    r_out = 18.25
    r_in = 10.75
    ring_acc.add_ring(center, r_out, r_in, -2.0, 1.5, 128)
    band_acc.add_ring(center, 18.50, 18.25, 1.20, 1.35, 128)
    cornice_acc.add_ring(center, 18.40, 18.25, 1.45, 1.60, 128)
    zocalo_acc.add_ring(center, 18.55, 18.25, -0.40, 0.20, 128)
    fogon_acc.add_ring(center, 1.50, 1.05, -1.95, -1.72, 64)

    inner_arcs = [(math.radians(185), math.radians(235)), (math.radians(250), math.radians(300)), (math.radians(75), math.radians(125))]
    for arc in inner_arcs:
        add_arc_patch(field_acc, weathered_acc, mortar_acc, center, r_in, -1.90, 1.35, arc[0], arc[1], 52, True, rng, templates, plain)
    outer_arcs = [(math.radians(195), math.radians(250)), (math.radians(15), math.radians(65))]
    for arc in outer_arcs:
        add_arc_patch(field_acc, weathered_acc, mortar_acc, center, r_out, 0.15, 1.40, arc[0], arc[1], 30, False, rng, templates, plain)

    stair_objects = [o for o in objects if "Escalera" in o.name]
    for stair in stair_objects:
        add_stairs_from_bounds(stairs_acc, stair, rng, templates, plain)

    ring_acc.create_object("GEO-Caral_HighPoly_PlazaMayor_Ring", bpy.data.materials["MAT-Caral_Remaster_Plaster_White"], high, sublayer, evidence="documentado", source=source)
    band_acc.create_object("GEO-Caral_HighPoly_PlazaMayor_BandRed", bpy.data.materials["MAT-Caral_Remaster_Plaster_Red"], high, sublayer, evidence="documentado", source=source)
    cornice_acc.create_object("GEO-Caral_HighPoly_PlazaMayor_Cornice", bpy.data.materials["MAT-Caral_Remaster_Plaster_Yellow"], high, sublayer, evidence="documentado", source=source)
    zocalo_acc.create_object("GEO-Caral_HighPoly_PlazaMayor_Zocalo", bpy.data.materials["MAT-Caral_Remaster_Stone_Cut"], high, sublayer, evidence="inferido", source=source)
    fogon_acc.create_object("GEO-Caral_HighPoly_PlazaMayor_FogonAro", bpy.data.materials["MAT-Caral_Remaster_Stone_Cut"], high, sublayer, evidence="inferido", source=source)
    field_acc.create_object("GEO-Caral_HighPoly_PlazaMayor_Stone_Field", bpy.data.materials["MAT-Caral_Remaster_Stone_Field"], high, sublayer, evidence="inferido", source=source)
    weathered_acc.create_object("GEO-Caral_HighPoly_PlazaMayor_Stone_Weathered", bpy.data.materials["MAT-Caral_Remaster_Rock"], high, sublayer, evidence="interpretativo", source=source)
    mortar_acc.create_object("GEO-Caral_HighPoly_PlazaMayor_Mortar", bpy.data.materials["MAT-Caral_Remaster_Mortar"], high, sublayer, evidence="interpretativo", source=source)
    stairs_acc.create_object("GEO-Caral_HighPoly_PlazaMayor_Stairs", bpy.data.materials["MAT-Caral_Remaster_Stone_Cut"], high, sublayer, evidence="inferido", source=source)
    print("PLAZA_DONE")


def build_anfiteatro(rng, templates, plain, high_root, low_root):
    sublayer = "anfiteatro"
    high = ensure_collection(f"{HIGH_ROOT}_Anfiteatro", high_root)
    low = ensure_collection(f"{LOW_ROOT}_Anfiteatro", low_root)
    objects = [o for o in bpy.data.objects if o.type == "MESH" and o.name.startswith("GEO-Caral_Anfiteatro")]
    source = "UNESCO 1269 p. 358"
    skip = {
        "PlazaAnillo",
        "Graderia_01",
        "Graderia_02",
        "Graderia_03",
        "EscaleraPlaza",
        "EscaleraTemplo",
        "Templo_Stair_02",
        "Templo_Stair_03",
        "Templo_Stair_Ground",
    }
    duplicate_base(objects, skip, high, low, sublayer, source, "GEO-Caral_Anfiteatro_")

    field_acc = MeshAccumulator()
    weathered_acc = MeshAccumulator()
    mortar_acc = MeshAccumulator()
    ring_acc = MeshAccumulator()
    coping_acc = MeshAccumulator()
    graderia_acc = MeshAccumulator()
    nosing_acc = MeshAccumulator()
    stairs_acc = MeshAccumulator()

    center = (0.0, -338.0)
    add_ring = ring_acc.add_ring
    add_ring(center, 18.5, 14.5, -2.5, 1.0, 128)
    coping_acc.add_ring(center, 18.65, 18.50, 1.0, 1.12, 128)

    for arc in [(math.radians(180), math.radians(235)), (math.radians(250), math.radians(310)), (math.radians(60), math.radians(120))]:
        add_arc_patch(field_acc, weathered_acc, mortar_acc, center, 14.5, -2.40, 0.90, arc[0], arc[1], 60, True, rng, templates, plain)
    for arc in [(math.radians(195), math.radians(250)), (math.radians(10), math.radians(65))]:
        add_arc_patch(field_acc, weathered_acc, mortar_acc, center, 18.5, 0.05, 0.95, arc[0], arc[1], 35, False, rng, templates, plain)

    tiers = [
        (18.5, 21.5, 1.6, 30),
        (21.5, 24.5, 2.4, 25),
        (24.5, 27.5, 3.2, 20),
    ]
    for r_in, r_out, top, blocks in tiers:
        graderia_acc.add_ring(center, r_out, r_in, 0.0, top, 72, math.pi, TAU, caps=True)
        nosing_acc.add_ring(center, r_out + 0.12, r_out, top, top + 0.07, 72, math.pi, TAU, caps=True)
        add_arc_patch(field_acc, weathered_acc, mortar_acc, center, r_out, 0.0, top, math.radians(195), math.radians(250), blocks, False, rng, templates, plain, row_height=0.42)

    temple = [o for o in objects if "Templo_Terrace" in o.name or "Templo_Summit" in o.name or "Templo_Zocalo" in o.name or "Muralla" in o.name]
    for obj in temple:
        low_b, high_b = bounds(obj)
        if "Templo_Terrace_01" in obj.name:
            south_budget, west_budget = 60, 40
        elif "Templo_Terrace_02" in obj.name:
            south_budget, west_budget = 45, 30
        elif "Templo_Terrace_03" in obj.name:
            south_budget, west_budget = 35, 25
        elif "Muralla" in obj.name:
            south_budget, west_budget = 30, 20
        else:
            south_budget, west_budget = 25, 18
        for normal, tangent, origin, length, budget in [
            ((0, -1, 0), (1, 0, 0), Vector((low_b.x, low_b.y, 0)), (high_b.x - low_b.x) * 0.58, south_budget),
            ((-1, 0, 0), (0, 1, 0), Vector((low_b.x, low_b.y, 0)), (high_b.y - low_b.y) * 0.45, west_budget),
        ]:
            add_rect_patch(field_acc, weathered_acc, mortar_acc, origin, tangent, normal, low_b.z, high_b.z, length, budget, rng, templates, plain)
        add_quoins(field_acc, low_b, high_b, rng, templates, courses=3, size=0.55)

    for stair in [o for o in objects if "Escalera" in o.name]:
        add_stairs_from_bounds(stairs_acc, stair, rng, templates, plain, max_steps=18)

    ring_acc.create_object("GEO-Caral_HighPoly_Anfiteatro_Ring", bpy.data.materials["MAT-Caral_Remaster_Plaster_White"], high, sublayer, evidence="documentado", source=source)
    coping_acc.create_object("GEO-Caral_HighPoly_Anfiteatro_RingCoping", bpy.data.materials["MAT-Caral_Remaster_Stone_Cut"], high, sublayer, evidence="inferido", source=source)
    graderia_acc.create_object("GEO-Caral_HighPoly_Anfiteatro_Graderias", bpy.data.materials["MAT-Caral_Remaster_Stone_Field"], high, sublayer, evidence="documentado", source=source)
    nosing_acc.create_object("GEO-Caral_HighPoly_Anfiteatro_GraderiaNosing", bpy.data.materials["MAT-Caral_Remaster_Stone_Cut"], high, sublayer, evidence="inferido", source=source)
    field_acc.create_object("GEO-Caral_HighPoly_Anfiteatro_Stone_Field", bpy.data.materials["MAT-Caral_Remaster_Stone_Field"], high, sublayer, evidence="inferido", source=source)
    weathered_acc.create_object("GEO-Caral_HighPoly_Anfiteatro_Stone_Weathered", bpy.data.materials["MAT-Caral_Remaster_Rock"], high, sublayer, evidence="interpretativo", source=source)
    mortar_acc.create_object("GEO-Caral_HighPoly_Anfiteatro_Mortar", bpy.data.materials["MAT-Caral_Remaster_Mortar"], high, sublayer, evidence="interpretativo", source=source)
    stairs_acc.create_object("GEO-Caral_HighPoly_Anfiteatro_Stairs", bpy.data.materials["MAT-Caral_Remaster_Stone_Cut"], high, sublayer, evidence="inferido", source=source)
    print("ANFITEATRO_DONE")


def build_altar(rng, templates, plain, high_root, low_root):
    sublayer = "altar-circular"
    high = ensure_collection(f"{HIGH_ROOT}_AltarCircular", high_root)
    low = ensure_collection(f"{LOW_ROOT}_AltarCircular", low_root)
    objects = [o for o in bpy.data.objects if o.type == "MESH" and o.name.startswith("GEO-Caral_AltarCircular")]
    source = "UNESCO 1269 p. 359"
    skip = {"Aro", "Altar", "Stair_02", "Stair_Ground"}
    duplicate_base(objects, skip, high, low, sublayer, source, "GEO-Caral_AltarCircular_")

    field_acc = MeshAccumulator()
    weathered_acc = MeshAccumulator()
    mortar_acc = MeshAccumulator()
    altar_acc = MeshAccumulator()
    altar_top_acc = MeshAccumulator()
    stairs_acc = MeshAccumulator()

    center = (-110.0, -300.0)
    altar_acc.add_ring(center, 1.35, 0.90, 4.0, 5.5, 64)
    altar_top_acc.add_ring(center, 1.45, 1.35, 5.42, 5.52, 64)
    add_arc_patch(field_acc, weathered_acc, mortar_acc, center, 1.35, 4.05, 5.38, math.radians(190), math.radians(320), 48, False, rng, templates, plain, row_height=0.3)

    for obj in [o for o in objects if "Terrace" in o.name or "Summit" in o.name]:
        low_b, high_b = bounds(obj)
        if "Terrace_01" in obj.name:
            south_budget, west_budget = 90, 45
        elif "Terrace_02" in obj.name:
            south_budget, west_budget = 60, 30
        else:
            south_budget, west_budget = 30, 20
        for normal, tangent, origin, length, budget in [
            ((0, -1, 0), (1, 0, 0), Vector((low_b.x, low_b.y, 0)), (high_b.x - low_b.x) * 0.55, south_budget),
            ((-1, 0, 0), (0, 1, 0), Vector((low_b.x, low_b.y, 0)), (high_b.y - low_b.y) * 0.42, west_budget),
        ]:
            add_rect_patch(field_acc, weathered_acc, mortar_acc, origin, tangent, normal, low_b.z, high_b.z, length, budget, rng, templates, plain)
        add_quoins(field_acc, low_b, high_b, rng, templates, courses=3, size=0.52)

    for stair in [o for o in objects if "Stair" in o.name]:
        add_stairs_from_bounds(stairs_acc, stair, rng, templates, plain, max_steps=12)

    altar_acc.create_object("GEO-Caral_HighPoly_AltarCircular_AltarRing", bpy.data.materials["MAT-Caral_Stone_Dark"], high, sublayer, evidence="documentado", source=source)
    altar_top_acc.create_object("GEO-Caral_HighPoly_AltarCircular_AltarCoping", bpy.data.materials["MAT-Caral_Remaster_Stone_Cut"], high, sublayer, evidence="inferido", source=source)
    field_acc.create_object("GEO-Caral_HighPoly_AltarCircular_Stone_Field", bpy.data.materials["MAT-Caral_Remaster_Stone_Field"], high, sublayer, evidence="inferido", source=source)
    weathered_acc.create_object("GEO-Caral_HighPoly_AltarCircular_Stone_Weathered", bpy.data.materials["MAT-Caral_Remaster_Rock"], high, sublayer, evidence="interpretativo", source=source)
    mortar_acc.create_object("GEO-Caral_HighPoly_AltarCircular_Mortar", bpy.data.materials["MAT-Caral_Remaster_Mortar"], high, sublayer, evidence="interpretativo", source=source)
    stairs_acc.create_object("GEO-Caral_HighPoly_AltarCircular_Stairs", bpy.data.materials["MAT-Caral_Remaster_Stone_Cut"], high, sublayer, evidence="inferido", source=source)
    print("ALTAR_DONE")


def make_cameras():
    def camera(name, location, target, lens):
        old = bpy.data.objects.get(name)
        if old is not None:
            bpy.data.objects.remove(old, do_unlink=True)
        data = bpy.data.cameras.new(name + "_Data")
        data.lens = lens
        data.sensor_width = 36
        obj = bpy.data.objects.new(name, data)
        bpy.data.collections["COL-Caral_Cameras"].objects.link(obj)
        obj.location = location
        obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()
        return obj

    camera("CAM-Caral_V2_Plaza", (-50, -10, 30), (0, 63, 0), 50)
    camera("CAM-Caral_V2_PlazaDetail", (-6, 54.5, 0.4), (0, 62.9, -0.5), 35)
    camera("CAM-Caral_V2_Anfiteatro", (-150, -460, 58), (0, -330, 4), 42)
    camera("CAM-Caral_V2_Altar", (-155, -345, 32), (-110, -300, 4), 45)
    camera("CAM-Caral_V2_AltarDetail", (-114, -309, 8.5), (-110, -300, 4.6), 55)


def main():
    args = parse_args()
    if not bpy.data.filepath.endswith("caral_remaster_v2.blend"):
        raise RuntimeError("Abrir blender/caral/caral_remaster_v2.blend antes de ejecutar")
    for name in ["COL-Caral_HighPoly_PlazaMayor", "COL-Caral_HighPoly_Anfiteatro", "COL-Caral_HighPoly_AltarCircular"]:
        if bpy.data.collections.get(name) is not None:
            raise RuntimeError(f"{name} ya existe; no se duplicará la Fase B")

    high_root = bpy.data.collections[HIGH_ROOT]
    low_root = bpy.data.collections[LOW_ROOT]
    rng = random.Random(SEED)
    templates = [bevel_cube_template(SEED + index) for index in range(6)]
    plain = plain_cube_template()

    depsgraph = bpy.context.evaluated_depsgraph_get()
    export_objects = [
        obj
        for obj in bpy.data.objects
        if obj.type == "MESH" and not any(c.name in EXCLUDED for c in obj.users_collection)
    ]
    high_mayor = [o for o in bpy.data.objects if o.type == "MESH" and o.name.startswith("GEO-Caral_HighPoly_Mayor")]
    before_other = [o for o in export_objects if not in_low_collection(o) and not o.name.startswith("GEO-Caral_HighPoly_")]
    before_total = sum(evaluated_tris(o, depsgraph) for o in high_mayor) + sum(evaluated_tris(o, depsgraph) for o in before_other)
    print(f"BEFORE_LOD0 {before_total}")

    build_plaza(rng, templates, plain, high_root, low_root)
    build_anfiteatro(rng, templates, plain, high_root, low_root)
    build_altar(rng, templates, plain, high_root, low_root)
    make_cameras()

    low_root.hide_render = True
    low_root.hide_viewport = True
    high_root.hide_render = False
    high_root.hide_viewport = False
    bpy.context.view_layer.update()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    high_objects = [o for o in bpy.data.objects if o.type == "MESH" and o.name.startswith("GEO-Caral_HighPoly_")]
    other_objects = [
        o
        for o in bpy.data.objects
        if o.type == "MESH"
        and not any(c.name in EXCLUDED for c in o.users_collection)
        and not in_low_collection(o)
        and not o.name.startswith("GEO-Caral_HighPoly_")
    ]
    per_region = {}
    for region, collection_name in {
        "Mayor": "COL-Caral_HighPoly_Mayor",
        "PlazaMayor": "COL-Caral_HighPoly_PlazaMayor",
        "Anfiteatro": "COL-Caral_HighPoly_Anfiteatro",
        "AltarCircular": "COL-Caral_HighPoly_AltarCircular",
    }.items():
        objs = [o for o in bpy.data.collections[collection_name].objects if o.type == "MESH"]
        per_region[region] = sum(evaluated_tris(o, depsgraph) for o in objs)
    after_total = sum(evaluated_tris(o, depsgraph) for o in high_objects) + sum(
        evaluated_tris(o, depsgraph) for o in other_objects
    )
    metrics = {
        "before_lod0_tris": before_total,
        "after_lod0_tris": after_total,
        "highpoly_objects": len(high_objects),
        "per_region_tris": per_region,
        "seed": SEED,
        "note": "Alterar contadores de piedra si se excede 250k",
    }
    print("V2B_METRICS " + json.dumps(metrics, sort_keys=True))
    if after_total > 250000:
        raise RuntimeError(f"LOD0 excedido: {after_total} tris > 250000")
    if not args.no_save:
        bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
        print(f"SAVED {bpy.data.filepath}")


if __name__ == "__main__":
    main()
