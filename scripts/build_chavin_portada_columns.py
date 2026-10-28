"""Sustituye las columnas lisas de la Portada por fustes acanalados.

Uso:
  blender --background blender/chavin/chavin_highpoly_v0.3.blend \
    --python scripts/build_chavin_portada_columns.py -- \
    --out-blend blender/chavin/chavin_highpoly_v0.4.blend

Las columnas conservan radio, altura, material y ubicación de la fuente. Las
acanaladuras son una lectura interpretativa del fuste tallado, no un calco del
escaneo ni de una imagen de referencia.
"""

import argparse
import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

COLUMNS = {
    "GEO-Chavin_Portada_Column_N": "MAT-Chavin_Portada_Dark",
    "GEO-Chavin_Portada_Column_S": "MAT-Chavin_Portada_Light",
}
RADIUS = 0.31
HEIGHT = 2.3
SEGMENTS = 48
FLUTES = 12
GROOVE_DEPTH = 0.024
Z_BOTTOM = -HEIGHT / 2
Z_TOP = HEIGHT / 2
BAND = 0.075
RINGS = (
    (Z_BOTTOM, RADIUS),
    (Z_BOTTOM + BAND, RADIUS),
    (Z_BOTTOM + BAND + 0.03, None),
    (Z_TOP - BAND - 0.03, None),
    (Z_TOP - BAND, RADIUS),
    (Z_TOP, RADIUS),
)


def parse_args():
    argv = sys.argv
    argv = argv[argv.index("--") + 1 :] if "--" in argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-blend", required=True)
    return parser.parse_args(argv)


def radius_at(theta, fixed):
    if fixed is not None:
        return fixed
    return RADIUS - GROOVE_DEPTH * (0.5 + 0.5 * math.cos(FLUTES * theta))


def build_column(name, material, location):
    vertices = []
    uvs = []
    for z, fixed in RINGS:
        for index in range(SEGMENTS + 1):
            theta = 2.0 * math.pi * index / SEGMENTS
            radius = radius_at(theta, fixed)
            vertices.append((radius * math.cos(theta), radius * math.sin(theta), z))
            uvs.append((index / SEGMENTS, (z - Z_BOTTOM) / HEIGHT))

    faces = []
    stride = SEGMENTS + 1
    for ring in range(len(RINGS) - 1):
        for index in range(SEGMENTS):
            a = ring * stride + index
            b = a + 1
            c = a + stride + 1
            d = a + stride
            faces.append((a, b, c, d))
    bottom = tuple(range(SEGMENTS))
    top_start = (len(RINGS) - 1) * stride
    top = tuple(top_start + index for index in range(SEGMENTS))
    faces.append(tuple(reversed(bottom)))
    faces.append(top)

    mesh = bpy.data.meshes.new(f"MESH-{name}")
    mesh.from_pydata(vertices, [], faces)
    mesh.validate()
    mesh.update()

    uv_layer = mesh.uv_layers.new(name="UVMap")
    for loop in mesh.loops:
        uv_layer.data[loop.index].uv = uvs[loop.vertex_index]

    for polygon in mesh.polygons:
        polygon.use_smooth = polygon.loop_total == 4

    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()

    mesh.materials.append(material)
    obj = bpy.data.objects.new(name, mesh)
    obj.location = Vector((location.x, location.y, location.z))
    obj["chavin_highpoly"] = "v0.4"
    obj["source"] = "levantamiento de la Portada; fuste acanalado interpretativo"
    obj["evidence"] = "inferido"
    collection = bpy.data.collections.get("COL-Chavin_Portada")
    if collection is None:
        collection = bpy.context.scene.collection
    collection.objects.link(obj)
    return obj


def main():
    args = parse_args()
    out = os.path.abspath(args.out_blend)
    replacements = []
    for name, material_name in COLUMNS.items():
        old = bpy.data.objects.get(name)
        if old is None:
            raise SystemExit(f"No existe {name}")
        material = bpy.data.materials.get(material_name)
        if material is None:
            raise SystemExit(f"No existe {material_name}")
        replacements.append((name, old, build_column(name, material, old.location)))

    for name, old, new in replacements:
        old.data.calc_loop_triangles()
        new.data.calc_loop_triangles()
        old_tris = len(old.data.loop_triangles)
        bpy.data.objects.remove(old, do_unlink=True)
        new.name = name
        new.data.name = f"MESH-{name}"
        print(
            "CHAVIN_COLUMN_REPLACED "
            f"{new.name} tris={len(new.data.loop_triangles)} old={old_tris}"
        )

    bpy.ops.wm.save_as_mainfile(filepath=out)
    print("CHAVIN_COLUMNS_OK", out)


if __name__ == "__main__":
    main()
