"""Audita una escena Blender sin modificarla.

Uso:
    blender --background blender/caral/caral_art.blend \
      --python scripts/audit_blender_scene.py -- \
      --out docs/remaster/caral/auditoria.json
"""

import argparse
import json
import os
import sys
from collections import Counter, defaultdict

import bpy
from mathutils import Vector


def parse_args():
    argv = sys.argv
    argv = argv[argv.index("--") + 1 :] if "--" in argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="docs/remaster/caral/auditoria.json")
    return parser.parse_args(argv)


def tri_count(obj):
    if obj.type != "MESH":
        return 0
    mesh = obj.data
    mesh.calc_loop_triangles()
    return len(mesh.loop_triangles)


def world_bounds(objects):
    points = []
    for obj in objects:
        if obj.type != "MESH":
            continue
        for corner in obj.bound_box:
            points.append(obj.matrix_world @ Vector(corner))
    if not points:
        return None
    mins = [min(p[i] for p in points) for i in range(3)]
    maxs = [max(p[i] for p in points) for i in range(3)]
    return {
        "min": [round(v, 3) for v in mins],
        "max": [round(v, 3) for v in maxs],
        "size": [round(maxs[i] - mins[i], 3) for i in range(3)],
    }


def main():
    args = parse_args()
    out = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)

    objects = list(bpy.data.objects)
    meshes = [o for o in objects if o.type == "MESH"]
    materials = list(bpy.data.materials)
    images = [i for i in bpy.data.images if i.source == "FILE"]

    type_counts = Counter(o.type for o in objects)
    modifier_counts = Counter()
    uv_missing = []
    material_usage = Counter()
    object_rows = []
    for obj in meshes:
        for modifier in obj.modifiers:
            modifier_counts[modifier.type] += 1
        if not obj.data.uv_layers:
            uv_missing.append(obj.name)
        for slot in obj.material_slots:
            if slot.material:
                material_usage[slot.material.name] += 1
        object_rows.append(
            {
                "name": obj.name,
                "collections": [c.name for c in obj.users_collection],
                "tris": tri_count(obj),
                "modifiers": [m.type for m in obj.modifiers],
                "uv_layers": len(obj.data.uv_layers),
                "materials": [s.material.name for s in obj.material_slots if s.material],
                "dimensions": [round(v, 3) for v in obj.dimensions],
            }
        )

    collections = []
    for collection in bpy.data.collections:
        collections.append(
            {
                "name": collection.name,
                "objects": len(collection.objects),
                "children": len(collection.children),
                "bounds": world_bounds(list(collection.objects)),
            }
        )

    image_rows = []
    for image in images:
        image_rows.append(
            {
                "name": image.name,
                "filepath": image.filepath,
                "packed": bool(image.packed_file),
                "size": list(image.size),
                "missing": not os.path.exists(bpy.path.abspath(image.filepath)),
            }
        )

    data = {
        "blender": bpy.app.version_string,
        "file": os.path.relpath(bpy.data.filepath, os.getcwd()) if bpy.data.filepath else None,
        "units": {
            "system": bpy.context.scene.unit_settings.system,
            "scale_length": bpy.context.scene.unit_settings.scale_length,
        },
        "render": {
            "engine": bpy.context.scene.render.engine,
            "resolution": [
                bpy.context.scene.render.resolution_x,
                bpy.context.scene.render.resolution_y,
            ],
            "color_management": bpy.context.scene.view_settings.view_transform,
        },
        "counts": {
            "objects": len(objects),
            "meshes": len(meshes),
            "materials": len(materials),
            "images": len(images),
            "tris": sum(tri_count(o) for o in meshes),
            "types": dict(type_counts),
            "modifiers": dict(modifier_counts),
        },
        "collections": collections,
        "materials": [
            {
                "name": material.name,
                "users": material.users,
                "objects": material_usage.get(material.name, 0),
                "nodes": [node.type for node in material.node_tree.nodes]
                if material.use_nodes and material.node_tree
                else [],
            }
            for material in materials
        ],
        "images": image_rows,
        "uv_missing": uv_missing,
        "objects": sorted(object_rows, key=lambda row: row["tris"], reverse=True),
        "lights": [
            {
                "name": light.name,
                "type": light.data.type,
                "energy": light.data.energy,
                "location": [round(v, 3) for v in light.location],
            }
            for light in objects
            if light.type == "LIGHT"
        ],
        "cameras": [
            {
                "name": camera.name,
                "lens": camera.data.lens,
                "location": [round(v, 3) for v in camera.location],
                "rotation": [round(v, 3) for v in camera.rotation_euler],
            }
            for camera in objects
            if camera.type == "CAMERA"
        ],
    }

    with open(out, "w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)

    print(f"AUDIT_OK {out}")
    print(
        f"OBJECTS {data['counts']['objects']} MESHES {data['counts']['meshes']} "
        f"TRIS {data['counts']['tris']} MATERIALS {data['counts']['materials']} "
        f"IMAGES {data['counts']['images']} UV_MISSING {len(uv_missing)}"
    )


if __name__ == "__main__":
    main()
