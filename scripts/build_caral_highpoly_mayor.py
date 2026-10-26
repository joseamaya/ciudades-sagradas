"""Prototipo high-poly de la Pirámide Mayor de Caral (v2, Fase A).

Uso:
    blender --background blender/caral/caral_remaster_v2.blend \
      --python scripts/build_caral_highpoly_mayor.py

No exporta GLB. Conserva el Mayor v1 en COL-Caral_LowPoly_Mayor.
Dimensiones de referencia: UNESCO 1269, p. 351 (170,80 × 149,69 m; 29,88 m).
"""

import argparse
import json
import math
import random
import sys

import bmesh
import bpy
from mathutils import Vector


SEED = 1269
FIELD_STONE_BUDGET = 2000
HIGH_ROOT = "COL-Caral_HighPoly"
HIGH_MAYOR = "COL-Caral_HighPoly_Mayor"
LOW_ROOT = "COL-Caral_LowPoly"
LOW_MAYOR = "COL-Caral_LowPoly_Mayor"
PREFIX = "GEO-Caral_PyramideMayor"
EXCLUDED = {
    "COL-Caral_GameExport",
    "COL-Caral_ScenarioCityExport",
    "COL-Caral_Gameplay",
    "COL-Caral_Cameras",
    "COL-Caral_Lights",
}


def parse_args():
    argv = sys.argv
    argv = argv[argv.index("--") + 1 :] if "--" in argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--field-stones", type=int, default=FIELD_STONE_BUDGET)
    parser.add_argument("--no-save", action="store_true")
    return parser.parse_args(argv)


def ensure_collection(name, parent=None):
    collection = bpy.data.collections.get(name)
    if collection is None:
        collection = bpy.data.collections.new(name)
    if parent is not None and collection.name not in parent.children:
        parent.children.link(collection)
    elif parent is None and collection.name not in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.link(collection)
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


def set_metadata(obj, evidence="inferido"):
    obj["layer"] = "city"
    obj["sublayer"] = "mayor"
    obj["lod"] = 0
    obj["units"] = "meters"
    obj["source"] = "UNESCO 1269 pp. 349-351 / Zona Arqueologica Caral"
    obj["evidence"] = evidence


def make_mortar_material():
    name = "MAT-Caral_Remaster_Mortar"
    material = bpy.data.materials.get(name)
    if material is None:
        material = bpy.data.materials.new(name)
    material.use_nodes = True
    bsdf = next(node for node in material.node_tree.nodes if node.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (0.20, 0.165, 0.125, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.96
    bsdf.inputs["Metallic"].default_value = 0.0
    material.diffuse_color = (0.20, 0.165, 0.125, 1.0)
    return material


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


def sphere_template():
    return template_from_bmesh(
        lambda bm: bmesh.ops.create_uvsphere(bm, u_segments=12, v_segments=8, radius=0.5)
    )


def ico_template():
    return template_from_bmesh(
        lambda bm: bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.5)
    )


def cylinder_template():
    return template_from_bmesh(
        lambda bm: bmesh.ops.create_cone(
            bm,
            cap_ends=True,
            cap_tris=False,
            segments=12,
            radius1=0.5,
            radius2=0.5,
            depth=1.0,
        )
    )


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

    def create_object(self, name, material, collection, smooth=False, evidence="inferido"):
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
        set_metadata(obj, evidence)
        mesh.calc_loop_triangles()
        print(f"MESH {name} verts={len(mesh.vertices)} tris={len(mesh.loop_triangles)}")
        return obj


def wall_definitions(low, high):
    xmin, ymin, zmin = low
    xmax, ymax, zmax = high
    return [
        ("S", (xmin, xmax), ymin, (1, 0, 0), (0, -1, 0)),
        ("N", (xmin, xmax), ymax, (1, 0, 0), (0, 1, 0)),
        ("W", (ymin, ymax), xmin, (0, 1, 0), (-1, 0, 0)),
        ("E", (ymin, ymax), xmax, (0, 1, 0), (1, 0, 0)),
    ]


def generate_wall_stones(terraces, stone_acc, weathered_acc, mortar_acc, templates, plain, rng, budget):
    candidates = []
    visibility = {"S": 1.0, "W": 0.85, "E": 0.65, "N": 0.45}
    for level, terrace in enumerate(terraces):
        low, high = bounds(terrace)
        for side, span, plane, tangent, normal in wall_definitions(low, high):
            weight = visibility[side] * max(0.35, 1.25 - level * 0.13)
            candidates.append((level, terrace, side, span, plane, tangent, normal, weight))
    total_weight = sum(item[-1] for item in candidates)
    used = 0
    for level, terrace, side, span, plane, tangent, normal, weight in candidates:
        allocation = max(18, round(budget * weight / total_weight))
        low, high = bounds(terrace)
        zmin, zmax = low.z, high.z
        wall_height = zmax - zmin
        rows = max(8, round(wall_height / 0.36))
        row_height = wall_height / rows
        per_row = max(2, round(allocation / rows))
        patch_length = min((span[1] - span[0]) * 0.42, per_row * 1.08)
        if side == "S" and level < 4:
            anchor = 0.08 if level % 2 == 0 else 0.68
        else:
            anchor = rng.uniform(0.06, 0.72)
        patch_start = span[0] + (span[1] - span[0] - patch_length) * anchor
        patch_end = patch_start + patch_length
        count = 0
        for row in range(rows):
            left = patch_start + rng.uniform(-0.32, 0.32)
            right = patch_end + rng.uniform(-0.32, 0.32)
            if row % 2:
                left += 0.35
                right += 0.35
            left = max(span[0] + 0.12, left)
            right = min(span[1] - 0.12, right)
            if right - left < 0.5:
                continue
            z = zmin + (row + 0.5) * row_height
            mortar_center = Vector((0, 0, 0))
            mortar_center += Vector(tangent) * ((left + right) * 0.5)
            if abs(normal[0]) > 0.5:
                mortar_center.x = plane + normal[0] * 0.012
            else:
                mortar_center.y = plane + normal[1] * 0.012
            mortar_center.z = z
            mortar_acc.add_template(
                plain,
                mortar_center,
                (right - left, 0.025, row_height * 0.98),
                tangent,
                normal,
                rng,
            )
            cursor = left
            while cursor < right - 0.18 and count < allocation:
                length = min(rng.uniform(0.45, 1.75), right - cursor)
                if length < 0.22:
                    break
                edge_distance = min(cursor - left, right - cursor)
                missing_chance = 0.24 if edge_distance < 0.8 else 0.07
                if rng.random() < missing_chance:
                    cursor += length + rng.uniform(0.02, 0.045)
                    continue
                depth = rng.uniform(0.05, 0.20)
                center = Vector((0, 0, 0))
                center += Vector(tangent) * (cursor + length * 0.5)
                if abs(normal[0]) > 0.5:
                    center.x = plane + normal[0] * (0.018 + depth * 0.5)
                else:
                    center.y = plane + normal[1] * (0.018 + depth * 0.5)
                center.z = z + rng.uniform(-0.035, 0.035)
                target_acc = weathered_acc if rng.random() < 0.18 else stone_acc
                target_acc.add_template(
                    rng.choice(templates),
                    center,
                    (max(0.18, length - 0.028), depth, row_height * rng.uniform(0.78, 0.96)),
                    tangent,
                    normal,
                    rng,
                    jitter=0.015,
                )
                count += 1
                used += 1
                cursor += length + rng.uniform(0.02, 0.045)
    print(f"WALL_STONES {used}")
    return used


def generate_quoins(terraces, cut_acc, templates, rng):
    count = 0
    for terrace in terraces:
        low, high = bounds(terrace)
        courses = 7
        height = (high.z - low.z) / courses
        for x in (low.x, high.x):
            for y in (low.y, high.y):
                for course in range(courses):
                    center = Vector((x, y, low.z + (course + 0.5) * height))
                    center.x += 0.035 if course % 2 else -0.035
                    cut_acc.add_template(
                        rng.choice(templates),
                        center,
                        (0.92, 0.92, height - 0.035),
                        (1, 0, 0),
                        (0, 1, 0),
                        rng,
                        jitter=0.014,
                    )
                    count += 1
    print(f"QUOINS {count}")


def generate_stairs(stair_objects, cut_acc, templates, plain, rng):
    steps = 16
    count = 0
    for stair in sorted(stair_objects, key=lambda obj: bounds(obj)[0].z):
        low, high = bounds(stair)
        tread = (high.y - low.y) / steps
        rise = (high.z - low.z) / steps
        for index in range(steps):
            front_y = low.y + index * tread
            top_z = low.z + (index + 1) * rise
            body_depth = high.y - front_y
            body_height = top_z - low.z
            center = Vector((0, (front_y + high.y) * 0.5, low.z + body_height * 0.5))
            cut_acc.add_template(
                plain,
                center,
                (high.x - low.x, body_depth, body_height),
                (1, 0, 0),
                (0, 1, 0),
                rng,
            )
            segments = 3
            segment_width = (high.x - low.x) / segments
            for segment in range(segments):
                cap_center = Vector(
                    (
                        low.x + (segment + 0.5) * segment_width,
                        front_y + 0.065,
                        top_z + 0.012,
                    )
                )
                cut_acc.add_template(
                    rng.choice(templates),
                    cap_center,
                    (segment_width - 0.025, 0.15, 0.085),
                    (1, 0, 0),
                    (0, 1, 0),
                    rng,
                    jitter=0.006,
                )
                count += 1
    print(f"STAIR_NOSING_STONES {count}")


def generate_shicras(first_terrace, bag_acc, stone_acc, mortar_acc, bag_template, tie_template, ico, plain, rng):
    low, high = bounds(first_terrace)
    south_y = low.y
    for row in range(2):
        for column in range(5):
            x = -75.0 + column * 0.86 + (0.18 if row else 0.0)
            z = 0.46 + row * 0.54
            center = Vector((x, south_y - 0.17, z))
            bag_acc.add_template(
                bag_template,
                center,
                (0.82, 0.50, 0.38),
                (1, 0, 0),
                (0, -1, 0),
                rng,
                jitter=0.012,
            )
            bag_acc.add_template(
                tie_template,
                center + Vector((0.0, 0.0, 0.19)),
                (0.24, 0.24, 0.10),
                (1, 0, 0),
                (0, -1, 0),
                rng,
            )
            for _ in range(4):
                pebble = center + Vector(
                    (rng.uniform(-0.17, 0.17), rng.uniform(-0.07, 0.07), 0.25)
                )
                size = rng.uniform(0.10, 0.17)
                stone_acc.add_template(
                    ico,
                    pebble,
                    (size, size * 0.8, size * 0.75),
                    (1, 0, 0),
                    (0, -1, 0),
                    rng,
                )
    mortar_acc.add_template(
        plain,
        Vector((-72.9, south_y - 0.018, 0.73)),
        (5.4, 0.035, 1.45),
        (1, 0, 0),
        (0, -1, 0),
        rng,
    )
    print("SHICRAS 10")


def main():
    args = parse_args()
    if not bpy.data.filepath.endswith("caral_remaster_v2.blend"):
        raise RuntimeError("Abrir blender/caral/caral_remaster_v2.blend antes de ejecutar")
    if bpy.data.collections.get(HIGH_ROOT) is not None:
        raise RuntimeError("COL-Caral_HighPoly ya existe; no se duplicará el prototipo")

    rng = random.Random(SEED)
    depsgraph = bpy.context.evaluated_depsgraph_get()
    export_objects = [
        obj
        for obj in bpy.data.objects
        if obj.type == "MESH" and not any(c.name in EXCLUDED for c in obj.users_collection)
    ]
    originals = [obj for obj in export_objects if obj.name.startswith(PREFIX)]
    before_total = sum(evaluated_tris(obj, depsgraph) for obj in export_objects)
    before_mayor = sum(evaluated_tris(obj, depsgraph) for obj in originals)
    print(f"BEFORE total={before_total} mayor={before_mayor} mayor_objects={len(originals)}")

    parent = bpy.data.collections.get("COL-Caral") or bpy.context.scene.collection
    high_root = ensure_collection(HIGH_ROOT, parent)
    high_mayor = ensure_collection(HIGH_MAYOR, high_root)
    low_root = ensure_collection(LOW_ROOT, parent)
    low_mayor = ensure_collection(LOW_MAYOR, low_root)
    high_root["lod"] = 0
    high_root["stage"] = "v2-fase-a-prototipo"
    low_root["lod"] = 1

    for obj in originals:
        move_to_collection(obj, low_mayor)
        obj["lod"] = 1
        obj["layer"] = "city"
        obj["sublayer"] = "mayor"

    for obj in originals:
        if "Stair_" in obj.name or "CornerStone_" in obj.name:
            continue
        duplicate = obj.copy()
        duplicate.data = obj.data.copy()
        duplicate.name = "GEO-Caral_HighPoly_Mayor_" + obj.name[len(PREFIX) + 1 :]
        high_mayor.objects.link(duplicate)
        set_metadata(duplicate, "documentado")

    templates = [bevel_cube_template(SEED + index) for index in range(6)]
    plain = plain_cube_template()
    bag_template = sphere_template()
    tie_template = cylinder_template()
    ico = ico_template()
    field_acc = MeshAccumulator()
    weathered_acc = MeshAccumulator()
    cut_acc = MeshAccumulator()
    mortar_acc = MeshAccumulator()
    bag_acc = MeshAccumulator()
    shicra_stone_acc = MeshAccumulator()

    terraces = [
        bpy.data.objects[f"{PREFIX}_Terrace_{index:02d}"] for index in range(1, 8)
    ]
    stairs = [obj for obj in originals if "Stair_" in obj.name]
    generate_wall_stones(terraces, field_acc, weathered_acc, mortar_acc, templates, plain, rng, args.field_stones)
    generate_quoins(terraces, cut_acc, templates, rng)
    generate_stairs(stairs, cut_acc, templates, plain, rng)
    generate_shicras(terraces[0], bag_acc, shicra_stone_acc, mortar_acc, bag_template, tie_template, ico, plain, rng)

    field_acc.create_object(
        "GEO-Caral_HighPoly_Mayor_Stone_Field",
        bpy.data.materials["MAT-Caral_Remaster_Stone_Field"],
        high_mayor,
    )
    weathered_acc.create_object(
        "GEO-Caral_HighPoly_Mayor_Stone_Weathered",
        bpy.data.materials["MAT-Caral_Remaster_Rock"],
        high_mayor,
        evidence="interpretativo",
    )
    cut_acc.create_object(
        "GEO-Caral_HighPoly_Mayor_Stone_Cut",
        bpy.data.materials["MAT-Caral_Remaster_Stone_Cut"],
        high_mayor,
    )
    mortar_acc.create_object(
        "GEO-Caral_HighPoly_Mayor_Mortar",
        make_mortar_material(),
        high_mayor,
        evidence="interpretativo",
    )
    bag_acc.create_object(
        "GEO-Caral_HighPoly_Mayor_Shicras",
        bpy.data.materials["MAT-Caral_Shicra"],
        high_mayor,
        smooth=True,
        evidence="inferido",
    )
    shicra_stone_acc.create_object(
        "GEO-Caral_HighPoly_Mayor_ShicraStones",
        bpy.data.materials["MAT-Caral_Remaster_Stone_Field"],
        high_mayor,
        evidence="inferido",
    )

    low_root.hide_render = True
    low_root.hide_viewport = True
    high_root.hide_render = False
    high_root.hide_viewport = False
    bpy.context.view_layer.update()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    high_objects = [obj for obj in high_mayor.objects if obj.type == "MESH"]
    after_mayor = sum(evaluated_tris(obj, depsgraph) for obj in high_objects)
    other_objects = [obj for obj in export_objects if obj not in originals]
    after_total = after_mayor + sum(evaluated_tris(obj, depsgraph) for obj in other_objects)
    metrics = {
        "before_total_tris": before_total,
        "before_mayor_tris": before_mayor,
        "before_mayor_objects": len(originals),
        "highpoly_mayor_tris": after_mayor,
        "highpoly_mayor_objects": len(high_objects),
        "projected_lod0_total_tris": after_total,
        "field_stone_budget": args.field_stones,
        "seed": SEED,
    }
    print("V2_METRICS " + json.dumps(metrics, sort_keys=True))
    if after_mayor > 135000:
        raise RuntimeError(f"Presupuesto excedido: {after_mayor} tris > 135000")
    if not args.no_save:
        bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
        print(f"SAVED {bpy.data.filepath}")


if __name__ == "__main__":
    main()
