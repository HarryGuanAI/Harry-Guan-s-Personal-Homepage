from pathlib import Path
import math
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "deps"))

import imageio.v3 as iio
from PIL import Image, ImageEnhance
import numpy as np


ROOT = Path(__file__).resolve().parent
THINKING_SRC = Path(
    r"C:\Users\ghl45\.codex\generated_images\019de282-f3c1-75c3-9149-f92fb1d48139\ig_011d9e7295af421f0169f464adddac81979d2fe03e38ab4d19.png"
)
WAVE_SRC = Path(
    r"C:\Users\ghl45\.codex\generated_images\019de282-f3c1-75c3-9149-f92fb1d48139\ig_011d9e7295af421f0169f4705a48b88197a48ac457d7cbd823.png"
)
OUT = ROOT / "personal_ip_hero_loop_1080p_6s.mp4"
FRAME_DIR = ROOT / "frames"

W, H = 1920, 1080
FPS = 30
DURATION = 6
TOTAL = FPS * DURATION


def ease(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def cover_resize(img: Image.Image, scale=1.0, dx=0, dy=0) -> Image.Image:
    src_w, src_h = img.size
    factor = max(W / src_w, H / src_h) * scale
    nw, nh = round(src_w * factor), round(src_h * factor)
    resized = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - W) // 2 - dx
    top = (nh - H) // 2 - dy
    canvas = Image.new("RGB", (W, H), (10, 12, 13))
    canvas.paste(resized, (-left, -top))
    return canvas


def blend(a: Image.Image, b: Image.Image, alpha: float) -> Image.Image:
    return Image.blend(a, b, ease(alpha))


def frame_at(i: int, thinking: Image.Image, wave: Image.Image) -> Image.Image:
    t = i / FPS
    if i == 0 or i == TOTAL - 1:
        return cover_resize(thinking, 1.0, 0, 0)

    breath = math.sin(math.pi * t / DURATION) ** 2
    micro = math.sin(2 * math.pi * t / 3.0)
    scale = 1.0 + 0.006 * breath + 0.002 * micro
    dy = round(3 * breath + 1.5 * micro)
    base = cover_resize(thinking, scale, 0, dy)

    if 1.45 <= t < 2.35:
        p = (t - 1.45) / 0.90
        wave_img = cover_resize(wave, 1.0 + 0.004 * math.sin(math.pi * p), 0, 0)
        return blend(base, wave_img, p)

    if 2.35 <= t < 3.45:
        wave_breath = 1.0 + 0.004 * math.sin(2 * math.pi * (t - 2.35) / 1.10)
        wave_dx = round(3 * math.sin(2 * math.pi * (t - 2.35) / 0.55))
        return cover_resize(wave, wave_breath, wave_dx, 0)

    if 3.45 <= t < 4.35:
        p = (t - 3.45) / 0.90
        wave_img = cover_resize(wave, 1.0, 0, 0)
        return blend(wave_img, base, p)

    return base


def main() -> None:
    FRAME_DIR.mkdir(parents=True, exist_ok=True)
    thinking = Image.open(THINKING_SRC).convert("RGB")
    wave = Image.open(WAVE_SRC).convert("RGB")

    frames = []
    for i in range(TOTAL):
        img = frame_at(i, thinking, wave)
        img = ImageEnhance.Sharpness(img).enhance(1.03)
        if i in {0, TOTAL - 1, 45, 75, 105, 150}:
            img.save(FRAME_DIR / f"preview_{i:03d}.jpg", quality=95)
        frames.append(np.asarray(img))

    iio.imwrite(
        OUT,
        frames,
        fps=FPS,
        codec="libx264",
        quality=8,
        pixelformat="yuv420p",
        macro_block_size=None,
    )
    print(OUT)


if __name__ == "__main__":
    main()
