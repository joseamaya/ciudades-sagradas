"""Genera la familia de piedra labrada de la Portada de las Falcónidas.

Uso:
    python3 scripts/make_chavin_portal_materials.py

Salida:
    blender/textures/chavin/chavin_portada_v1_light_diffuse.jpg
    blender/textures/chavin/chavin_portada_v1_light_roughness.jpg
    blender/textures/chavin/chavin_portada_v1_light_normal.png
    blender/textures/chavin/chavin_portada_v1_dark_diffuse.jpg
    blender/textures/chavin/chavin_portada_v1_dark_roughness.jpg
    blender/textures/chavin/chavin_portada_v1_dark_normal.png
"""

from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

SIZE = 1024
OUT = Path("blender/textures/chavin")
OUT.mkdir(parents=True, exist_ok=True)


def field(size, seed, sigma):
    rng = np.random.default_rng(seed)
    data = rng.normal(0.0, 1.0, (size, size)).astype(np.float32)
    return gaussian_filter(data, sigma=sigma, mode="wrap")


def normalized(data):
    lo = float(data.min())
    hi = float(data.max())
    return (data - lo) / max(1e-6, hi - lo)


def stone(size, seed, base, contrast, pink):
    broad = normalized(field(size, seed, size / 28))
    medium = normalized(field(size, seed + 3, size / 95))
    fine = field(size, seed + 7, 0.8)
    y, x = np.mgrid[0:size, 0:size].astype(np.float32)
    veins = np.sin((x * 1.7 + y * 0.43) / size * 12.0 + 2.3 * broad)
    veins = np.clip((veins - 0.55) * 1.8, 0.0, 1.0)
    pores = (field(size, seed + 11, 0.55) > 2.0).astype(np.float32)
    pores = gaussian_filter(pores, sigma=0.75, mode="wrap")

    tone = (
        0.54 * broad
        + 0.31 * medium
        + 0.10 * fine
        + 0.05 * veins
    )
    tone = np.clip((tone - 0.5) * contrast + 0.5, 0.0, 1.0)
    warm = np.clip(pink * (veins - 0.25) + 0.35 * (medium - 0.5), -0.25, 0.35)

    color = np.zeros((size, size, 3), dtype=np.float32)
    for i in range(3):
        color[:, :, i] = base[i] * (0.62 + 0.68 * tone)
    color[:, :, 0] *= 1.0 + 0.10 * warm
    color[:, :, 1] *= 1.0 + 0.035 * warm
    color[:, :, 2] *= 1.0 - 0.045 * warm
    color *= 1.0 - 0.16 * pores[:, :, None]
    color[:, :, 0] += 7.0 * veins
    color[:, :, 1] += 4.0 * veins
    color = np.clip(color, 0, 255)

    height = 0.62 * broad + 0.25 * medium + 0.13 * fine
    height -= 0.22 * pores
    height += 0.05 * veins

    roughness = 0.76 + 0.10 * (fine - 0.5) + 0.08 * (1.0 - height)
    roughness = np.clip(roughness, 0.58, 0.94)
    return color, height, roughness


def normal_from_height(height, strength):
    dx = (np.roll(height, -1, axis=1) - np.roll(height, 1, axis=1)) * 0.5
    dy = (np.roll(height, -1, axis=0) - np.roll(height, 1, axis=0)) * 0.5
    nx = -dx * strength
    ny = dy * strength
    nz = np.ones_like(height)
    length = np.sqrt(nx * nx + ny * ny + nz * nz)
    normal = np.dstack((nx / length, ny / length, nz / length))
    return ((normal * 0.5 + 0.5) * 255).clip(0, 255).astype(np.uint8)


def save_rgb(array, name):
    Image.fromarray(np.clip(array, 0, 255).astype(np.uint8), "RGB").save(
        OUT / name, quality=92, optimize=True
    )


def save_gray(array, name):
    Image.fromarray((np.clip(array, 0, 1) * 255).astype(np.uint8), "L").save(
        OUT / name, quality=92, optimize=True
    )


def save_normal(height, name, strength):
    Image.fromarray(normal_from_height(height, strength)).save(OUT / name)


light_color, light_height, light_roughness = stone(
    SIZE,
    seed=401,
    base=(168, 158, 142),
    contrast=1.28,
    pink=1.0,
)
dark_color, dark_height, dark_roughness = stone(
    SIZE,
    seed=409,
    base=(49, 52, 51),
    contrast=1.05,
    pink=0.35,
)

save_rgb(light_color, "chavin_portada_v1_light_diffuse.jpg")
save_gray(light_roughness, "chavin_portada_v1_light_roughness.jpg")
save_normal(light_height, "chavin_portada_v1_light_normal.png", 1.35)
save_rgb(dark_color, "chavin_portada_v1_dark_diffuse.jpg")
save_gray(dark_roughness, "chavin_portada_v1_dark_roughness.jpg")
save_normal(dark_height, "chavin_portada_v1_dark_normal.png", 1.2)

for name in (
    "light_diffuse",
    "light_roughness",
    "light_normal",
    "dark_diffuse",
    "dark_roughness",
    "dark_normal",
):
    suffix = ".png" if name.endswith("normal") else ".jpg"
    img = np.asarray(Image.open(OUT / ("chavin_portada_v1_" + name + suffix)).convert("RGB")).astype(np.float32)
    lr = float(np.abs(img[:, 0] - img[:, -1]).mean())
    tb = float(np.abs(img[0, :] - img[-1, :]).mean())
    print("EDGE", name, round(lr, 2), round(tb, 2))

print("WROTE", OUT)
