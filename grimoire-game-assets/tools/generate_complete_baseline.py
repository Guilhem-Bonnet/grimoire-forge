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

SOURCE_ID = "grimoire-procedural-pack-v1"
SOURCE_LICENSE = "internal-procedural"
AUTHOR = "grimoire-generator"
NOTES = "Procedural baseline aligned to the Grimoire 2D style guide; review before final hero use."

PALETTES: dict[str, tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]] = {
    "neutral": ((102, 90, 77), (187, 166, 126), (58, 49, 43), (241, 229, 204)),
    "parchment": ((149, 126, 93), (214, 188, 142), (82, 67, 50), (248, 238, 215)),
    "brass": ((139, 119, 70), (210, 176, 88), (74, 58, 31), (255, 231, 160)),
    "verdigris": ((91, 122, 116), (134, 176, 167), (46, 65, 62), (220, 244, 236)),
    "memory": ((107, 103, 148), (163, 158, 219), (58, 53, 89), (232, 226, 255)),
    "ember": ((139, 73, 69), (216, 109, 92), (72, 34, 35), (255, 208, 173)),
    "leaf": ((110, 132, 80), (168, 192, 112), (58, 70, 42), (232, 243, 183)),
    "storm": ((90, 105, 134), (132, 160, 198), (45, 55, 73), (224, 240, 255)),
}


@dataclass(frozen=True, slots=True)
class AssetSpec:
    asset_id: str
    category: str
    filename: str
    frame_w: int
    frame_h: int
    frames: int = 1
    states: str = "default"

    @property
    def relative_path(self) -> str:
        return f"10-curated/{self.category}/{self.filename}"


def _palette(asset_id: str, category: str) -> tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]:
    token = asset_id.lower()

    if category == "fx":
        if _contains_any(token, ("done", "achievement", "xp", "challenge", "confetti")):
            return PALETTES["brass"]
        if _contains_any(token, ("memory",)):
            return PALETTES["memory"]
        if _contains_any(token, ("handoff", "broadcast", "subagent", "spawn")):
            return PALETTES["verdigris"]
        if _contains_any(token, ("error", "flash", "panic", "reject")):
            return PALETTES["ember"]
        if _contains_any(token, ("document",)):
            return PALETTES["parchment"]
        if _contains_any(token, ("rain", "window")):
            return PALETTES["storm"]

    if category == "ui":
        if _contains_any(token, ("error", "panic")):
            return PALETTES["ember"]
        if _contains_any(token, ("warning", "security", "bug")):
            return PALETTES["brass"]
        if _contains_any(token, ("done", "success")):
            return PALETTES["leaf"]
        if _contains_any(token, ("reading", "doc", "library")):
            return PALETTES["parchment"]
        if _contains_any(token, ("search", "subagent", "link", "timeline", "room", "progress", "header")):
            return PALETTES["storm"]
        return PALETTES["neutral"]

    if category == "furniture":
        if _contains_any(token, ("plant", "fern", "flower", "cactus", "terrarium")):
            return PALETTES["leaf"]
        if _contains_any(token, ("lamp", "orb", "neon", "server", "console", "cooler", "vending")):
            return PALETTES["storm"]
        if _contains_any(token, ("banner", "poster", "plaque", "trophy", "garland")):
            return PALETTES["brass"]
        if _contains_any(token, ("board", "frame", "bookshelf", "pizza", "blueprint")):
            return PALETTES["parchment"]
        return PALETTES["neutral"]

    if category == "floors":
        if _contains_any(token, ("parquet", "wood", "checker")):
            return PALETTES["parchment"]
        if _contains_any(token, ("carpet",)):
            return PALETTES["memory"]
        return PALETTES["neutral"]

    if category == "walls":
        if _contains_any(token, ("window",)):
            return PALETTES["storm"]
        if _contains_any(token, ("paper",)):
            return PALETTES["memory"]
        if _contains_any(token, ("wood", "bookshelf")):
            return PALETTES["parchment"]
        return PALETTES["neutral"]

    return PALETTES["neutral"]


def _draw_diamond(
    draw: ImageDraw.ImageDraw,
    cx: int,
    cy: int,
    radius: int,
    color: tuple[int, int, int, int],
) -> None:
    draw.polygon(
        [(cx, cy - radius), (cx + radius, cy), (cx, cy + radius), (cx - radius, cy)],
        outline=color,
    )


def _draw_starburst(
    draw: ImageDraw.ImageDraw,
    cx: int,
    cy: int,
    inner: int,
    outer: int,
    color: tuple[int, int, int, int],
) -> None:
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)):
        draw.line((cx + dx * inner, cy + dy * inner, cx + dx * outer, cy + dy * outer), fill=color, width=1)


def _contains_any(text: str, tokens: tuple[str, ...]) -> bool:
    return any(token in text for token in tokens)


def _draw_symbol(
    draw: ImageDraw.ImageDraw,
    asset_id: str,
    w: int,
    h: int,
    accent: tuple[int, int, int],
    spark: tuple[int, int, int],
) -> None:
    token = asset_id.lower()

    if _contains_any(token, ("done", "success", "approve")):
        draw.line((2, h // 2, w // 2 - 1, h - 3), fill=(*spark, 255), width=1)
        draw.line((w // 2 - 1, h - 3, w - 2, 2), fill=(*spark, 255), width=1)
        return

    if _contains_any(token, ("warning",)):
        draw.polygon([(w // 2, 1), (1, h - 2), (w - 2, h - 2)], outline=(*spark, 255), fill=(*accent, 210))
        draw.point((w // 2, h // 2), fill=(15, 15, 15, 255))
        return

    if _contains_any(token, ("error", "panic", "reject")):
        draw.line((2, 2, w - 3, h - 3), fill=(*spark, 255), width=1)
        draw.line((2, h - 3, w - 3, 2), fill=(*spark, 255), width=1)
        return

    if _contains_any(token, ("search", "research")):
        draw.ellipse((1, 1, w - 5, h - 5), outline=(*spark, 255), width=1)
        draw.line((w - 5, h - 5, w - 2, h - 2), fill=(*spark, 255), width=1)
        return

    if _contains_any(token, ("security", "lock")):
        draw.rectangle((2, h // 2, w - 3, h - 2), outline=(*spark, 255), fill=(*accent, 210))
        draw.arc((3, 1, w - 4, h // 2 + 1), 180, 360, fill=(*spark, 255), width=1)
        return

    if _contains_any(token, ("bug",)):
        draw.ellipse((3, 3, w - 4, h - 3), outline=(*spark, 255), fill=(*accent, 220))
        draw.line((w // 2, 1, w // 2, 3), fill=(*spark, 255), width=1)
        return

    if _contains_any(token, ("feature", "sparkle", "celebrating")):
        cx = w // 2
        cy = h // 2
        draw.line((cx, 1, cx, h - 2), fill=(*spark, 255), width=1)
        draw.line((1, cy, w - 2, cy), fill=(*spark, 255), width=1)
        draw.line((2, 2, w - 3, h - 3), fill=(*spark, 255), width=1)
        draw.line((2, h - 3, w - 3, 2), fill=(*spark, 255), width=1)
        return

    if _contains_any(token, ("doc", "library", "reading", "book")):
        draw.rectangle((1, 2, w // 2, h - 2), outline=(*spark, 255), fill=(*accent, 210))
        draw.rectangle((w // 2, 2, w - 2, h - 2), outline=(*spark, 255), fill=(*accent, 190))
        return

    if _contains_any(token, ("test", "infra", "factory")):
        draw.rectangle((w // 2 - 2, 2, w // 2 + 2, h - 3), outline=(*spark, 255), fill=(*accent, 210))
        draw.rectangle((w // 2 - 3, h - 4, w // 2 + 3, h - 2), fill=(*spark, 255))
        return

    if _contains_any(token, ("meeting", "presenting", "chat")):
        draw.rounded_rectangle((1, 2, w - 2, h - 4), radius=2, outline=(*spark, 255), fill=(*accent, 210))
        draw.polygon([(w // 3, h - 4), (w // 3 + 2, h - 1), (w // 3 + 4, h - 4)], fill=(*accent, 210))
        return

    # Fallback glyph
    draw.rectangle((1, 1, w - 2, h - 2), outline=(*spark, 255), fill=(*accent, 180))
    draw.line((2, h // 2, w - 3, h // 2), fill=(*spark, 255), width=1)


def _draw_floor_or_wall(
    draw: ImageDraw.ImageDraw,
    w: int,
    h: int,
    frame: int,
    base: tuple[int, int, int],
    accent: tuple[int, int, int],
    shadow: tuple[int, int, int],
) -> None:
    draw.rectangle((0, 0, w - 1, h - 1), fill=(*base, 255))
    step = 4 if min(w, h) >= 16 else 2
    for y in range(0, h, step):
        for x in range(0, w, step):
            if ((x // step) + (y // step) + frame) % 2 == 0:
                draw.rectangle((x, y, min(w - 1, x + step - 1), min(h - 1, y + step - 1)), fill=(*shadow, 255))
    draw.rectangle((0, 0, w - 1, h - 1), outline=(*accent, 255))


def _draw_furniture(
    draw: ImageDraw.ImageDraw,
    asset_id: str,
    w: int,
    h: int,
    frame: int,
    base: tuple[int, int, int],
    accent: tuple[int, int, int],
    shadow: tuple[int, int, int],
    spark: tuple[int, int, int],
) -> None:
    margin_x = max(1, w // 6)
    margin_y = max(1, h // 6)
    top = margin_y + (frame % 2)
    bottom = max(top + 1, h - 1 - margin_y)

    draw.rectangle((margin_x, top, max(margin_x + 1, w - 1 - margin_x), bottom), fill=(*base, 225), outline=(*accent, 255))

    if h >= 12:
        draw.line((margin_x, bottom, margin_x, h - 1), fill=(*shadow, 240), width=1)
        draw.line((max(margin_x + 1, w - 1 - margin_x), bottom, max(margin_x + 1, w - 1 - margin_x), h - 1), fill=(*shadow, 240), width=1)

    for x in range(margin_x, max(margin_x + 1, w - margin_x), max(2, w // 8)):
        draw.point((x, top), fill=(*spark, 255))

    token = asset_id.lower()

    if _contains_any(token, ("lamp", "orb", "neon")):
        glow_w = max(2, w // 4)
        draw.ellipse((w // 2 - glow_w // 2, 0, w // 2 + glow_w // 2, min(h - 1, glow_w)), fill=(*spark, 220))

    if _contains_any(token, ("banner", "poster", "plaque", "board")):
        bar_h = max(2, h // 4)
        draw.rectangle((max(0, margin_x - 1), 0, max(1, w - margin_x), bar_h), fill=(*accent, 220))

    if _contains_any(token, ("duck",)):
        draw.ellipse((max(0, w // 2 - 2), max(0, h // 2 - 2), min(w - 1, w // 2 + 3), min(h - 1, h // 2 + 2)), fill=(255, 220, 60, 255))


def _draw_fx(
    draw: ImageDraw.ImageDraw,
    asset_id: str,
    w: int,
    h: int,
    frame: int,
    frames: int,
    accent: tuple[int, int, int],
    spark: tuple[int, int, int],
) -> None:
    cx = w // 2
    cy = h // 2
    token = asset_id.lower()
    progress = frame / max(1, frames - 1)
    radius = max(1, int(max(2, min(w, h) // 2 - 2) * (0.35 + progress * 0.65)))

    if _contains_any(token, ("done", "sparkle", "achievement", "xp", "challenge")):
        _draw_starburst(draw, cx, cy, 1, radius, (*spark, 255))
        _draw_diamond(draw, cx, cy, max(1, radius // 2), (*accent, 210))
        for px, py in ((cx - radius, cy), (cx + radius, cy), (cx, cy - radius), (cx, cy + radius)):
            if 0 <= px < w and 0 <= py < h:
                draw.point((px, py), fill=(*spark, 255))
        return

    if _contains_any(token, ("confetti",)):
        pieces = ((1, 1), (5, 3), (9, 0), (12, 4), (3, 8), (10, 10))
        for idx, (seed_x, seed_y) in enumerate(pieces):
            px = (seed_x + frame * (1 + (idx % 2))) % w
            py = (seed_y + frame + idx) % h
            color = accent if idx % 2 == 0 else spark
            draw.rectangle((px, py, min(w - 1, px + 1), min(h - 1, py + 1)), fill=(*color, 240))
        return

    if _contains_any(token, ("handoff",)):
        left_x = 3
        right_x = w - 4
        draw.ellipse((left_x - 1, cy - 1, left_x + 1, cy + 1), fill=(*accent, 230))
        draw.ellipse((right_x - 1, cy - 1, right_x + 1, cy + 1), fill=(*accent, 230))
        draw.line((left_x + 1, cy, right_x - 1, cy), fill=(*accent, 180), width=1)
        moving_x = left_x + 2 + int((right_x - left_x - 4) * progress)
        draw.ellipse((moving_x - 1, cy - 1, moving_x + 1, cy + 1), fill=(*spark, 255))
        return

    if _contains_any(token, ("broadcast",)):
        for spread in (radius, radius + 2, radius + 4):
            draw.arc((cx - spread, cy - spread, cx + spread, cy + spread), 300, 60, fill=(*accent, 210), width=1)
        return

    if _contains_any(token, ("subagent",)):
        start_x = 3
        end_x = w - 4
        start_y = 4
        end_y = h - 5
        draw.ellipse((start_x - 1, start_y - 1, start_x + 1, start_y + 1), fill=(*accent, 230))
        draw.ellipse((end_x - 1, end_y - 1, end_x + 1, end_y + 1), fill=(*accent, 230))
        draw.line((start_x, start_y, end_x, end_y), fill=(*accent, 170), width=1)
        particle_x = start_x + int((end_x - start_x) * progress)
        particle_y = start_y + int((end_y - start_y) * progress)
        draw.ellipse((particle_x - 1, particle_y - 1, particle_x + 1, particle_y + 1), fill=(*spark, 255))
        return

    if _contains_any(token, ("memory",)):
        page_left = cx - 2
        page_top = cy - 3
        draw.rectangle((page_left, page_top, page_left + 4, page_top + 5), outline=(*accent, 220), fill=(*spark, 80))
        draw.line((page_left + 1, page_top + 2, page_left + 3, page_top + 2), fill=(*accent, 255), width=1)
        for idx in range(3):
            direction = -1 if "read" in token else 1
            px = cx + direction * (4 + idx * 3 - int(progress * 4))
            py = cy - 2 + idx * 2
            if 0 <= px < w and 0 <= py < h:
                draw.point((px, py), fill=(*spark, 240))
        return

    if _contains_any(token, ("document",)):
        travel = int((w - 8) * progress)
        left = max(1, 1 + travel)
        top = max(1, 3 + (frame % 2))
        draw.polygon(
            [(left, top + 1), (left + 3, top), (left + 5, top + 2), (left + 2, top + 3)],
            outline=(*accent, 230),
            fill=(*spark, 120),
        )
        draw.line((max(0, left - 2), top + 3, left, top + 2), fill=(*accent, 180), width=1)
        draw.line((max(0, left - 4), top + 4, left - 1, top + 3), fill=(*accent, 120), width=1)
        return

    if _contains_any(token, ("flash", "error")):
        border = 220 if frame % 2 == 0 else 120
        _draw_diamond(draw, cx, cy, radius, (*accent, border))
        draw.line((2, 2, w - 3, h - 3), fill=(*spark, 255), width=1)
        draw.line((2, h - 3, w - 3, 2), fill=(*spark, 255), width=1)
        draw.rectangle((1, 1, w - 2, h - 2), outline=(255, 124, 104, border))
        return

    if _contains_any(token, ("rain",)):
        shadow_color = (accent[0] // 2, accent[1] // 2, accent[2] // 2)
        draw.line((1, 0, 1, h - 1), fill=(*shadow_color, 220), width=1)
        draw.line((w - 2, 0, w - 2, h - 1), fill=(*shadow_color, 220), width=1)
        for x in range(3, w - 2, 3):
            y0 = (x * 2 + frame * 2) % max(1, h)
            draw.line((x, y0, x, min(h - 1, y0 + 3)), fill=(*spark, 210), width=1)
        return

    if _contains_any(token, ("spawn",)):
        _draw_diamond(draw, cx, cy, radius, (*accent, 220))
        _draw_diamond(draw, cx, cy, max(1, radius // 2), (*spark, 255))
        return

    _draw_diamond(draw, cx, cy, radius, (*accent, 220))
    for px, py in ((cx - radius, cy), (cx + radius, cy), (cx, cy - radius), (cx, cy + radius)):
        if 0 <= px < w and 0 <= py < h:
            draw.point((px, py), fill=(*spark, 220))


def _draw_ui(
    draw: ImageDraw.ImageDraw,
    asset_id: str,
    w: int,
    h: int,
    frame: int,
    base: tuple[int, int, int],
    accent: tuple[int, int, int],
    shadow: tuple[int, int, int],
    spark: tuple[int, int, int],
) -> None:
    draw.rectangle((0, 0, w - 1, h - 1), fill=(*shadow, 210), outline=(*accent, 255))

    if w >= 6 and h >= 6:
        draw.rectangle((1, 1, w - 2, h - 2), outline=(*spark, 220))

    token = asset_id.lower()
    if _contains_any(token, ("bar", "progress")):
        inner_w = max(1, w - 4)
        fill_w = max(1, int(inner_w * ((frame % 4) + 1) / 4))
        draw.rectangle((2, 2, 1 + fill_w, h - 3), fill=(*base, 240))
        return

    _draw_symbol(draw, token, w, h, accent, spark)


def _render_asset(spec: AssetSpec, target_path: Path) -> None:
    target_path.parent.mkdir(parents=True, exist_ok=True)
    base, accent, shadow, spark = _palette(spec.asset_id, spec.category)

    sprite_sheet = Image.new("RGBA", (spec.frame_w * spec.frames, spec.frame_h), (0, 0, 0, 0))

    for frame in range(spec.frames):
        frame_img = Image.new("RGBA", (spec.frame_w, spec.frame_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame_img)

        if spec.category in {"floors", "walls"}:
            _draw_floor_or_wall(draw, spec.frame_w, spec.frame_h, frame, base, accent, shadow)
        elif spec.category == "furniture":
            _draw_furniture(draw, spec.asset_id, spec.frame_w, spec.frame_h, frame, base, accent, shadow, spark)
        elif spec.category == "fx":
            _draw_fx(draw, spec.asset_id, spec.frame_w, spec.frame_h, frame, spec.frames, accent, spark)
        elif spec.category == "ui":
            _draw_ui(draw, spec.asset_id, spec.frame_w, spec.frame_h, frame, base, accent, shadow, spark)
        else:
            draw.rectangle((0, 0, spec.frame_w - 1, spec.frame_h - 1), fill=(*base, 255), outline=(*accent, 255))

        sprite_sheet.paste(frame_img, (frame * spec.frame_w, 0), frame_img)

    sprite_sheet.save(target_path, format="PNG")


def _build_specs() -> list[AssetSpec]:
    specs: list[AssetSpec] = []

    furniture_specs = [
        ("garland_led", 64, 4),
        ("desk_lamp", 16, 24),
        ("floor_lamp", 16, 28),
        ("neon_sign_blue", 32, 16),
        ("chandelier", 32, 32),
        ("window_curtain", 16, 32),
        ("fern_hanging", 16, 20),
        ("flower_vase", 16, 16),
        ("terrarium", 16, 16),
        ("bean_bag_blue", 16, 14),
        ("rug_grid", 32, 24),
        ("cushion_orange", 10, 10),
        ("pouf", 14, 12),
        ("team_banner", 16, 40),
        ("desk_pennant", 8, 12),
        ("trophy", 16, 20),
        ("cork_board", 32, 24),
        ("photo_frame", 12, 14),
        ("team_plaque", 24, 8),
        ("pizza_box", 16, 14),
        ("vending_machine", 16, 32),
        ("water_cooler", 16, 28),
        ("snack_bowl", 10, 8),
        ("retro_console", 24, 16),
        ("figurine_dev", 8, 12),
        ("poster_dark_academia", 24, 32),
        ("server_rack_mini", 16, 32),
        ("rubber_duck", 8, 8),
        ("magic_orb_pedestal", 16, 24),
        ("blueprint_wall", 24, 16),
        ("vote_board", 24, 16),
    ]
    for slug, width, height in furniture_specs:
        specs.append(
            AssetSpec(
                asset_id=f"furniture_{slug}_v01",
                category="furniture",
                filename=f"{slug}_v01.png",
                frame_w=width,
                frame_h=height,
            )
        )

    floor_specs = [
        "parquet_warm",
        "parquet_cool",
        "carpet_navy",
        "tiles_mono",
        "checker_amber",
        "wood_old",
    ]
    for slug in floor_specs:
        specs.append(
            AssetSpec(
                asset_id=f"floor_{slug}_v01",
                category="floors",
                filename=f"floor_{slug}_v01.png",
                frame_w=16,
                frame_h=16,
            )
        )

    wall_specs = [
        ("brick_dark", 16, 16),
        ("panel_wood", 16, 16),
        ("paper_arcane", 16, 16),
        ("window_night", 16, 32),
        ("bookshelf_tile", 16, 16),
    ]
    for slug, width, height in wall_specs:
        specs.append(
            AssetSpec(
                asset_id=f"wall_{slug}_v01",
                category="walls",
                filename=f"wall_{slug}_v01.png",
                frame_w=width,
                frame_h=height,
            )
        )

    fx_specs = [
        ("xp_burst", 16, 16, 6),
        ("achievement_unlock_burst", 32, 16, 6),
        ("confetti", 16, 16, 8),
        ("spawn_effect", 16, 16, 6),
        ("memory_read", 16, 16, 4),
        ("memory_write", 16, 16, 4),
        ("handoff", 16, 16, 6),
        ("error_flash", 16, 16, 2),
        ("done_sparkle", 16, 16, 8),
        ("challenge_win", 16, 16, 8),
        ("document_flying", 16, 16, 4),
        ("window_rain", 16, 16, 12),
        ("broadcast_wave", 16, 16, 6),
        ("subagent_tether_particles", 16, 16, 6),
    ]
    for slug, width, height, frames in fx_specs:
        specs.append(
            AssetSpec(
                asset_id=f"fx_{slug}_v01",
                category="fx",
                filename=f"fx_{slug}_v01.png",
                frame_w=width,
                frame_h=height,
                frames=frames,
                states="anim",
            )
        )

    ui_specs = [
        ("panel_frame", 32, 32),
        ("tooltip_frame", 32, 24),
        ("modal_frame", 48, 32),
        ("button_primary", 32, 16),
        ("button_secondary", 32, 16),
        ("progress_context", 64, 8),
        ("progress_rate_limit", 64, 8),
        ("progress_memory", 64, 8),
        ("minimap_frame", 48, 48),
        ("timeline_marker", 16, 16),
        ("timeline_tick", 8, 16),
        ("badge_success", 16, 16),
        ("badge_warning", 16, 16),
        ("badge_error", 16, 16),
        ("header_observatory", 16, 16),
    ]
    for slug, width, height in ui_specs:
        specs.append(
            AssetSpec(
                asset_id=f"ui_{slug}_v01",
                category="ui",
                filename=f"ui_{slug}_v01.png",
                frame_w=width,
                frame_h=height,
            )
        )

    state_icons = [
        "idle",
        "thinking",
        "typing",
        "reading",
        "searching",
        "executing",
        "waiting",
        "error",
        "warning",
        "done",
        "celebrating",
        "meeting",
        "presenting",
        "sleeping",
        "panic",
        "confused",
        "subagent_link",
    ]
    for state in state_icons:
        specs.append(
            AssetSpec(
                asset_id=f"ui_icon_state_{state}_v01",
                category="ui",
                filename=f"ui_icon_state_{state}_v01.png",
                frame_w=8,
                frame_h=8,
            )
        )

    task_icons = [
        "bug",
        "feature",
        "infra",
        "doc",
        "research",
        "test",
        "refactor",
        "security",
        "design",
    ]
    for task in task_icons:
        specs.append(
            AssetSpec(
                asset_id=f"ui_icon_task_{task}_v01",
                category="ui",
                filename=f"ui_icon_task_{task}_v01.png",
                frame_w=8,
                frame_h=8,
            )
        )

    room_icons = [
        "openspace_dev",
        "openspace_qa",
        "meeting_room",
        "challenge_room",
        "war_room",
        "library",
        "agent_factory",
        "retro_room",
        "corridor",
    ]
    for room in room_icons:
        specs.append(
            AssetSpec(
                asset_id=f"ui_icon_room_{room}_v01",
                category="ui",
                filename=f"ui_icon_room_{room}_v01.png",
                frame_w=8,
                frame_h=8,
            )
        )

    return specs


def _write_or_update_index(index_file: Path, specs: list[AssetSpec]) -> tuple[int, int]:
    existing_rows: list[dict[str, str]] = []
    existing_by_id: dict[str, dict[str, str]] = {}

    if index_file.exists():
        with index_file.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                asset_id = (row.get("asset_id") or "").strip()
                if not asset_id:
                    continue
                existing_rows.append(row)
                existing_by_id[asset_id] = row

    created = 0
    updated = 0

    for spec in specs:
        row = {
            "asset_id": spec.asset_id,
            "category": spec.category,
            "source_id": SOURCE_ID,
            "license": SOURCE_LICENSE,
            "relative_path": spec.relative_path,
            "frames": str(spec.frames),
            "tile_w": str(spec.frame_w),
            "tile_h": str(spec.frame_h),
            "states": spec.states,
            "author": AUTHOR,
            "notes": NOTES,
            "validated": "true",
        }

        if spec.asset_id in existing_by_id:
            existing_by_id[spec.asset_id].update(row)
            updated += 1
        else:
            existing_rows.append(row)
            created += 1

    with index_file.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=INDEX_HEADERS)
        writer.writeheader()
        for row in existing_rows:
            writer.writerow({header: row.get(header, "") for header in INDEX_HEADERS})

    return created, updated


def _generate_assets(curated_root: Path, specs: list[AssetSpec]) -> tuple[int, int]:
    created = 0
    updated = 0

    for spec in specs:
        target_file = curated_root / spec.category / spec.filename
        existed = target_file.exists()
        _render_asset(spec, target_file)
        if existed:
            updated += 1
        else:
            created += 1

    return created, updated


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a complete procedural baseline for Grimoire Game assets.")
    parser.add_argument(
        "--assets-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Path to grimoire-game-assets root.",
    )
    args = parser.parse_args()

    assets_root = args.assets_root.resolve()
    curated_root = assets_root / "10-curated"
    index_file = assets_root / "manifests" / "assets-index.csv"

    specs = _build_specs()

    generated_created, generated_updated = _generate_assets(curated_root, specs)
    index_created, index_updated = _write_or_update_index(index_file, specs)

    print(f"[complete-assets] specs: {len(specs)}")
    print(f"[complete-assets] generated-created: {generated_created}")
    print(f"[complete-assets] generated-updated: {generated_updated}")
    print(f"[complete-assets] index-created: {index_created}")
    print(f"[complete-assets] index-updated: {index_updated}")


if __name__ == "__main__":
    main()
