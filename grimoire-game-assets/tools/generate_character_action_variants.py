#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw

INDEX_HEADERS = [
    "asset_id",
    "category",
    "source_id",
    "license",
    "relative_path",
    "frames",
    "tile_w",
    "tile_h",
    "states",
    "author",
    "notes",
    "validated",
]

FRAME_W = 16
FRAME_H = 32
SHEET_COLS = 7
SHEET_ROWS = 3
SHEET_W = FRAME_W * SHEET_COLS
SHEET_H = FRAME_H * SHEET_ROWS
AUTHOR = "github-copilot"
SOURCE_ID = "local-pixel-agents"
SOURCE_LICENSE = "internal-procedural"
FRONT_LOOP_COLS = (0, 1, 2, 3, 2, 1, 0)
BACK_LOOP_COLS = (0, 1, 2, 3, 4, 5, 6)
SIDE_LOOP_COLS = (0, 1, 2, 3, 4, 5, 6)
FRONT_FACE_BOX = (4, 10, 12, 17)
BACK_HEAD_BOX = (4, 8, 12, 16)
PROFILE_FACE_BOX = (10, 11, 13, 18)


@dataclass(frozen=True, slots=True)
class ActionSheetSpec:
    asset_id: str
    filename: str
    source_filename: str
    states: tuple[str, str, str]
    notes: str
    theme: str

    @property
    def relative_path(self) -> str:
        return f"10-curated/characters/{self.filename}"


ARCHIVIST_THEME = {
    "ink": (42, 35, 35, 255),
    "paper": (239, 230, 207, 255),
    "paper_shadow": (210, 198, 172, 255),
    "brass": (210, 176, 88, 255),
    "verdigris": (109, 152, 143, 255),
    "verdigris_dark": (80, 119, 114, 255),
}

OPERATOR_THEME = {
    "ink": (42, 35, 35, 255),
    "ink_mid": (73, 62, 66, 255),
    "ink_soft": (104, 88, 93, 255),
    "ember": (216, 109, 92, 255),
    "ember_dark": (139, 73, 69, 255),
    "brass": (210, 176, 88, 255),
    "paper": (239, 230, 207, 255),
    "paper_shadow": (208, 199, 184, 255),
}

OPERATOR_BLUE_REMAP = {
    (35, 41, 77, 255): OPERATOR_THEME["ink"],
    (52, 61, 90, 255): OPERATOR_THEME["ink_mid"],
    (73, 85, 126, 255): OPERATOR_THEME["ink_soft"],
}


SPECS = [
    ActionSheetSpec(
        asset_id="character_archivist_actions_v01",
        filename="character_archivist_actions_v01.png",
        source_filename="character_archivist_seed_v01.png",
        states=("show-ledger", "write-ledger", "read-scroll"),
        notes="Curated action pack for the archivist variant aligned to the source model pattern: front ledger, back writing pose and side scroll read.",
        theme="archivist",
    ),
    ActionSheetSpec(
        asset_id="character_operator_ember_actions_v01",
        filename="character_operator_ember_actions_v01.png",
        source_filename="character_seed_03_v01.png",
        states=("show-badge", "open-toolbox", "raise-lantern"),
        notes="Curated ember operator action pack with readable props: badge, toolbox and lantern.",
        theme="operator",
    ),
]


def _crop_frame(sheet: Image.Image, row: int, col: int) -> Image.Image:
    return sheet.crop((col * FRAME_W, row * FRAME_H, (col + 1) * FRAME_W, (row + 1) * FRAME_H))


def _remap_exact_colors(frame: Image.Image, replacements: dict[tuple[int, int, int, int], tuple[int, int, int, int]]) -> None:
    pixels = frame.load()
    for y in range(frame.height):
        for x in range(frame.width):
            color = pixels[x, y]
            replacement = replacements.get(color)
            if replacement is not None:
                pixels[x, y] = replacement


def _restore_box(target: Image.Image, source: Image.Image, box: tuple[int, int, int, int]) -> None:
    left, top, right, bottom = box
    source_pixels = source.load()
    target_pixels = target.load()
    for y in range(top, bottom + 1):
        for x in range(left, right + 1):
            target_pixels[x, y] = source_pixels[x, y]


def _restore_face_zone(frame: Image.Image, source_frame: Image.Image, row: int) -> None:
    if row == 0:
        face_box = FRONT_FACE_BOX
    elif row == 1:
        face_box = BACK_HEAD_BOX
    else:
        face_box = PROFILE_FACE_BOX
    _restore_box(frame, source_frame, face_box)


def _draw_box(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    *,
    outline: tuple[int, int, int, int],
    fill: tuple[int, int, int, int] | None = None,
) -> None:
    draw.rectangle(box, outline=outline, fill=fill)


def _draw_open_ledger(draw: ImageDraw.ImageDraw, x: int, y: int, theme: dict[str, tuple[int, int, int, int]]) -> None:
    _draw_box(draw, (x, y, x + 3, y + 4), outline=theme["ink"], fill=theme["paper"])
    _draw_box(draw, (x + 4, y, x + 7, y + 4), outline=theme["ink"], fill=theme["paper_shadow"])
    draw.line((x + 4, y + 1, x + 4, y + 4), fill=theme["brass"], width=1)
    draw.point((x + 2, y + 1), fill=theme["ink"])
    draw.point((x + 6, y + 1), fill=theme["ink"])


def _draw_quill(draw: ImageDraw.ImageDraw, x: int, y: int, theme: dict[str, tuple[int, int, int, int]]) -> None:
    draw.line((x, y, x + 2, y - 2), fill=theme["ink"], width=1)
    draw.point((x + 2, y - 3), fill=theme["paper"])
    draw.point((x + 3, y - 2), fill=theme["paper"])
    draw.point((x + 1, y - 2), fill=theme["paper"])


def _draw_mug(draw: ImageDraw.ImageDraw, x: int, y: int, theme: dict[str, tuple[int, int, int, int]]) -> None:
    _draw_box(draw, (x, y, x + 3, y + 3), outline=theme["ink"], fill=theme["verdigris"] if "verdigris" in theme else theme["paper_shadow"])
    draw.point((x + 4, y + 1), fill=theme["ink"])
    draw.point((x + 4, y + 2), fill=theme["ink"])
    draw.point((x + 1, y - 1), fill=theme["paper"])
    draw.point((x + 2, y - 2), fill=theme["paper"])


def _draw_scroll(draw: ImageDraw.ImageDraw, x: int, y: int, theme: dict[str, tuple[int, int, int, int]]) -> None:
    _draw_box(draw, (x, y, x + 3, y + 6), outline=theme["ink"], fill=theme["paper"])
    draw.line((x + 1, y + 1, x + 1, y + 5), fill=theme["paper_shadow"], width=1)
    draw.point((x + 2, y + 2), fill=theme["ink"])
    draw.point((x + 3, y + 3), fill=theme["brass"])


def _draw_badge(draw: ImageDraw.ImageDraw, x: int, y: int, theme: dict[str, tuple[int, int, int, int]]) -> None:
    _draw_box(draw, (x, y, x + 3, y + 4), outline=theme["ink"], fill=theme["paper"])
    draw.point((x + 1, y), fill=theme["brass"])
    draw.point((x + 2, y + 2), fill=theme["ink"])
    draw.line((x + 1, y + 3, x + 2, y + 3), fill=theme["paper_shadow"], width=1)


def _draw_toolbox(draw: ImageDraw.ImageDraw, x: int, y: int, theme: dict[str, tuple[int, int, int, int]]) -> None:
    _draw_box(draw, (x, y + 2, x + 7, y + 6), outline=theme["ink"], fill=theme["ember_dark"])
    draw.line((x + 1, y + 2, x + 6, y + 2), fill=theme["paper"], width=1)
    draw.line((x + 2, y + 1, x + 5, y + 1), fill=theme["brass"], width=1)
    draw.point((x + 3, y + 4), fill=theme["paper"])
    draw.point((x + 4, y + 4), fill=theme["paper"])


def _draw_lantern(draw: ImageDraw.ImageDraw, x: int, y: int, col: int, theme: dict[str, tuple[int, int, int, int]]) -> None:
    glow = [theme["brass"], theme["paper"], theme["brass"], theme["paper"], theme["brass"], theme["paper"], theme["brass"]][col]
    _draw_box(draw, (x, y, x + 2, y + 4), outline=theme["ink"], fill=glow)
    draw.point((x + 1, y - 1), fill=theme["ink"])
    sparkle_positions = (
        ((x + 4, y + 1),),
        ((x + 4, y + 1), (x + 5, y + 2)),
        ((x + 4, y + 2), (x + 5, y + 1)),
        ((x + 4, y + 1), (x + 5, y + 2)),
        ((x + 4, y + 2), (x + 5, y + 1)),
        ((x + 4, y + 1), (x + 5, y + 2)),
        ((x + 4, y + 1),),
    )[col]
    for sparkle_x, sparkle_y in sparkle_positions:
        if 0 <= sparkle_x < FRAME_W and 0 <= sparkle_y < FRAME_H:
            draw.point((sparkle_x, sparkle_y), fill=theme["paper"])


def _draw_simple_arm(
    draw: ImageDraw.ImageDraw,
    start: tuple[int, int],
    end: tuple[int, int],
    *,
    outline: tuple[int, int, int, int],
    fill: tuple[int, int, int, int],
) -> None:
    draw.line((start[0], start[1], end[0], end[1]), fill=outline, width=1)
    mid_x = (start[0] + end[0]) // 2
    mid_y = (start[1] + end[1]) // 2
    draw.point((mid_x, mid_y), fill=fill)


def _render_archivist_frame(frame: Image.Image, row: int, col: int) -> None:
    draw = ImageDraw.Draw(frame)
    theme = ARCHIVIST_THEME

    if row == 0:
        ledger_x = [4, 4, 4, 4, 5, 5, 4][col]
        ledger_y = 19
        _draw_open_ledger(draw, ledger_x, ledger_y, theme)
        _draw_simple_arm(draw, (5, 18), (ledger_x + 1, ledger_y + 4), outline=theme["verdigris_dark"], fill=theme["verdigris"])
        _draw_simple_arm(draw, (11, 18), (ledger_x + 6, ledger_y + 4), outline=theme["verdigris_dark"], fill=theme["verdigris"])
        return

    if row == 1:
        ledger_x = [4, 4, 4, 4, 5, 5, 4][col]
        ledger_y = 20
        _draw_open_ledger(draw, ledger_x, ledger_y, theme)
        quill_x = [8, 9, 10, 10, 9, 8, 8][col]
        quill_y = [19, 18, 18, 19, 20, 20, 19][col]
        _draw_quill(draw, quill_x, quill_y, theme)
        _draw_simple_arm(draw, (4, 18), (ledger_x + 1, ledger_y + 3), outline=theme["verdigris_dark"], fill=theme["verdigris"])
        _draw_simple_arm(draw, (11, 18), (quill_x, quill_y), outline=theme["verdigris_dark"], fill=theme["verdigris"])
        return

    scroll_x = [11, 11, 12, 12, 12, 11, 11][col]
    scroll_y = [16, 15, 15, 14, 15, 15, 16][col]
    _draw_scroll(draw, scroll_x, scroll_y, theme)
    _draw_simple_arm(draw, (10, 18), (scroll_x, scroll_y + 5), outline=theme["verdigris_dark"], fill=theme["verdigris"])


def _render_operator_frame(frame: Image.Image, row: int, col: int) -> None:
    draw = ImageDraw.Draw(frame)
    theme = OPERATOR_THEME

    if row == 0:
        badge_positions = [(9, 19), (9, 18), (10, 18), (10, 18), (10, 18), (9, 18), (9, 19)]
        badge_x, badge_y = badge_positions[col]
        _draw_badge(draw, badge_x, badge_y, theme)
        _draw_simple_arm(draw, (10, 18), (badge_x + 1, badge_y + 4), outline=theme["ember_dark"], fill=theme["ember"])
        return

    if row == 1:
        toolbox_x = [4, 4, 4, 4, 5, 5, 4][col]
        toolbox_y = 19
        _draw_toolbox(draw, toolbox_x, toolbox_y, theme)
        tool_positions = [(9, 22), (10, 22), (11, 21), (10, 20), (9, 21), (10, 22), (9, 22)]
        tool_x, tool_y = tool_positions[col]
        draw.line((tool_x, tool_y, tool_x + 2, tool_y - 2), fill=theme["brass"], width=1)
        draw.point((tool_x + 1, tool_y - 3), fill=theme["paper"])
        draw.point((tool_x + 2, tool_y - 1), fill=theme["paper"])
        _draw_simple_arm(draw, (4, 18), (toolbox_x + 1, toolbox_y + 2), outline=theme["ember_dark"], fill=theme["ember"])
        _draw_simple_arm(draw, (11, 18), (tool_x, tool_y), outline=theme["ember_dark"], fill=theme["ember"])
        if col in {2, 3, 4}:
            draw.point((toolbox_x + 2, toolbox_y + 1), fill=theme["paper"])
            draw.point((toolbox_x + 5, toolbox_y + 1), fill=theme["paper"])
        return

    lantern_positions = [(11, 16), (11, 15), (12, 14), (12, 13), (12, 14), (11, 15), (11, 16)]
    lantern_x, lantern_y = lantern_positions[col]
    _draw_lantern(draw, lantern_x, lantern_y, col, theme)
    _draw_simple_arm(draw, (10, 17), (lantern_x + 1, lantern_y + 4), outline=theme["ember_dark"], fill=theme["ember"])


def _render_sheet(spec: ActionSheetSpec, characters_dir: Path) -> Path:
    source_path = characters_dir / spec.source_filename
    source_sheet = Image.open(source_path).convert("RGBA")
    result = Image.new("RGBA", (SHEET_W, SHEET_H), (0, 0, 0, 0))

    if spec.theme == "archivist":
        row_layouts = (
            (0, FRONT_LOOP_COLS),
            (1, BACK_LOOP_COLS),
            (2, SIDE_LOOP_COLS),
        )
        render_frame = _render_archivist_frame
    else:
        row_layouts = (
            (0, FRONT_LOOP_COLS),
            (1, BACK_LOOP_COLS),
            (2, SIDE_LOOP_COLS),
        )
        render_frame = _render_operator_frame

    for output_row, (source_row, source_cols) in enumerate(row_layouts):
        for col in range(SHEET_COLS):
            frame = _crop_frame(source_sheet, source_row, source_cols[col])
            if spec.theme == "operator":
                _remap_exact_colors(frame, OPERATOR_BLUE_REMAP)
            source_frame = frame.copy()
            render_frame(frame, output_row, col)
            _restore_face_zone(frame, source_frame, output_row)
            result.paste(frame, (col * FRAME_W, output_row * FRAME_H), frame)

    target_path = characters_dir / spec.filename
    result.save(target_path, format="PNG")
    return target_path


def _update_index(index_file: Path, specs: list[ActionSheetSpec]) -> None:
    rows: list[dict[str, str]] = []
    by_id: dict[str, dict[str, str]] = {}

    if index_file.exists():
        with index_file.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                asset_id = (row.get("asset_id") or "").strip()
                if not asset_id:
                    continue
                rows.append(row)
                by_id[asset_id] = row

    for spec in specs:
        row = {
            "asset_id": spec.asset_id,
            "category": "characters",
            "source_id": SOURCE_ID,
            "license": SOURCE_LICENSE,
            "relative_path": spec.relative_path,
            "frames": "9",
            "tile_w": str(SHEET_W),
            "tile_h": str(SHEET_H),
            "states": "|".join(spec.states),
            "author": AUTHOR,
            "notes": spec.notes,
            "validated": "true",
        }

        if spec.asset_id in by_id:
            by_id[spec.asset_id].update(row)
        else:
            rows.append(row)

    with index_file.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=INDEX_HEADERS)
        writer.writeheader()
        for row in rows:
            writer.writerow({header: row.get(header, "") for header in INDEX_HEADERS})


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate deterministic action sheets for Grimoire seated characters.")
    parser.add_argument(
        "--assets-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Path to grimoire-game-assets root.",
    )
    args = parser.parse_args()

    assets_root = args.assets_root.resolve()
    characters_dir = assets_root / "10-curated" / "characters"
    index_file = assets_root / "manifests" / "assets-index.csv"

    generated_paths = [_render_sheet(spec, characters_dir) for spec in SPECS]
    _update_index(index_file, SPECS)

    for path in generated_paths:
        print(f"[character-actions] wrote {path}")
    print(f"[character-actions] updated index {index_file}")


if __name__ == "__main__":
    main()