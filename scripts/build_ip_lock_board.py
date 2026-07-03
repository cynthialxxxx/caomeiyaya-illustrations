#!/usr/bin/env python3
"""Build the Caomeiyaya IP lock board from the desktop pet spritesheet."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "caomeiyaya-reference" / "spritesheet.webp"
OUT_DIR = ROOT / "assets" / "caomeiyaya-ip-lock"
SKILL_OUT_DIR = ROOT / "caomeiyaya-illustrations" / "assets" / "caomeiyaya-ip-lock"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
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


def extract_frames(limit: int = 18) -> list[Image.Image]:
    im = Image.open(SOURCE).convert("RGBA")
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
                    if (
                        0 <= nx < width
                        and 0 <= ny < height
                        and (nx, ny) not in visited
                        and is_sprite(nx, ny)
                    ):
                        visited.add((nx, ny))
                        stack.append((nx, ny))
            box_w = max_x - min_x + 1
            box_h = max_y - min_y + 1
            if count > 800 and 45 <= box_w <= 140 and 55 <= box_h <= 170:
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
        pad = 18
        crop = im.crop(
            (
                max(0, min_x - pad),
                max(0, min_y - pad),
                min(width, max_x + pad),
                min(height, max_y + pad),
            )
        )
        bg = Image.new("RGBA", crop.size, (255, 255, 255, 255))
        bg.alpha_composite(crop)
        frames.append(bg.convert("RGB"))
    return frames


def draw_multiline(draw: ImageDraw.ImageDraw, xy: tuple[int, int], lines: list[str], fill: str, fnt: ImageFont.ImageFont, leading: int) -> int:
    x, y = xy
    for line in lines:
        draw.text((x, y), line, fill=fill, font=fnt)
        y += leading
    return y


def make_frames_sheet(frames: list[Image.Image]) -> Image.Image:
    thumb = 164
    pad = 24
    cols = 6
    rows = 3
    canvas = Image.new("RGB", (cols * thumb + (cols + 1) * pad, rows * thumb + (rows + 1) * pad), "white")
    for index, frame in enumerate(frames[: cols * rows]):
        work = frame.copy()
        work.thumbnail((thumb, thumb), Image.LANCZOS)
        x = pad + (index % cols) * (thumb + pad) + (thumb - work.width) // 2
        y = pad + (index // cols) * (thumb + pad) + (thumb - work.height) // 2
        canvas.paste(work, (x, y))
    return canvas


def make_model_sheet(frames: list[Image.Image]) -> Image.Image:
    title = font(52, bold=True)
    heading = font(30, bold=True)
    body = font(25)
    small = font(21)
    canvas = Image.new("RGB", (2400, 1600), "#fffdf8")
    draw = ImageDraw.Draw(canvas)

    red = "#f14d58"
    green = "#78b861"
    ink = "#2b2522"
    muted = "#6f6860"
    orange = "#f0a23a"
    blue = "#4d86c6"

    draw.rounded_rectangle((52, 52, 2348, 1548), radius=34, outline="#eadfcf", width=3)
    draw.text((96, 82), "草莓芽芽 IP 标准板", fill=ink, font=title)
    draw.text((100, 152), "主锚点：桌宠 spritesheet 默认形象。样片生成前必须先满足本页识别规则。", fill=muted, font=body)

    frames_sheet = make_frames_sheet(frames)
    frames_sheet.thumbnail((1280, 560), Image.LANCZOS)
    draw.rounded_rectangle((92, 230, 1452, 850), radius=24, fill="white", outline="#eee2d2", width=2)
    canvas.paste(frames_sheet, (132, 275))
    draw.text((132, 238), "默认帧集合：比例、轮廓、表情和动作节奏以这里为准", fill=ink, font=heading)

    main = frames[1 if len(frames) > 1 else 0].copy()
    main.thumbnail((420, 420), Image.LANCZOS)
    draw.rounded_rectangle((1510, 230, 2265, 850), radius=24, fill="white", outline="#eee2d2", width=2)
    canvas.paste(main, (1585, 330))
    draw.text((1548, 238), "单体识别规则", fill=ink, font=heading)
    y = 312
    dna = [
        ("圆壳草莓帽", red),
        ("额前叶冠刘海", green),
        ("短手短脚桌宠比例", ink),
        ("浅绿连体装 + 红鞋", green),
        ("圆脸、亮眼、粉腮", red),
        ("厚黑描边，Q 版玩偶感", ink),
    ]
    for label, color in dna:
        draw.rounded_rectangle((1920, y + 4, 1948, y + 32), radius=8, fill=color)
        draw.text((1965, y), label, fill=ink, font=body)
        y += 58

    draw.rounded_rectangle((92, 915, 720, 1456), radius=24, fill="white", outline="#eee2d2", width=2)
    draw.text((132, 950), "不可变特征", fill=ink, font=heading)
    draw_multiline(
        draw,
        (132, 1012),
        [
            "1. 草莓帽必须是圆鼓鼓的外壳",
            "2. 叶片刘海贴在额头，形成叶冠",
            "3. 身体是小桌宠，不拉成长身小女孩",
            "4. 绿色连体装、红鞋、草莓吊坠保留",
            "5. 表情软萌，但不能只做装饰",
            "6. 线条厚实，避免轻水彩泛角色",
        ],
        ink,
        small,
        54,
    )

    draw.rounded_rectangle((770, 915, 1398, 1456), radius=24, fill="white", outline="#eee2d2", width=2)
    draw.text((810, 950), "允许变化", fill=ink, font=heading)
    draw_multiline(
        draw,
        (810, 1012),
        [
            "1. 可以坐、跑、推、拉、搬、修补",
            "2. 可加入藤蔓、小篮子、果酱罐",
            "3. 可根据正文变成努力/困惑/开心",
            "4. 可降低颜色饱和度适配白底插图",
            "5. 可让道具承担信息结构",
            "6. 可保留少量红橙蓝中文标注",
        ],
        ink,
        small,
        54,
    )

    draw.rounded_rectangle((1448, 915, 2265, 1456), radius=24, fill="white", outline="#eee2d2", width=2)
    draw.text((1488, 950), "禁止跑偏", fill=ink, font=heading)
    draw_multiline(
        draw,
        (1488, 1012),
        [
            "1. 不要画成草莓帽小女孩",
            "2. 不要把帽子变成普通兜帽或头盔",
            "3. 不要丢掉叶片刘海和红鞋",
            "4. 不要变成儿童绘本、水彩插画或商业海报",
            "5. 不要让角色站在角落旁观",
            "6. 不要让配图结构脱离角色动作",
        ],
        ink,
        small,
        54,
    )

    draw.line((100, 1498, 2300, 1498), fill="#eadfcf", width=2)
    draw.text((100, 1518), "生成验收：去掉草莓芽芽后图的核心动作不应成立；第一眼必须像桌宠草莓芽芽，而不是泛草莓角色。", fill=muted, font=small)
    draw.text((2020, 1518), "red/green = IP identity", fill=blue, font=small)
    draw.rounded_rectangle((1990, 1515, 2014, 1539), radius=6, fill=orange)
    return canvas


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    SKILL_OUT_DIR.mkdir(parents=True, exist_ok=True)
    frames = extract_frames()
    frames_sheet = make_frames_sheet(frames)
    model_sheet = make_model_sheet(frames)
    outputs = {
        "default-sprite-frames.png": frames_sheet,
        "caomeiyaya-ip-model-sheet.png": model_sheet,
    }
    for name, image in outputs.items():
        image.save(OUT_DIR / name)
        image.save(SKILL_OUT_DIR / name)
        print(f"wrote {OUT_DIR / name}")
        print(f"wrote {SKILL_OUT_DIR / name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
