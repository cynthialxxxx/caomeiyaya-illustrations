#!/usr/bin/env python3
"""Generate Caomeiyaya showcase samples with Qwen Image.

The script uses the DashScope/Model Studio multimodal generation endpoint.
It intentionally never prints or writes the API key.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "examples" / "caomeiyaya-showcase-qwen"
META_DIR = OUT_DIR / "_meta"

MODEL = os.getenv("QWEN_IMAGE_MODEL", "qwen-image-2.0-pro")
SIZE = os.getenv("QWEN_IMAGE_SIZE", "2048*1152")
BASE_URL = os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/api/v1").rstrip("/")
ENDPOINT = f"{BASE_URL}/services/aigc/multimodal-generation/generation"
PROMPT_EXTEND = os.getenv("QWEN_PROMPT_EXTEND", "false").lower() in {"1", "true", "yes"}
REFERENCE_IMAGES = [
    item.strip()
    for item in os.getenv("QWEN_REFERENCE_IMAGES", "").split(",")
    if item.strip()
]

NEGATIVE_PROMPT = (
    "低分辨率，低画质，图片模糊，构图混乱，信息过载，背景复杂，PPT模板感，商业海报感，"
    "儿童贴纸感，3D渲染，厚重阴影，渐变背景，照片质感，写实人像，文字模糊，文字扭曲，"
    "错别字，英文乱码，角色缺少草莓帽，角色缺少叶片刘海，角色只是站在角落装饰，"
    "多余标题，左上角大标题，黑色说明文字段落，大段中文，正文段落，复杂说明，边框卡片，水印。"
)

STYLE_PREFIX = """
16:9 横版中文正文配图，纯白背景，大量留白，黑色手绘线稿，少量草莓红、叶片绿、橙色箭头和蓝色辅助批注。
画面像中文文章里的正文插图，不是封面，不是 PPT，不是商业海报，不要复杂架构图，不要满屏文字。

固定角色：草莓芽芽。必须以输入参考图中的桌宠 spritesheet / IP 标准板为唯一角色锚点，不要重新设计角色。她是极高头身比的小桌宠，不是草莓帽小女孩：圆鼓鼓草莓壳帽、额前绿色叶片刘海形成叶冠、短手短脚、圆脸亮眼粉腮、浅绿色连体装、红色小鞋、厚黑描边、Q 版玩偶感。
草莓芽芽必须承担画面的核心动作，不能只是站在旁边。读者要一眼看到她正在推动、搬运、修补、筛选、搭桥、踩机器或操作系统。如果角色不像参考图里的桌宠草莓芽芽，则本图不合格。

文字要求：只出现 3 到 6 个短中文标签，字要清晰可读。不要写说明长句，不要写英文，不要写大标题。
绝对不要把提示词里的“主题、核心隐喻、画面、构图、要求”等说明文字写进图里。图上只能出现指定的短标签词，不能出现任何说明段落、标题、摘要、冒号式长句或顶部大段文字。
整体气质：清爽、低科技、手绘解释图、轻微戏剧感、可爱服务于结构表达。
""".strip()


SAMPLES = [
    {
        "filename": "01-info-overload.png",
        "title": "信息过载",
        "prompt": """
主题：信息过载。核心隐喻：把乱飞的信息筛成可用线索。
画面：左侧有 5 张小纸片飞来，分别标注“评论”“灵感”“截图”“链接”“想法”；中间是一个手绘低科技大漏斗；草莓芽芽站在漏斗下方，双手接住掉下来的信息颗粒，并把它们放进右侧小盒子。右侧盒子标注“可用线索”。用少量橙色箭头表示流向。
构图：左侧输入，中间筛选，右侧输出。草莓芽芽在漏斗下方承担接住和整理动作。
""",
    },
    {
        "filename": "02-product-validation.png",
        "title": "产品验证",
        "prompt": """
主题：产品验证。核心隐喻：别急着做大，先推过一扇小门。
画面：左侧有一个小盒子标注“假设”；中间是一扇窄窄的手绘小门，门上小标签“验证门”；草莓芽芽正用肩膀和双手把“假设”盒子推过小门；右侧有一个更稳的小盒子标注“证据”。门口可以有一条小小门槛，强调费力但可通过。
构图：三段式，线条稀疏，草莓芽芽是推动验证的主体。
""",
    },
    {
        "filename": "03-content-compound.png",
        "title": "内容复利",
        "prompt": """
主题：内容复利。核心隐喻：一次想法被持续浇灌，长出多种产物。
画面：左下角草莓芽芽拿小水壶给一株简洁的内容植物浇水；植物枝头长出 4 个小果实，分别标注“文章”“短视频”“案例”“脚本”；右侧有一个小篮子标注“素材库”，成熟果实沿着轻微箭头落进篮子。
构图：左下角色动作，中间植物结构，右侧沉淀结果。不要画成农场或儿童画，要像文章解释图。
""",
    },
    {
        "filename": "04-trust-bridge.png",
        "title": "信任建立",
        "prompt": """
主题：信任建立。核心隐喻：信任不是喊出来的，是一块块证据铺过去的。
画面：中间是一条很浅的小裂谷；草莓芽芽正在搬一块石头放到桥上，石头上写“案例”；桥上还有几块石头，分别标注“截图”“数据”“反馈”“承诺”；左侧是一个小人轮廓，右侧是“放心通过”的小路牌。
构图：桥横向展开，草莓芽芽在桥中间搬证据石头，承担核心动作。画面清爽，少量橙色路径线。
""",
    },
    {
        "filename": "05-one-person-company.png",
        "title": "一人公司",
        "prompt": """
主题：一人公司。核心隐喻：不是变成三个人，而是让系统接住三件事。
画面：中间是一个手绘小控制台，只有三根拉杆，标签分别是“内容”“产品”“交付”；草莓芽芽站在控制台前，踮脚同时调整拉杆；右侧输出一个小卡片标注“日常运转”。控制台下方可以有几条简单线缆，但不要复杂。
构图：角色在中间操作系统，右侧输出结果。像随手画的解释草图。
""",
    },
    {
        "filename": "06-auto-daily-report.png",
        "title": "自动日报",
        "prompt": """
主题：自动日报。核心隐喻：碎片进入小机器，吐出当天摘要。
画面：左侧有三张碎纸片标注“会议”“任务”“想法”；中间是一台手绘日报小机器，机器上有小窗口和几条横线；草莓芽芽踩着脚踏板让机器运转，同时拉住一根草莓藤蔓；右侧吐出一张纸，标注“今日摘要”“3 件重点”。
构图：输入、机器处理、输出，草莓芽芽必须参与让机器运转。白底，留白多，文字少。
""",
    },
]


def build_payload(prompt: str) -> dict[str, Any]:
    content = [{"image": url} for url in REFERENCE_IMAGES[:3]]
    content.append({"text": f"{STYLE_PREFIX}\n\n{prompt.strip()}"})
    return {
        "model": MODEL,
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": content,
                }
            ]
        },
        "parameters": {
            "negative_prompt": NEGATIVE_PROMPT,
            "prompt_extend": PROMPT_EXTEND,
            "watermark": False,
            "size": SIZE,
        },
    }


def request_json(payload: dict[str, Any]) -> dict[str, Any]:
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise RuntimeError("DASHSCOPE_API_KEY is not set")

    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        ENDPOINT,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    for attempt in range(1, 5):
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", "replace")
            if exc.code == 429 and attempt < 4:
                delay = 45 * attempt
                print(f"rate limited; retrying in {delay}s")
                time.sleep(delay)
                continue
            raise RuntimeError(f"HTTP {exc.code}: {body}") from exc
    raise RuntimeError("request failed after retries")


def extract_image_url(response: dict[str, Any]) -> str:
    choices = response.get("output", {}).get("choices", [])
    for choice in choices:
        for item in choice.get("message", {}).get("content", []):
            image_url = item.get("image")
            if image_url:
                return image_url
    raise RuntimeError(f"No image URL in response: {json.dumps(response, ensure_ascii=False)[:1000]}")


def download(url: str, path: Path) -> None:
    with urllib.request.urlopen(url, timeout=180) as response:
        path.write_bytes(response.read())


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    META_DIR.mkdir(parents=True, exist_ok=True)

    print(f"endpoint: {ENDPOINT}")
    print(f"model: {MODEL}")
    print(f"size: {SIZE}")
    print(f"prompt_extend: {PROMPT_EXTEND}")
    print(f"reference images: {len(REFERENCE_IMAGES[:3])}")
    for index, sample in enumerate(SAMPLES, start=1):
        target = OUT_DIR / sample["filename"]
        meta = META_DIR / f"{Path(sample['filename']).stem}.json"
        if target.exists() and meta.exists():
            print(f"[{index}/{len(SAMPLES)}] skipping existing {sample['filename']}")
            continue
        print(f"[{index}/{len(SAMPLES)}] generating {sample['filename']} - {sample['title']}")
        payload = build_payload(sample["prompt"])
        response = request_json(payload)
        image_url = extract_image_url(response)
        download(image_url, target)
        meta.write_text(
            json.dumps(
                {
                    "filename": sample["filename"],
                    "title": sample["title"],
                    "model": MODEL,
                    "size": SIZE,
                    "endpoint": ENDPOINT,
                    "reference_images": REFERENCE_IMAGES[:3],
                    "request_id": response.get("request_id"),
                    "usage": response.get("usage"),
                    "prompt": payload["input"]["messages"][0]["content"][-1]["text"],
                    "negative_prompt": NEGATIVE_PROMPT,
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"saved: {target}")
        time.sleep(1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
