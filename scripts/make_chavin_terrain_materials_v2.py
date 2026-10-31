"""Genera el detalle neutro del valle y el normal del agua de Chavín v0.7.

Uso:
    python3 scripts/make_chavin_terrain_materials_v2.py

Salida:
    blender/textures/chavin/chavin_terrain_v2_diffuse.jpg
    blender/textures/chavin/chavin_terrain_v2_roughness.jpg
    blender/textures/chavin/chavin_terrain_v2_normal.png
    blender/textures/chavin/chavin_water_v1_normal.png
"""

from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

OUT = Path("blender/textures/chavin")
OUT.mkdir(parents=True, exist_ok=True)


def noise(size, seed, sigma):
    rng = np.random.default_rng(seed)
    data = rng.normal(0.0, 1.0, (size, size)).astype(np.float32)
    return gaussian_filter(data, sigma=sigma, mode="wrap")


def normalized(data):
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


def terrain_detail():
    size = 1024
    broad = normalized(noise(size, 811, size / 28))
    medium = normalized(noise(size, 821, size / 95))
    fine = noise(size, 829, 0.9)
    grit = (noise(size, 839, 0.45) > 1.35).astype(np.float32)
    grit = gaussian_filter(grit, sigma=0.7, mode="wrap")

    tone = 0.55 * broad + 0.32 * medium + 0.13 * fine
    tone = np.clip((tone - 0.5) * 1.2 + 0.5, 0.0, 1.0)

    color = np.zeros((size, size, 3), dtype=np.float32)
    color[:, :, 0] = 186 * (0.82 + 0.30 * tone)
    color[:, :, 1] = 181 * (0.82 + 0.28 * tone)
    color[:, :, 2] = 168 * (0.80 + 0.26 * tone)
    color *= 1.0 - 0.12 * grit[:, :, None]
    color = np.clip(color, 0, 255)

    height = 0.58 * broad + 0.27 * medium + 0.15 * fine
    height -= 0.22 * grit
    roughness = 0.84 + 0.07 * (fine - 0.5) + 0.05 * (1.0 - height)
    roughness = np.clip(roughness, 0.70, 0.97)

    Image.fromarray(color.astype(np.uint8), "RGB").save(
        OUT / "chavin_terrain_v2_diffuse.jpg", quality=92, optimize=True
    )
    Image.fromarray((roughness * 255).astype(np.uint8), "L").save(
        OUT / "chavin_terrain_v2_roughness.jpg", quality=92, optimize=True
    )
    Image.fromarray(normal_from_height(height, 0.9)).save(
        OUT / "chavin_terrain_v2_normal.png"
    )


def water_normal():
    size = 512
    axis = np.linspace(0.0, 2.0 * np.pi, size, endpoint=False, dtype=np.float32)
    xx, yy = np.meshgrid(axis, axis)
    height = (
        0.55 * np.sin(xx * 7.0 + yy * 1.5)
        + 0.30 * np.sin(yy * 13.0 - xx * 2.0)
        + 0.15 * np.sin((xx + yy) * 23.0)
    )
    height += 0.18 * noise(size, 907, 1.1)
    normal = normal_from_height(height, 1.7)
    Image.fromarray(normal).save(OUT / "chavin_water_v1_normal.png")


if __name__ == "__main__":
    terrain_detail()
    water_normal()
    print("WROTE", OUT)
