from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[4]
RENDER_DIR = ROOT / ".temp" / "rendered"
OUTPUT_DIR = ROOT / ".temp" / "llm-crops"


@dataclass
class Segment:
    top: int
    bottom: int


def load_page(page_number: int) -> Image.Image:
    path = RENDER_DIR / f"page-{page_number:03}.png"
    if not path.exists():
        raise FileNotFoundError(path)
    return Image.open(path).convert("RGB")


def blue_row_score(image: Image.Image, y: int) -> int:
    width, _ = image.size
    score = 0
    for x in range(width):
        red, green, blue = image.getpixel((x, y))
        if blue > 150 and blue - red > 15 and blue - green > 5:
            score += 1
    return score


def detect_rules(image: Image.Image) -> list[int]:
    width, height = image.size
    threshold = int(width * 0.30)
    candidates: list[int] = []
    for y in range(height):
        if blue_row_score(image, y) >= threshold:
            candidates.append(y)

    rules: list[int] = []
    for y in candidates:
        if not rules or y - rules[-1] > 6:
            rules.append(y)

    if len(rules) < 2:
        raise ValueError("横罫線を十分に検出できませんでした")
    return rules


def build_segments(image: Image.Image) -> list[Segment]:
    _, height = image.size
    rules = detect_rules(image)
    segments: list[Segment] = []
    for index in range(len(rules) - 1):
        top_rule = rules[index]
        bottom_rule = rules[index + 1]
        top = max(0, top_rule + 3)
        bottom = min(height, bottom_rule - 3)
        if bottom - top < 70:
            continue
        segments.append(Segment(top=top, bottom=bottom))
    return segments


def pad(image: Image.Image, border: int = 24) -> Image.Image:
    return ImageOps.expand(image, border=border, fill="white")


def stitch_pair(explanation: Image.Image, example: Image.Image) -> Image.Image:
    left = pad(explanation)
    right = pad(example)
    width = left.width + right.width
    height = max(left.height, right.height)
    canvas = Image.new("RGB", (width, height), "white")
    canvas.paste(left, (0, 0))
    canvas.paste(right, (left.width, 0))
    return canvas


def crop_pair(explanation_page: int, example_page: int, output_dir: Path) -> list[Path]:
    explanation = load_page(explanation_page)
    example = load_page(example_page)
    explanation_segments = build_segments(explanation)
    example_segments = build_segments(example)

    count = min(len(explanation_segments), len(example_segments))
    if count == 0:
        raise ValueError("切り出し対象の段が見つかりませんでした")

    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for index in range(count):
        left_segment = explanation_segments[index]
        right_segment = example_segments[index]
        left_crop = explanation.crop((0, left_segment.top, explanation.width, left_segment.bottom))
        right_crop = example.crop((0, right_segment.top, example.width, right_segment.bottom))
        merged = stitch_pair(left_crop, right_crop)
        output_path = output_dir / f"pair-{explanation_page:03}-{example_page:03}-{index + 1:02}.png"
        merged.save(output_path)
        written.append(output_path)
    return written


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("explanation_page", type=int)
    parser.add_argument("example_page", type=int)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()

    written = crop_pair(args.explanation_page, args.example_page, args.output_dir)
    for path in written:
        print(path.name)


if __name__ == "__main__":
    main()