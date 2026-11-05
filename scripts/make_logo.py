# -*- coding: utf-8 -*-
"""nightly 插件 logo 生成：原版齿轮设计 → 黑客帝国配色（黑底 + Matrix 绿线）。

原版元素（用户提供 640x640）：金色噪点背景 + 装饰细圆 + 白色圆(黑描边) + 黑色齿轮 + 顶部三角。
映射规则：背景金/白圆 → 纯黑；原黑色线条（描边/齿轮/三角/弧）→ Matrix 绿 #00FF41。

用法:
    python make_logo.py
"""
import os
from PIL import Image, ImageDraw
import numpy as np

SRC = r"D:\FuC\Desktop\dc45523c-db21-4d9d-b774-13452db311ef.jpeg"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(OUT_DIR, "..", "nightly", "assets", "ui", "logo.png")

# 黑线主体的亮度上界：L 低于此值按绿线强度渐变，高于则压黑
DARK_THRESHOLD = 110.0


def to_matrix(src_im: Image.Image) -> Image.Image:
    """黑底 + 绿线映射。绿色强度 = smoothstep(DARK_THRESHOLD - L)，保持 #00FF41 色相（B=G*65/255）。"""
    src = np.array(src_im, dtype=np.uint8)
    L = np.array(src_im.convert("L"), dtype=np.float32)
    t = np.clip((DARK_THRESHOLD - L) / DARK_THRESHOLD, 0.0, 1.0) ** 0.8
    g = (t * 255).astype(np.uint8)
    rgb = np.zeros((*g.shape, 3), dtype=np.uint8)
    rgb[..., 1] = g
    rgb[..., 2] = (g.astype(np.int16) * 65 // 255).astype(np.uint8)
    return Image.fromarray(rgb, "RGB")


def circular_crop(im: Image.Image, size: int) -> Image.Image:
    """中心圆形裁剪 + 透明四角（与插件 logo.png 圆形规格一致）。"""
    im = im.resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size - 1, size - 1], fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(im, (0, 0), mask)
    return out


def main() -> None:
    src = Image.open(SRC).convert("RGB")
    im = to_matrix(src)
    im.save(os.path.join(OUT_DIR, "logo_matrix_black.png"))
    logo = circular_crop(im, 256)
    logo.save(os.path.join(OUT_DIR, "logo_matrix_black_round.png"))
    logo.save(LOGO_PATH)
    print("logo updated:", os.path.normpath(LOGO_PATH))


if __name__ == "__main__":
    main()
