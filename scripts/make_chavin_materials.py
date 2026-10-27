"""Genera texturas procedurales de mampostería para Chavín.

Uso:
    python3 scripts/make_chavin_materials.py

Salida:
    blender/textures/chavin/chavin_ashlar_diffuse.jpg
    blender/textures/chavin/chavin_ashlar_roughness.jpg
    blender/textures/chavin/chavin_ashlar_normal.png
"""

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import gaussian_filter

SIZE = 2048
OUT = Path("blender/textures/chavin")
OUT.mkdir(parents=True, exist_ok=True)


def grain(size, seed=2, blur=0.7):
    rng = np.random.default_rng(seed)
    data = rng.normal(0.5, 0.12, (size, size)).astype(np.float32)
    data = gaussian_filter(data, sigma=max(0.1, blur), mode="wrap")
    return np.clip(data, 0, 1)


def normal_from_height(height, strength=1.1):
    dx = (np.roll(height, -1, axis=1) - np.roll(height, 1, axis=1)) * 0.5
    dy = (np.roll(height, -1, axis=0) - np.roll(height, 1, axis=0)) * 0.5
    nx = -dx * strength
    ny = dy * strength
    nz = np.ones_like(height)
    length = np.sqrt(nx * nx + ny * ny + nz * nz)
    normal = np.dstack((nx / length, ny / length, nz / length))
    return ((normal * 0.5 + 0.5) * 255).clip(0, 255).astype(np.uint8)


def ashlar(size, seed):
    rng = np.random.default_rng(seed)
    height_img = Image.new("L", (size, size), 100)
    color_img = Image.new("RGB", (size, size), (108, 104, 96))
    draw_h = ImageDraw.Draw(height_img)
    draw_c = ImageDraw.Draw(color_img)

    courses = 7
    course_h = size // courses
    mortar = max(10, size // 220)

    for row in range(courses):
        y0 = row * course_h
        offset = int(rng.integers(0, size // 3))
        x = -offset
        while x < size:
            width = int(rng.integers(size // 7, size // 3))
            base = int(rng.integers(112, 156))
            tone = (base + 4, base, base - 7)
            for shift in (-size, 0, size):
                x0 = x + shift + mortar
                x1 = x + shift + width - mortar
                y1 = y0 + course_h - mortar
                if x1 < 0 or x0 > size:
                    continue
                draw_h.rectangle([x0, y0 + mortar, x1, y1], fill=base)
                draw_c.rectangle([x0, y0 + mortar, x1, y1], fill=tone)
                draw_h.line([x0, y0 + mortar, x1, y0 + mortar], fill=min(255, base + 14), width=3)
            x += width

    height = np.asarray(height_img, dtype=np.float32) / 255.0
    height = 0.78 * height + 0.22 * grain(size, seed + 2, 0.8)
    color = np.asarray(color_img, dtype=np.float32)
    color = np.clip(color * (0.93 + 0.12 * grain(size, seed + 3, 1.1))[:, :, None], 0, 255)
    roughness = 0.82 + 0.10 * (grain(size, seed + 4, 1.0) - 0.5) + 0.06 * (1 - height)
    return color, height, roughness


def save_rgb(array, name):
    Image.fromarray(array.astype(np.uint8), "RGB").save(OUT / name, quality=92, optimize=True)


def save_gray(array, name):
    Image.fromarray((np.clip(array, 0, 1) * 255).astype(np.uint8), "L").save(OUT / name)


color, height, roughness = ashlar(SIZE, 151)
save_rgb(color, "chavin_ashlar_diffuse.jpg")
save_gray(roughness, "chavin_ashlar_roughness.jpg")
Image.fromarray(normal_from_height(height, 1.2)).save(OUT / "chavin_ashlar_normal.png")

print("WROTE", OUT)
