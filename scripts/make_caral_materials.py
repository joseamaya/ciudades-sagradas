"""Genera texturas procedurales para el remaster de Caral.

Uso:
    python3 scripts/make_caral_materials.py

Salida:
    blender/textures/generated/remaster/
"""

from pathlib import Path
import math
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy.spatial import cKDTree
from scipy.ndimage import gaussian_filter

SIZE = 2048
SMALL = 1024
OUT = Path("blender/textures/generated/remaster")
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(1269)
random.seed(1269)


def periodic_noise(size, octaves=4, seed=1):
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:size, 0:size] / size
    result = np.zeros((size, size), dtype=np.float32)
    for octave in range(octaves):
        frequency = 2 ** (octave + 1)
        amplitude = 1.0 / (octave + 1)
        for _ in range(3):
            angle = rng.uniform(0, math.pi)
            fx = max(1, int(round(math.cos(angle) * frequency)))
            fy = max(1, int(round(math.sin(angle) * frequency)))
            phase = rng.uniform(0, math.tau)
            result += amplitude * np.sin(math.tau * (fx * x + fy * y) + phase)
    result -= result.min()
    result /= max(result.max(), 1e-6)
    return result


def isotropic(size, seed, sigma):
    rng = np.random.default_rng(seed)
    noise = rng.normal(0.0, 1.0, (size, size)).astype(np.float32)
    noise = gaussian_filter(noise, sigma=max(1.0, sigma), mode="wrap")
    noise -= noise.min()
    noise /= max(noise.max(), 1e-6)
    return noise


def grain(size, seed=2, blur=0.7):
    rng = np.random.default_rng(seed)
    data = rng.normal(0.5, 0.12, (size, size)).astype(np.float32)
    data = gaussian_filter(data, sigma=max(0.1, blur), mode="wrap")
    return np.clip(data, 0, 1)


def normal_from_height(height, strength=1.0):
    dx = (np.roll(height, -1, axis=1) - np.roll(height, 1, axis=1)) * 0.5
    dy = (np.roll(height, -1, axis=0) - np.roll(height, 1, axis=0)) * 0.5
    nx = -dx * strength
    ny = dy * strength
    nz = np.ones_like(height)
    length = np.sqrt(nx * nx + ny * ny + nz * nz)
    normal = np.dstack((nx / length, ny / length, nz / length))
    return ((normal * 0.5 + 0.5) * 255).clip(0, 255).astype(np.uint8)


def crack_mask(size, seed, count=26):
    rng = np.random.default_rng(seed)
    image = Image.new("L", (size, size), 255)
    draw = ImageDraw.Draw(image)
    for _ in range(count):
        x = int(rng.integers(0, size))
        y = int(rng.integers(0, size))
        points = [(x, y)]
        for _ in range(int(rng.integers(2, 5))):
            x += int(rng.integers(-size // 12, size // 12))
            y += int(rng.integers(-size // 18, size // 18))
            points.append((x, y))
        for ox in (-size, 0, size):
            for oy in (-size, 0, size):
                draw.line([(px + ox, py + oy) for px, py in points], fill=0, width=max(2, size // 700))
    image = image.filter(ImageFilter.GaussianBlur(0.6))
    return 1.0 - np.asarray(image, dtype=np.float32) / 255.0


def save_rgb(array, name, size):
    image = Image.fromarray(array.astype(np.uint8), "RGB")
    if image.size != (size, size):
        image = image.resize((size, size), Image.Resampling.LANCZOS)
    image.save(OUT / name, quality=92, optimize=True)
    print("WROTE", OUT / name)


def save_gray(array, name, size):
    image = Image.fromarray((np.clip(array, 0, 1) * 255).astype(np.uint8), "L")
    if image.size != (size, size):
        image = image.resize((size, size), Image.Resampling.LANCZOS)
    image.save(OUT / name)
    print("WROTE", OUT / name)


def plaster(size, base, seed, crack_strength=0.38, crack_count=26, variation=1.0):
    low = isotropic(size, seed, size / 24)
    mid = isotropic(size, seed + 1, size / 96)
    fine = grain(size, seed + 2, 0.6)
    height = 0.52 + variation * (0.06 * (low - 0.5) + 0.05 * (mid - 0.5)) + 0.04 * (fine - 0.5)
    tint = 0.95 + variation * (0.06 * (low - 0.5) + 0.03 * (mid - 0.5)) + 0.04 * (fine - 0.5)
    color = np.zeros((size, size, 3), dtype=np.float32)
    for i in range(3):
        color[:, :, i] = np.clip(base[i] * tint, 0, 255)
    cracks = crack_mask(size, seed + 10, count=crack_count)
    height -= 0.03 * cracks
    color *= (1.0 - crack_strength * cracks)[:, :, None]
    roughness = 0.80 + variation * (0.03 * (low - 0.5) + 0.03 * (mid - 0.5)) + 0.06 * (fine - 0.5) + 0.08 * cracks
    return color, height, roughness


def stone_cut(size, seed):
    rng = np.random.default_rng(seed)
    height_img = Image.new("L", (size, size), 110)
    color_img = Image.new("RGB", (size, size), (120, 112, 100))
    draw_h = ImageDraw.Draw(height_img)
    draw_c = ImageDraw.Draw(color_img)
    courses = 8
    course_h = size // courses
    mortar = max(8, size // 180)
    for row in range(courses):
        y0 = row * course_h
        offset = int(rng.integers(0, size // 2))
        x = -offset
        while x < size:
            width = int(rng.integers(size // 8, size // 4))
            base = int(rng.integers(150, 190))
            tone = np.array([base + 8, base + 2, base - 8])
            for shift in (-size, 0, size):
                x0 = x + shift + mortar
                x1 = x + shift + width - mortar
                y1 = y0 + course_h - mortar
                if x1 < 0 or x0 > size:
                    continue
                draw_h.rectangle([x0, y0 + mortar, x1, y1], fill=base)
                draw_c.rectangle([x0, y0 + mortar, x1, y1], fill=tuple(int(v) for v in tone))
                draw_h.line([x0, y0 + mortar, x1, y0 + mortar], fill=min(255, base + 18), width=3)
                draw_c.line([x0, y0 + mortar, x1, y0 + mortar], fill=(min(255, tone[0] + 12), min(255, tone[1] + 12), min(255, tone[2] + 12)), width=3)
            x += width
    height = np.asarray(height_img, dtype=np.float32) / 255.0
    height = 0.75 * height + 0.25 * grain(size, seed + 2, 0.8)
    color = np.asarray(color_img, dtype=np.float32)
    color = np.clip(color * (0.92 + 0.16 * grain(size, seed + 3, 1.2))[:, :, None], 0, 255)
    roughness = 0.78 + 0.12 * (grain(size, seed + 4, 1.0) - 0.5) + 0.08 * (1 - height)
    return color, height, roughness


def stone_field(size, seed):
    rng = np.random.default_rng(seed)
    small = 1024
    seeds = rng.uniform(0, small, (150, 2))
    tree = cKDTree(np.vstack([seeds, seeds + [small, 0], seeds + [0, small], seeds + [small, small], seeds - [small, 0], seeds - [0, small]]))
    yy, xx = np.mgrid[0:small, 0:small]
    points = np.column_stack([xx.ravel(), yy.ravel()])
    distances, indices = tree.query(points, k=2, workers=-1)
    d1 = distances[:, 0].reshape(small, small)
    d2 = distances[:, 1].reshape(small, small)
    cell = (indices[:, 0] % len(seeds)).reshape(small, small)
    edge = np.clip((d2 - d1) / 7.0, 0, 1)
    height = 0.78 - 0.28 * (1 - edge)
    height += 0.04 * (grain(small, seed + 5, 0.5) - 0.5)
    base = rng.integers(130, 180, (len(seeds), 1))
    palette = np.column_stack([base[:, 0] + 8, base[:, 0] + 2, base[:, 0] - 10]).clip(0, 255)
    color = palette[cell].astype(np.float32)
    color *= (0.9 + 0.2 * grain(small, seed + 6, 1.0))[:, :, None]
    color = np.clip(color, 0, 255)
    roughness = 0.8 + 0.1 * (grain(small, seed + 7, 1.0) - 0.5) + 0.06 * (1 - height)
    # Upscale a 2K para el mapa final
    height = np.asarray(Image.fromarray((height * 255).astype(np.uint8)).resize((size, size), Image.Resampling.BICUBIC), dtype=np.float32) / 255.0
    color = np.asarray(Image.fromarray(color.astype(np.uint8)).resize((size, size), Image.Resampling.LANCZOS), dtype=np.float32)
    roughness = np.asarray(Image.fromarray((roughness * 255).astype(np.uint8)).resize((size, size), Image.Resampling.BICUBIC), dtype=np.float32) / 255.0
    return color, height, roughness



def ground(size, base, seed, grain_amount=0.06):
    fine = grain(size, seed, 0.8)
    color = np.zeros((size, size, 3), dtype=np.float32)
    for i in range(3):
        color[:, :, i] = np.clip(base[i] * (1.0 + grain_amount * (fine - 0.5)), 0, 255)
    height = 0.5 + 0.02 * (fine - 0.5)
    roughness = 0.90 + 0.04 * (fine - 0.5)
    return color, height, roughness


def terrain_sand(size, base, seed):
    macro = isotropic(size, seed, size / 8)
    mid = isotropic(size, seed + 1, size / 32)
    fine = grain(size, seed + 2, 0.8)
    color = np.zeros((size, size, 3), dtype=np.float32)
    for i in range(3):
        color[:, :, i] = np.clip(
            base[i] * (0.92 + 0.10 * (macro - 0.5) + 0.05 * (mid - 0.5) + 0.03 * (fine - 0.5)),
            0, 255,
        )
    height = 0.5 + 0.015 * (mid - 0.5) + 0.02 * (fine - 0.5)
    roughness = 0.92 + 0.03 * (fine - 0.5)
    return color, height, roughness



def rock_face(size, base, seed):
    rng = np.random.default_rng(seed)
    small = 1024
    count = 110
    seeds = rng.uniform(0, small, (count, 2))
    tree = cKDTree(np.vstack([
        seeds,
        seeds + [small, 0], seeds + [0, small], seeds + [small, small],
        seeds - [small, 0], seeds - [0, small],
    ]))
    yy, xx = np.mgrid[0:small, 0:small]
    points = np.column_stack([xx.ravel(), yy.ravel()])
    distances, indices = tree.query(points, k=2, workers=-1)
    d1 = distances[:, 0].reshape(small, small)
    d2 = distances[:, 1].reshape(small, small)
    cell = (indices[:, 0] % count).reshape(small, small)
    edge = np.clip((d2 - d1) / 6.0, 0, 1)

    tones = rng.integers(100, 146, (count, 1))
    palette = np.column_stack([tones + 8, tones + 2, tones - 10]).clip(0, 255)
    color = palette[cell].astype(np.float32)
    color *= (0.9 + 0.2 * grain(small, seed + 3, 1.0))[:, :, None]
    color *= (0.85 + 0.15 * edge)[:, :, None]
    color *= np.array(base, dtype=np.float32) / np.array([120, 112, 102], dtype=np.float32)
    color = np.clip(color, 0, 255)

    height = 0.78 - 0.32 * (1 - edge) + 0.05 * (grain(small, seed + 5, 0.6) - 0.5)
    roughness = 0.82 + 0.06 * (1 - edge) + 0.04 * (grain(small, seed + 6, 1.0) - 0.5)

    height = np.asarray(Image.fromarray((height * 255).astype(np.uint8)).resize((size, size), Image.Resampling.BICUBIC), dtype=np.float32) / 255.0
    color = np.asarray(Image.fromarray(color.astype(np.uint8)).resize((size, size), Image.Resampling.LANCZOS), dtype=np.float32)
    roughness = np.asarray(Image.fromarray((roughness * 255).astype(np.uint8)).resize((size, size), Image.Resampling.BICUBIC), dtype=np.float32) / 255.0
    return color, height, roughness


def dry_grass(size, base, seed):
    rng = np.random.default_rng(seed)
    image = Image.new("RGB", (size, size), tuple(int(v) for v in base))
    height = Image.new("L", (size, size), 128)
    draw = ImageDraw.Draw(image)
    draw_h = ImageDraw.Draw(height)
    for _ in range(size * 2):
        x = int(rng.integers(0, size)); y = int(rng.integers(0, size))
        length = int(rng.integers(4, 22)); angle = rng.uniform(-0.5, 0.5)
        x2 = int(x + math.cos(angle) * length); y2 = int(y + math.sin(angle) * length)
        tone = tuple(int(np.clip(c + rng.normal(0, 20), 0, 255)) for c in base)
        h = int(np.clip(128 + rng.normal(0, 28), 0, 255))
        for ox, oy in ((-size, 0), (0, 0), (size, 0), (0, -size), (0, size)):
            draw.line([(x + ox, y + oy), (x2 + ox, y2 + oy)], fill=tone, width=1)
            draw_h.line([(x + ox, y + oy), (x2 + ox, y2 + oy)], fill=h, width=1)
    image = image.filter(ImageFilter.GaussianBlur(0.35))
    height = height.filter(ImageFilter.GaussianBlur(0.35))
    color = np.asarray(image, dtype=np.float32)
    low = isotropic(size, seed + 3, size / 16)
    color *= (0.9 + 0.2 * (low - 0.5))[:, :, None]
    color = np.clip(color, 0, 255)
    h = np.asarray(height, dtype=np.float32) / 255.0
    h = 0.5 + 0.12 * (h - 0.5) + 0.03 * (low - 0.5) + 0.02 * (grain(size, seed + 1, 0.7) - 0.5)
    roughness = 0.90 + 0.04 * (grain(size, seed + 2, 1.0) - 0.5)
    return color, h, roughness


def foliage(size, base, seed):
    low = isotropic(size, seed, size / 10)
    mid = isotropic(size, seed + 1, size / 40)
    fine = grain(size, seed + 2, 0.7)
    color = np.zeros((size, size, 3), dtype=np.float32)
    for i in range(3):
        color[:, :, i] = np.clip(base[i] * (0.85 + 0.20 * (low - 0.5) + 0.10 * (mid - 0.5) + 0.05 * (fine - 0.5)), 0, 255)
    height = 0.5 + 0.03 * (low - 0.5) + 0.02 * (fine - 0.5)
    roughness = 0.85 + 0.04 * (fine - 0.5)
    return color, height, roughness


def adobe(size, base, seed):
    low = isotropic(size, seed, size / 20)
    mid = isotropic(size, seed + 1, size / 60)
    fine = grain(size, seed + 2, 0.8)
    color = np.zeros((size, size, 3), dtype=np.float32)
    for i in range(3):
        color[:, :, i] = np.clip(base[i] * (0.92 + 0.08 * (low - 0.5) + 0.05 * (mid - 0.5) + 0.04 * (fine - 0.5)), 0, 255)
    height = 0.5 + 0.03 * (mid - 0.5) + 0.02 * (fine - 0.5)
    roughness = 0.88 + 0.04 * (fine - 0.5)
    return color, height, roughness


def thatch(size, base, seed):
    rng = np.random.default_rng(seed)
    image = Image.new("RGB", (size, size), tuple(int(v) for v in base))
    height = Image.new("L", (size, size), 128)
    draw = ImageDraw.Draw(image)
    draw_h = ImageDraw.Draw(height)
    for _ in range(size):
        x = int(rng.integers(0, size)); y = int(rng.integers(0, size))
        length = int(rng.integers(12, 48)); angle = rng.uniform(-0.15, 0.15)
        x2 = int(x + math.cos(angle) * length); y2 = int(y + math.sin(angle) * length)
        tone = tuple(int(np.clip(c + rng.normal(0, 14), 0, 255)) for c in base)
        h = int(np.clip(128 + rng.normal(0, 24), 0, 255))
        for ox, oy in ((-size, 0), (0, 0), (size, 0), (0, -size), (0, size)):
            draw.line([(x + ox, y + oy), (x2 + ox, y2 + oy)], fill=tone, width=2)
            draw_h.line([(x + ox, y + oy), (x2 + ox, y2 + oy)], fill=h, width=2)
    image = image.filter(ImageFilter.GaussianBlur(0.5))
    height = height.filter(ImageFilter.GaussianBlur(0.5))
    color = np.asarray(image, dtype=np.float32)
    h = np.asarray(height, dtype=np.float32) / 255.0
    h = 0.5 + 0.10 * (h - 0.5) + 0.02 * (grain(size, seed + 1, 0.8) - 0.5)
    roughness = 0.90 + 0.03 * (grain(size, seed + 2, 1.0) - 0.5)
    return color, h, roughness

def main():
    white_color, white_height, white_rough = plaster(SIZE, (216, 206, 186), 11, crack_strength=0.22, crack_count=18)
    save_rgb(white_color, "plaster_white_diffuse.jpg", SIZE)
    save_gray(white_rough, "plaster_white_roughness.jpg", SIZE)
    Image.fromarray(normal_from_height(white_height, 25.0)).save(OUT / "plaster_white_normal.png")

    yellow_color, _, _ = plaster(SMALL, (196, 158, 88), 21, crack_strength=0.10, crack_count=8, variation=0.55)
    save_rgb(yellow_color, "plaster_yellow_diffuse.jpg", SMALL)
    red_color, _, _ = plaster(SMALL, (160, 64, 44), 31, crack_strength=0.14, crack_count=10, variation=0.65)
    save_rgb(red_color, "plaster_red_diffuse.jpg", SMALL)

    cut_color, cut_height, cut_rough = stone_cut(SIZE, 41)
    save_rgb(cut_color, "stone_cut_diffuse.jpg", SIZE)
    save_gray(cut_rough, "stone_cut_roughness.jpg", SIZE)
    Image.fromarray(normal_from_height(cut_height, 1.8)).save(OUT / "stone_cut_normal.png")

    field_color, field_height, field_rough = stone_field(SIZE, 51)
    save_rgb(field_color, "stone_field_diffuse.jpg", SIZE)
    save_gray(field_rough, "stone_field_roughness.jpg", SIZE)
    Image.fromarray(normal_from_height(field_height, 1.5)).save(OUT / "stone_field_normal.png")

    ground_height = None
    ground_rough = None
    for name, base, seed in (
        ("ground_sand_diffuse.jpg", (198, 178, 142), 61),
        ("ground_earth_diffuse.jpg", (150, 128, 98), 62),
        ("ground_rock_diffuse.jpg", (120, 112, 102), 63),
    ):
        color, height, rough = ground(SMALL, base, seed)
        save_rgb(color, name, SMALL)
        if ground_height is None:
            ground_height, ground_rough = height, rough
    save_gray(ground_rough, "ground_roughness.jpg", SMALL)
    Image.fromarray(normal_from_height(ground_height, 0.8)).save(OUT / "ground_normal.png")

    sand_color, _, _ = terrain_sand(SIZE, (205, 184, 148), 71)
    save_rgb(sand_color, "terrain_sand_diffuse.jpg", SIZE)

    rock_color, rock_height, rock_rough = rock_face(SIZE, (124, 114, 101), 81)
    save_rgb(rock_color, "rock_face_diffuse.jpg", SIZE)
    save_gray(rock_rough, "rock_face_roughness.jpg", SIZE)
    Image.fromarray(normal_from_height(rock_height, 3.0)).save(OUT / "rock_face_normal.png")

    grass_color, grass_height, grass_rough = dry_grass(SMALL, (168, 140, 86), 91)
    save_rgb(grass_color, "dry_grass_diffuse.jpg", SMALL)
    save_gray(grass_rough, "dry_grass_roughness.jpg", SMALL)
    Image.fromarray(normal_from_height(grass_height, 1.5)).save(OUT / "dry_grass_normal.png")

    leaf_color, leaf_height, leaf_rough = foliage(SMALL, (70, 95, 50), 101)
    save_rgb(leaf_color, "foliage_diffuse.jpg", SMALL)
    save_gray(leaf_rough, "foliage_roughness.jpg", SMALL)
    Image.fromarray(normal_from_height(leaf_height, 1.2)).save(OUT / "foliage_normal.png")

    adobe_color, adobe_height, adobe_rough = adobe(SMALL, (150, 125, 95), 111)
    save_rgb(adobe_color, "adobe_diffuse.jpg", SMALL)
    save_gray(adobe_rough, "adobe_roughness.jpg", SMALL)
    Image.fromarray(normal_from_height(adobe_height, 1.2)).save(OUT / "adobe_normal.png")

    thatch_color, thatch_height, thatch_rough = thatch(SMALL, (160, 130, 80), 121)
    save_rgb(thatch_color, "thatch_diffuse.jpg", SMALL)
    save_gray(thatch_rough, "thatch_roughness.jpg", SMALL)
    Image.fromarray(normal_from_height(thatch_height, 1.5)).save(OUT / "thatch_normal.png")

    print("DONE")


if __name__ == "__main__":
    main()
