"""Genera la familia ashlar v0.2 de Chavín.

Uso:
    python3 scripts/make_chavin_materials_v2.py

Salida:
    blender/textures/chavin/chavin_ashlar_v2_diffuse.jpg
    blender/textures/chavin/chavin_ashlar_v2_diffuse_dark.jpg
    blender/textures/chavin/chavin_ashlar_v2_roughness.jpg
    blender/textures/chavin/chavin_ashlar_v2_normal.png
"""

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import gaussian_filter

SIZE = 2048
OUT = Path("blender/textures/chavin")
OUT.mkdir(parents=True, exist_ok=True)


def grain(size, seed, blur):
    rng = np.random.default_rng(seed)
    data = rng.normal(0.5, 0.12, (size, size)).astype(np.float32)
    data = gaussian_filter(data, sigma=max(0.1, blur), mode="wrap")
    return np.clip(data, 0, 1)


def mottle(size, seed):
    rng = np.random.default_rng(seed)
    data = rng.normal(0.0, 1.0, (size, size)).astype(np.float32)
    data = gaussian_filter(data, sigma=size // 22, mode="wrap")
    lo = float(data.min())
    hi = float(data.max())
    return (data - lo) / max(1e-6, hi - lo)


def normal_from_height(height, strength):
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
    base_h = size / courses
    edges = [0]
    for i in range(courses - 1):
        jitter = int(rng.integers(-size // 90, size // 90 + 1))
        edges.append(int((i + 1) * base_h + jitter))
    edges.append(size)
    for i in range(1, len(edges)):
        if edges[i] <= edges[i - 1]:
            edges[i] = edges[i - 1] + 1

    mortar = max(8, size // 240)
    for row in range(courses):
        y0 = edges[row]
        y1 = edges[row + 1]
        if y1 - y0 <= 2 * mortar:
            continue
        offset = int(rng.integers(0, size))
        x = -offset
        while x < size:
            width = int(rng.integers(size // 9, size // 3))
            base = int(rng.integers(102, 150))
            warm = int(rng.integers(-4, 9))
            tone = (
                min(255, base + 18 + warm),
                min(255, base + 4),
                max(0, base - 26 + warm // 2),
            )
            for shift in (-size, 0, size):
                x0 = x + shift + mortar
                x1 = x + shift + width - mortar
                yy0 = y0 + mortar
                yy1 = y1 - mortar
                if x1 < 0 or x0 > size or yy1 <= yy0:
                    continue
                draw_h.rectangle([x0, yy0, x1, yy1], fill=base)
                draw_c.rectangle([x0, yy0, x1, yy1], fill=tone)
                draw_h.line([x0, yy0, x1, yy0], fill=min(255, base + 16), width=3)
                if rng.random() < 0.35:
                    chip_x = int(rng.integers(x0, max(x0 + 1, x1)))
                    chip_y = yy0 if rng.random() < 0.5 else yy1 - 3
                    draw_h.rectangle([chip_x, chip_y, chip_x + 4, chip_y + 3], fill=max(0, base - 28))
                    draw_c.rectangle([chip_x, chip_y, chip_x + 4, chip_y + 3], fill=(70, 66, 58))
            x += width

    height = np.asarray(height_img, dtype=np.float32) / 255.0
    height = 0.78 * height + 0.22 * grain(size, seed + 2, 0.8)
    color = np.asarray(color_img, dtype=np.float32)
    large = mottle(size, seed + 5)
    color = color * (0.86 + 0.22 * large[:, :, None])
    color = np.clip(color * (0.93 + 0.14 * grain(size, seed + 3, 1.1))[:, :, None], 0, 255)
    roughness = 0.80 + 0.11 * (grain(size, seed + 4, 1.0) - 0.5) + 0.07 * (1 - height)
    return color, height, roughness


def save_rgb(array, name):
    Image.fromarray(np.clip(array, 0, 255).astype(np.uint8), "RGB").save(
        OUT / name, quality=92, optimize=True
    )


def save_gray(array, name):
    Image.fromarray((np.clip(array, 0, 1) * 255).astype(np.uint8), "L").save(OUT / name)


color, height, roughness = ashlar(SIZE, 271)
save_rgb(color, "chavin_ashlar_v2_diffuse.jpg")
save_rgb(color * 0.58, "chavin_ashlar_v2_diffuse_dark.jpg")
save_gray(roughness, "chavin_ashlar_v2_roughness.jpg")
Image.fromarray(normal_from_height(height, 2.2)).save(OUT / "chavin_ashlar_v2_normal.png")

for name in ("diffuse", "diffuse_dark", "roughness", "normal"):
    img = np.asarray(Image.open(OUT / ("chavin_ashlar_v2_" + name + (".jpg" if name != "normal" else ".png"))).convert("RGB")).astype(np.float32)
    lr = float(np.abs(img[:, 0] - img[:, -1]).mean())
    tb = float(np.abs(img[0, :] - img[-1, :]).mean())
    print("EDGE", name, round(lr, 2), round(tb, 2))

print("WROTE", OUT)
