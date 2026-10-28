"""Renderiza vistas de revisión del pase high-poly de Chavín.

Uso:
  blender --background blender/chavin/chavin_highpoly_v0.1.blend \
    --python scripts/render_chavin_highpoly.py -- --out-dir /tmp/chavin_highpoly
"""

import argparse
import os
import sys

import bpy


def parse_args():
    argv = sys.argv
    argv = argv[argv.index("--") + 1 :] if "--" in argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--engine", default="workbench", choices=("workbench", "eevee"))
    return parser.parse_args(argv)


def set_engine(scene, name):
    if name == "workbench":
        scene.render.engine = "BLENDER_WORKBENCH"
        scene.display.shading.light = "STUDIO"
        scene.display.shading.color_type = "MATERIAL"
        scene.display.shading.show_shadows = True
        scene.display.shading.show_cavity = True
        scene.display.shading.cavity_type = "BOTH"
        return
    for candidate in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):
        try:
            scene.render.engine = candidate
            return
        except TypeError:
            continue
    raise RuntimeError("No hay motor EEVEE disponible")


def main():
    args = parse_args()
    os.makedirs(args.out_dir, exist_ok=True)
    scene = bpy.context.scene
    set_engine(scene, args.engine)
    scene.render.resolution_x = 1000
    scene.render.resolution_y = 750
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    if scene.world is not None:
        scene.world.color = (0.035, 0.040, 0.045)
    views = (
        ("CAM-Chavin_HP_Portada", "portada.png"),
        ("CAM-Chavin_HP_Falcon", "falcon.png"),
        ("CAM-Chavin_HP_Lanzon", "lanzon.png"),
        ("CAM-Chavin_HP_LanzonFace", "lanzon-face.png"),
        ("CAM-Chavin_HP_Facade", "facade.png"),
        ("CAM-Chavin_Hero", "hero.png"),
    )
    for name, filename in views:
        camera = bpy.data.objects.get(name)
        if camera is None:
            print("MISSING_CAMERA", name)
            continue
        scene.camera = camera
        scene.render.filepath = os.path.join(args.out_dir, filename)
        bpy.ops.render.render(write_still=True)
        print("RENDERED", scene.render.filepath)


if __name__ == "__main__":
    main()
