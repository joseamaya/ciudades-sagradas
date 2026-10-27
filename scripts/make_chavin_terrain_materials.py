"""Genera la textura de terreno del preview de Chavín.

Uso:
    python3 scripts/make_chavin_terrain_materials.py

Salida:
    blender/textures/chavin/chavin_terrain_v1_diffuse.jpg
    blender/textures/chavin/chavin_terrain_v1_roughness.jpg
    blender/textures/chavin/chavin_terrain_v1_normal.png
"""

from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

SIZE = 1024
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


def main():
    broad = normalized(noise(SIZE, 701, SIZE / 24))
    medium = normalized(noise(SIZE, 707, SIZE / 90))
    fine = noise(SIZE, 711, 0.8)
    pebbles = (noise(SIZE, 719, 0.55) > 1.7).astype(np.float32)
    pebbles = gaussian_filter(pebbles, sigma=0.8, mode="wrap")

    tone = 0.56 * broad + 0.31 * medium + 0.13 * fine
    tone = np.clip((tone - 0.5) * 1.35 + 0.5, 0.0, 1.0)
    color = np.zeros((SIZE, SIZE, 3), dtype=np.float32)
    color[:, :, 0] = 166 * (0.58 + 0.66 * tone)
    color[:, :, 1] = 139 * (0.56 + 0.64 * tone)
    color[:, :, 2] = 101 * (0.52 + 0.62 * tone)
    color *= 1.0 - 0.20 * pebbles[:, :, None]
    color[:, :, 0] += 10 * medium
    color[:, :, 1] += 7 * medium
    color = np.clip(color, 0, 255)

    height = 0.58 * broad + 0.27 * medium + 0.15 * fine
    height -= 0.28 * pebbles
    roughness = 0.82 + 0.08 * (fine - 0.5) + 0.06 * (1.0 - height)
    roughness = np.clip(roughness, 0.64, 0.96)

    Image.fromarray(color.astype(np.uint8), "RGB").save(
        OUT / "chavin_terrain_v1_diffuse.jpg", quality=92, optimize=True
    )
    Image.fromarray((roughness * 255).astype(np.uint8), "L").save(
        OUT / "chavin_terrain_v1_roughness.jpg", quality=92, optimize=True
    )
    Image.fromarray(normal_from_height(height, 1.1)).save(
        OUT / "chavin_terrain_v1_normal.png"
    )
    print("WROTE", OUT)


if __name__ == "__main__":
    main()
