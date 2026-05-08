#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw

FRAME_W = 16
FRAME_H = 32
SHEET_COLS = 7
SHEET_ROWS = 3
FRONT_LOOP_COLS = (0, 1, 2, 3, 2, 1, 0)
BACK_LOOP_COLS = (0, 1, 2, 3, 4, 5, 6)
SIDE_LOOP_COLS = (0, 1, 2, 3, 4, 5, 6)
FRONT_FACE_BOX = (4, 10, 12, 17)
BACK_HEAD_BOX = (4, 8, 12, 16)
PROFILE_FACE_BOX = (10, 11, 13, 18)
REVIEW_SCALE = 12
BOX_COLOR = (216, 109, 92, 255)


def _crop_frame(sheet: Image.Image, row: int, col: int) -> Image.Image:
    return sheet.crop((col * FRAME_W, row * FRAME_H, (col + 1) * FRAME_W, (row + 1) * FRAME_H))


def _normalized_pixel(pixel: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    if pixel[3] == 0:
        return (0, 0, 0, 0)
    return pixel


def _changed_pixels_in_box(current: Image.Image, source: Image.Image, box: tuple[int, int, int, int]) -> int:
    left, top, right, bottom = box
    changes = 0
    for y in range(top, bottom + 1):
        for x in range(left, right + 1):
            if _normalized_pixel(current.getpixel((x, y))) != _normalized_pixel(source.getpixel((x, y))):
                changes += 1
    return changes


def _review_strip(sheet: Image.Image, boxes: tuple[tuple[int, int, int, int], ...]) -> Image.Image:
    strip = Image.new("RGBA", (FRAME_W * SHEET_COLS, FRAME_H * SHEET_ROWS), (0, 0, 0, 0))
    for row in range(SHEET_ROWS):
        for col in range(SHEET_COLS):
            frame = _crop_frame(sheet, row, col).copy()
            draw = ImageDraw.Draw(frame)
            draw.rectangle(boxes[row], outline=BOX_COLOR, width=1)
            strip.paste(frame, (col * FRAME_W, row * FRAME_H), frame)
    return strip.resize((strip.width * REVIEW_SCALE, strip.height * REVIEW_SCALE), Image.Resampling.NEAREST)


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit face-zone collisions in Grimoire character sheets.")
    parser.add_argument("sheet", type=Path, help="Generated or curated character sheet to audit.")
    parser.add_argument("--source-sheet", type=Path, help="Optional source sheet for collision diffing.")
    parser.add_argument(
        "--layout",
        choices=("front-front-side",),
        default="front-front-side",
        help="Row layout mapping used by the generated sheet.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional output file for the zoomed review sheet.",
    )
    args = parser.parse_args()

    sheet = Image.open(args.sheet).convert("RGBA")
    face_boxes = (FRONT_FACE_BOX, BACK_HEAD_BOX, PROFILE_FACE_BOX)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        _review_strip(sheet, face_boxes).save(args.output)
        print(f"[audit] wrote review {args.output}")

    if not args.source_sheet:
        return 0

    source_sheet = Image.open(args.source_sheet).convert("RGBA")
    row_layouts = (
        (0, FRONT_LOOP_COLS),
        (1, BACK_LOOP_COLS),
        (2, SIDE_LOOP_COLS),
    )

    issues: list[str] = []
    for output_row, (source_row, source_cols) in enumerate(row_layouts):
        for col in range(SHEET_COLS):
            current = _crop_frame(sheet, output_row, col)
            source = _crop_frame(source_sheet, source_row, source_cols[col])
            changes = _changed_pixels_in_box(current, source, face_boxes[output_row])
            if changes:
                issues.append(f"row={output_row} col={col} changed_face_pixels={changes}")

    if issues:
        print("[audit] face-zone collisions detected:")
        for issue in issues:
            print(issue)
        return 1

    print("[audit] no face-zone collisions detected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())