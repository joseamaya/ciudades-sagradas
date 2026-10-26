"""Renders de validación de la Fase B de Caral v2.

Uso:
    blender --background blender/caral/caral_remaster_v2.blend \
      --python scripts/render_caral_v2_phase_b.py -- \
      --out-dir docs/remaster/caral
"""

import argparse
import os
import sys

import bpy
from mathutils import Vector


REGIONS = {
    "plaza": "COL-Caral_HighPoly_PlazaMayor",
    "anfiteatro": "COL-Caral_HighPoly_Anfiteatro",
    "altar": "COL-Caral_HighPoly_AltarCircular",
}
LOW_REGIONS = {
    "plaza": "COL-Caral_LowPoly_PlazaMayor",
    "anfiteatro": "COL-Caral_LowPoly_Anfiteatro",
    "altar": "COL-Caral_LowPoly_AltarCircular",
}
LOW_ROOT = "COL-Caral_LowPoly"
LOW_MAYOR = "COL-Caral_LowPoly_Mayor"
HIGH_ROOT = "COL-Caral_HighPoly"


def parse_args():
    argv = sys.argv
    argv = argv[argv.index("--") + 1 :] if "--" in argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True)
    return parser.parse_args(argv)


def set_collection_visibility(name, visible):
    collection = bpy.data.collections.get(name)
    if collection is None:
        raise RuntimeError(f"Falta la colección {name}")
    collection.hide_render = not visible
    collection.hide_viewport = not visible


def show_before(target):
    set_collection_visibility(HIGH_ROOT, True)
    set_collection_visibility(LOW_ROOT, True)
    set_collection_visibility(LOW_MAYOR, False)
    for key, collection_name in REGIONS.items():
        set_collection_visibility(collection_name, key != target)
    for key, collection_name in LOW_REGIONS.items():
        set_collection_visibility(collection_name, key == target)


def show_after():
    set_collection_visibility(LOW_ROOT, False)
    set_collection_visibility(HIGH_ROOT, True)
    for collection_name in REGIONS.values():
        set_collection_visibility(collection_name, True)


def set_camera(name):
    camera = bpy.data.objects.get(name)
    if camera is None:
        raise RuntimeError(f"Falta la cámara {name}")
    bpy.context.scene.camera = camera
    return camera


def render(path):
    scene = bpy.context.scene
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print(f"RENDERED {path}")


def main():
    args = parse_args()
    out_dir = os.path.abspath(args.out_dir)
    os.makedirs(out_dir, exist_ok=True)
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 1600
    scene.render.resolution_y = 900
    scene.render.resolution_percentage = 100
    scene.eevee.taa_render_samples = 64
    scene.render.image_settings.file_format = "JPEG"
    scene.render.image_settings.quality = 91
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.render.film_transparent = False

    jobs = [
        ("plaza", "CAM-Caral_V2_Plaza", "v2-before-plaza.jpg", "v2-after-plaza.jpg"),
        ("anfiteatro", "CAM-Caral_V2_Anfiteatro", "v2-before-anfiteatro.jpg", "v2-after-anfiteatro.jpg"),
        ("altar", "CAM-Caral_V2_Altar", "v2-before-altar.jpg", "v2-after-altar.jpg"),
    ]
    for target, camera_name, before_name, after_name in jobs:
        set_camera(camera_name)
        show_before(target)
        render(os.path.join(out_dir, before_name))
        show_after()
        render(os.path.join(out_dir, after_name))

    show_after()
    set_camera("CAM-Caral_V2_PlazaDetail")
    render(os.path.join(out_dir, "v2-after-plaza-detail.jpg"))
    set_camera("CAM-Caral_V2_AltarDetail")
    render(os.path.join(out_dir, "v2-after-altar-detail.jpg"))

    scene.camera = bpy.data.objects["CAM-Caral_V2_Mayor"]
    set_collection_visibility(LOW_ROOT, False)
    print("PHASE_B_RENDERS_OK")


if __name__ == "__main__":
    main()
