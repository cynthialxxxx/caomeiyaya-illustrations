#!/usr/bin/env python3
"""Generate IP-locked showcase samples using the desktop-pet sprite frames."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SPRITESHEET = ROOT / "assets" / "caomeiyaya-reference" / "spritesheet.webp"
OUT_DIR = ROOT / "examples" / "caomeiyaya-showcase"
SKILL_OUT_DIR = ROOT / "caomeiyaya-illustrations" / "assets" / "caomeiyaya-showcase"

W, H = 2048, 1152
INK = "#27211f"
MUTED = "#6c655d"
RED = "#f04e59"
GREEN = "#6fb45e"
ORANGE = "#ed9b32"
BLUE = "#4f86c8"


def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Songti.ttc",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size=size, index=1 if bold else 0)
        except Exception:
            continue
    return ImageFont.load_default()


FONT_28 = font(28)
FONT_30 = font(30)
FONT_32 = font(32)
FONT_36 = font(36, bold=True)
FONT_42 = font(42, bold=True)


def extract_sprite_frames(limit: int = 18) -> list[Image.Image]:
    im = Image.open(SPRITESHEET).convert("RGBA")
    pixels = im.load()
    width, height = im.size
    visited: set[tuple[int, int]] = set()
    boxes: list[tuple[int, int, int, int, int]] = []

    def is_sprite(x: int, y: int) -> bool:
        r, g, b, a = pixels[x, y]
        return a > 10 and r + g + b > 45

    for y in range(height):
        for x in range(width):
            if (x, y) in visited or not is_sprite(x, y):
                continue
            stack = [(x, y)]
            visited.add((x, y))
            min_x = max_x = x
            min_y = max_y = y
            count = 0
            while stack:
                cx, cy = stack.pop()
                count += 1
                min_x, max_x = min(min_x, cx), max(max_x, cx)
                min_y, max_y = min(min_y, cy), max(max_y, cy)
                for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                    if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited and is_sprite(nx, ny):
                        visited.add((nx, ny))
                        stack.append((nx, ny))
            bw = max_x - min_x + 1
            bh = max_y - min_y + 1
            if count > 800 and 45 <= bw <= 140 and 55 <= bh <= 170:
                boxes.append((min_x, min_y, max_x, max_y, count))

    boxes = sorted(boxes, key=lambda b: (b[1], b[0]))
    selected: list[tuple[int, int, int, int, int]] = []
    for box in boxes:
        cx = (box[0] + box[2]) // 2
        cy = (box[1] + box[3]) // 2
        if all(abs(cx - ((old[0] + old[2]) // 2)) > 30 or abs(cy - ((old[1] + old[3]) // 2)) > 30 for old in selected):
            selected.append(box)
        if len(selected) >= limit:
            break

    frames: list[Image.Image] = []
    for box in selected:
        min_x, min_y, max_x, max_y, _ = box
        pad = 16
        frames.append(
            im.crop(
                (
                    max(0, min_x - pad),
                    max(0, min_y - pad),
                    min(width, max_x + pad),
                    min(height, max_y + pad),
                )
            )
        )
    return frames


def canvas() -> Image.Image:
    return Image.new("RGB", (W, H), "white")


def draw_label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, color: str = INK) -> None:
    x, y = xy
    bbox = draw.textbbox((x, y), text, font=FONT_32)
    draw.rounded_rectangle((bbox[0] - 14, bbox[1] - 8, bbox[2] + 14, bbox[3] + 8), radius=12, outline="#d8d0c4", width=3, fill="white")
    draw.text((x, y), text, fill=color, font=FONT_32)


def draw_arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], color: str = ORANGE, width: int = 6) -> None:
    draw.line((start, end), fill=color, width=width)
    ex, ey = end
    sx, sy = start
    dx = 1 if ex >= sx else -1
    dy = 1 if ey >= sy else -1
    draw.polygon([(ex, ey), (ex - 28 * dx, ey - 12 * dy), (ex - 16 * dx, ey + 20 * dy)], fill=color)


def paste_sprite(base: Image.Image, sprite: Image.Image, center: tuple[int, int], height: int = 230) -> None:
    work = sprite.copy()
    ratio = height / work.height
    work = work.resize((int(work.width * ratio), height), Image.LANCZOS)
    x = center[0] - work.width // 2
    y = center[1] - work.height // 2
    base.paste(work, (x, y), work)


def draw_box(draw: ImageDraw.ImageDraw, xyxy: tuple[int, int, int, int], text: str, color: str = GREEN) -> None:
    draw.rounded_rectangle(xyxy, radius=18, outline=INK, width=5, fill="white")
    x1, y1, x2, y2 = xyxy
    bbox = draw.textbbox((0, 0), text, font=FONT_36)
    draw.text((x1 + (x2 - x1 - (bbox[2] - bbox[0])) // 2, y1 + (y2 - y1 - (bbox[3] - bbox[1])) // 2), text, fill=color, font=FONT_36)


def paper(draw: ImageDraw.ImageDraw, x: int, y: int, text: str) -> None:
    draw.polygon([(x, y), (x + 116, y + 14), (x + 98, y + 94), (x - 12, y + 78)], outline=INK, fill="white")
    draw.text((x + 12, y + 28), text, fill=INK, font=FONT_28)


def sample_01(frames: list[Image.Image]) -> Image.Image:
    im = canvas()
    d = ImageDraw.Draw(im)
    for i, text in enumerate(["评论", "灵感", "截图", "链接", "想法"]):
        paper(d, 130 + (i % 2) * 130, 170 + i * 86, text)
        draw_arrow(d, (300 + (i % 2) * 110, 215 + i * 86), (760, 410 + i * 20))
    d.polygon([(760, 245), (1180, 245), (1015, 660), (925, 660)], outline=INK, fill="#f7f7f7")
    for x in range(790, 1140, 45):
        d.line((x, 280, x + 220, 600), fill="#b8b8b8", width=2)
    paste_sprite(im, frames[6], (710, 760), 340)
    d.arc((730, 650, 900, 800), 205, 330, fill=BLUE, width=5)
    for x in [875, 915, 955]:
        paper(d, x, 720 + (x - 875) // 2, "")
    draw_box(d, (1420, 610, 1740, 760), "可用线索")
    draw_arrow(d, (1100, 650), (1400, 685))
    draw_label(d, (610, 850), "先接住", BLUE)
    return im


def sample_02(frames: list[Image.Image]) -> Image.Image:
    im = canvas()
    d = ImageDraw.Draw(im)
    draw_box(d, (250, 470, 540, 630), "假设", MUTED)
    d.rounded_rectangle((850, 315, 1045, 760), radius=18, outline=INK, width=6, fill="#fff8ee")
    d.rectangle((900, 390, 1010, 720), outline=INK, width=4, fill="white")
    draw_label(d, (860, 250), "验证门", RED)
    paste_sprite(im, frames[8], (770, 610), 350)
    draw_arrow(d, (560, 550), (820, 550))
    draw_arrow(d, (1050, 550), (1355, 550))
    draw_box(d, (1380, 470, 1670, 630), "证据", GREEN)
    draw_label(d, (710, 805), "小步推一下", ORANGE)
    return im


def sample_03(frames: list[Image.Image]) -> Image.Image:
    im = canvas()
    d = ImageDraw.Draw(im)
    paste_sprite(im, frames[10], (470, 760), 340)
    d.line((840, 780, 920, 430), fill=GREEN, width=8)
    for end, label in [((740, 520), "文章"), ((1040, 500), "短视频"), ((710, 700), "案例"), ((1120, 700), "脚本")]:
        d.line((890, 560, end[0], end[1]), fill=GREEN, width=5)
        d.ellipse((end[0] - 35, end[1] - 35, end[0] + 35, end[1] + 35), fill="#ff626b", outline=INK, width=3)
        d.text((end[0] + 45, end[1] - 18), label, fill=INK, font=FONT_28)
    d.arc((545, 580, 780, 870), 320, 50, fill=BLUE, width=5)
    d.rounded_rectangle((1320, 710, 1620, 860), radius=22, outline=INK, width=5, fill="white")
    d.arc((1360, 650, 1580, 790), 0, 180, fill=INK, width=4)
    d.text((1395, 765), "素材库", fill=GREEN, font=FONT_36)
    draw_arrow(d, (1125, 710), (1310, 780))
    draw_label(d, (420, 905), "一颗想法", BLUE)
    return im


def sample_04(frames: list[Image.Image]) -> Image.Image:
    im = canvas()
    d = ImageDraw.Draw(im)
    d.arc((360, 480, 1640, 1040), 190, 350, fill=INK, width=7)
    d.line((370, 760, 760, 850), fill=INK, width=6)
    d.line((1280, 850, 1660, 760), fill=INK, width=6)
    labels = ["截图", "反馈", "数据", "案例", "承诺"]
    for i, label in enumerate(labels):
        x = 650 + i * 150
        y = 675 + (i % 2) * 34
        d.rounded_rectangle((x, y, x + 145, y + 78), radius=18, outline=INK, width=4, fill="#f1f1ed")
        d.text((x + 30, y + 22), label, fill=INK, font=FONT_30)
    paste_sprite(im, frames[12], (1240, 610), 330)
    d.rounded_rectangle((1540, 430, 1770, 525), radius=16, outline=INK, width=4, fill="white")
    d.text((1570, 455), "放心通过", fill=GREEN, font=FONT_32)
    draw_arrow(d, (450, 680), (630, 710))
    draw_arrow(d, (1400, 700), (1540, 650))
    return im


def sample_05(frames: list[Image.Image]) -> Image.Image:
    im = canvas()
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((545, 430, 1210, 780), radius=24, outline=INK, width=6, fill="white")
    d.text((740, 465), "小小控制台", fill=INK, font=FONT_36)
    for i, (label, color) in enumerate([("内容", RED), ("产品", GREEN), ("交付", BLUE)]):
        x = 690 + i * 170
        d.line((x, 610, x, 735), fill=INK, width=5)
        d.ellipse((x - 28, 570, x + 28, 626), fill=color, outline=INK, width=3)
        d.text((x - 30, 745), label, fill=INK, font=FONT_28)
    paste_sprite(im, frames[15], (470, 690), 350)
    draw_arrow(d, (1215, 610), (1420, 610))
    draw_box(d, (1445, 535, 1745, 685), "日常运转", GREEN)
    draw_label(d, (420, 845), "接住三件事", BLUE)
    return im


def sample_06(frames: list[Image.Image]) -> Image.Image:
    im = canvas()
    d = ImageDraw.Draw(im)
    for i, text in enumerate(["会议", "任务", "想法"]):
        paper(d, 235 + i * 105, 560 + i * 44, text)
        draw_arrow(d, (420 + i * 110, 615 + i * 38), (760, 610 + i * 20))
    d.rounded_rectangle((840, 350, 1320, 820), radius=28, outline=INK, width=6, fill="white")
    d.text((970, 395), "日报小机器", fill=INK, font=FONT_36)
    d.rectangle((970, 485, 1190, 600), outline=INK, width=4, fill="#f7fbff")
    for y in [660, 705, 750]:
        d.line((925, y, 1240, y), fill="#c6c6c6", width=3)
    paste_sprite(im, frames[9], (740, 765), 340)
    d.line((782, 665, 870, 625), fill=GREEN, width=6)
    draw_arrow(d, (1320, 620), (1480, 620))
    d.polygon([(1490, 500), (1770, 565), (1715, 810), (1440, 740)], outline=INK, fill="white")
    d.text((1515, 585), "今日摘要", fill=RED, font=FONT_32)
    d.text((1518, 645), "3 件重点", fill=BLUE, font=FONT_32)
    return im


def make_contact_sheet(paths: list[Path]) -> Image.Image:
    thumb_w, thumb_h = 520, 292
    padding = 24
    label_h = 44
    sheet = Image.new("RGB", (padding * 3 + thumb_w * 2, padding * 4 + (thumb_h + label_h) * 3), "white")
    draw = ImageDraw.Draw(sheet)
    for i, path in enumerate(paths):
        im = Image.open(path).convert("RGB")
        im.thumbnail((thumb_w, thumb_h), Image.LANCZOS)
        x = padding + (i % 2) * (thumb_w + padding)
        y = padding + (i // 2) * (thumb_h + label_h + padding)
        sheet.paste(im, (x, y))
        draw.text((x, y + thumb_h + 8), path.name, fill=INK, font=FONT_28)
    return sheet


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    SKILL_OUT_DIR.mkdir(parents=True, exist_ok=True)
    frames = extract_sprite_frames()
    samples = [
        ("01-info-overload.png", sample_01),
        ("02-product-validation.png", sample_02),
        ("03-content-compound.png", sample_03),
        ("04-trust-bridge.png", sample_04),
        ("05-one-person-company.png", sample_05),
        ("06-auto-daily-report.png", sample_06),
    ]
    written: list[Path] = []
    for name, maker in samples:
        image = maker(frames)
        root_path = OUT_DIR / name
        skill_path = SKILL_OUT_DIR / name
        image.save(root_path)
        image.save(skill_path)
        written.append(root_path)
        print(f"wrote {root_path}")
        print(f"wrote {skill_path}")
    contact = make_contact_sheet(written)
    contact.save(OUT_DIR / "contact-sheet.png")
    print(f"wrote {OUT_DIR / 'contact-sheet.png'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
