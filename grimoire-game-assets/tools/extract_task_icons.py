#!/usr/bin/env python3
"""
extract_task_icons.py — Découpe une feuille 3×3 d'icônes isométriques
en 9 fichiers PNG individuels, avec détourage du fond blanc et crop serré.

Usage:
    python3 tools/extract_task_icons.py [--source PATH] [--out DIR] [--version NN]
                                         [--tolerance N] [--padding N] [--dry-run]

Source par défaut : 00-intake/pixel-agents/tasks-icons-sheet.png
Output par défaut : 10-curated/ui/
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image
import numpy as np

# Mapping grille (row, col) → slug d'icône (ordre lecture, gauche→droite, haut→bas)
ICON_MAPPING: dict[tuple[int, int], str] = {
    (0, 0): "ui_icon_task_bug",
    (0, 1): "ui_icon_task_feature",
    (0, 2): "ui_icon_task_infra",
    (1, 0): "ui_icon_task_doc",
    (1, 1): "ui_icon_task_research",
    (1, 2): "ui_icon_task_security",
    (2, 0): "ui_icon_task_test",
    (2, 1): "ui_icon_task_refactor",
    (2, 2): "ui_icon_task_design",
}

DEFAULT_SOURCE = Path("00-intake/pixel-agents/tasks-icons-sheet.png")
DEFAULT_OUT = Path("10-curated/ui")
DEFAULT_SAT_THRESHOLD = 0.09   # saturation HSV max pour être considéré "fond"
DEFAULT_VAL_MIN = 0.78         # luminosité HSV min pour être considéré "fond"
DEFAULT_FADE_RANGE = 0.05      # zone de fondu pour les bords anti-aliasés
DEFAULT_PADDING = 8            # pixels de marge après crop serré


def _compute_bg_mask(rgb_f: np.ndarray, sat_thresh: float, val_min: float, fade_range: float) -> np.ndarray:
    """
    Retourne un masque float [0..1] où :
      1.0 = fond pur (→ alpha=0)
      0.0 = contenu (→ alpha=255)
    Détection basée sur la saturation HSV : le damier blanc/gris a une
    saturation quasi nulle, tandis que les éléments du dessin ont de la couleur.
    Le fondu progressif sur la zone de transition gère l'anti-aliasing.
    """
    r, g, b = rgb_f[:, :, 0], rgb_f[:, :, 1], rgb_f[:, :, 2]

    # Calcul HSV vectorisé
    cmax = np.maximum(np.maximum(r, g), b)          # Value (=luminosité)
    cmin = np.minimum(np.minimum(r, g), b)
    delta = cmax - cmin

    # Saturation (évite division par zéro sur les noirs purs)
    sat = np.where(cmax > 0, delta / cmax, 0.0)

    # Fond = peu saturé ET suffisamment clair
    # Zone de fondu : sat entre sat_thresh et sat_thresh + fade_range
    fully_bg = (sat <= sat_thresh) & (cmax >= val_min)
    in_fade  = (sat > sat_thresh) & (sat <= sat_thresh + fade_range) & (cmax >= val_min)

    mask = np.zeros(rgb_f.shape[:2], dtype=np.float32)
    mask[fully_bg] = 1.0
    # Fondu linéaire dans la zone intermédiaire
    fade_frac = (sat[in_fade] - sat_thresh) / fade_range
    mask[in_fade] = 1.0 - fade_frac

    return mask


def detoure_cell(
    cell: Image.Image,
    sat_thresh: float = DEFAULT_SAT_THRESHOLD,
    val_min: float = DEFAULT_VAL_MIN,
    fade_range: float = DEFAULT_FADE_RANGE,
    padding: int = DEFAULT_PADDING,
) -> Image.Image:
    """
    1. Calcule un masque "fond" par saturation HSV
    2. Applique le masque → fond = alpha 0, contenu = alpha 255 (avec fondu anti-aliasing)
    3. Décontamine la couleur des pixels semi-transparents : les pixels de bord AA
       ont leur RGB mélangé avec le fond blanc (bakée dans le source RGB).
       On récupère la vraie couleur par reverse-composite : color = (mixed - white*(1-a)) / a
    4. Crop serré autour du contenu
    """
    rgb = cell.convert("RGB")
    rgb_f = np.array(rgb).astype(np.float32) / 255.0

    bg_mask = _compute_bg_mask(rgb_f, sat_thresh, val_min, fade_range)

    # Alpha channel [0..1]
    alpha_f = np.clip(1.0 - bg_mask, 0.0, 1.0)

    # --- Décontamination de couleur ---
    # Pour les pixels semi-transparents, la couleur source est :
    #   color_mixed = color_real * alpha + blanc * (1 - alpha)
    # => color_real = (color_mixed - blanc * (1 - alpha)) / alpha
    # Le fond est blanc (1,1,1)
    eps = 1e-6
    safe_a = np.maximum(alpha_f, eps)[:, :, np.newaxis]           # (H,W,1)
    one_minus_a = (1.0 - alpha_f)[:, :, np.newaxis]               # (H,W,1)
    color_real = (rgb_f - one_minus_a) / safe_a
    color_real = np.clip(color_real, 0.0, 1.0)

    # Reconstruire RGBA
    rgba_arr = np.empty((*rgb_f.shape[:2], 4), dtype=np.uint8)
    rgba_arr[:, :, :3] = (color_real * 255).astype(np.uint8)
    rgba_arr[:, :, 3] = (alpha_f * 255).astype(np.uint8)

    result = Image.fromarray(rgba_arr, "RGBA")

    alpha_ch = result.split()[3]
    bbox = alpha_ch.getbbox()
    if bbox is None:
        return result

    left, top, right, bottom = bbox
    h, w = rgba_arr.shape[:2]
    left = max(0, left - padding)
    top = max(0, top - padding)
    right = min(w, right + padding)
    bottom = min(h, bottom + padding)

    return result.crop((left, top, right, bottom))


def extract_icons(
    source: Path,
    out_dir: Path,
    version: str = "v02",
    sat_thresh: float = DEFAULT_SAT_THRESHOLD,
    val_min: float = DEFAULT_VAL_MIN,
    fade_range: float = DEFAULT_FADE_RANGE,
    padding: int = DEFAULT_PADDING,
    dry_run: bool = False,
) -> list[Path]:
    """Découpe la feuille en 9 icônes, détoure le fond damier et exporte."""
    img = Image.open(source).convert("RGB")
    w, h = img.size
    cell_w = w // 3
    cell_h = h // 3

    out_dir.mkdir(parents=True, exist_ok=True)
    exported: list[Path] = []

    for (row, col), slug in sorted(ICON_MAPPING.items()):
        x0 = col * cell_w
        y0 = row * cell_h
        x1 = x0 + cell_w
        y1 = y0 + cell_h

        cell = img.crop((x0, y0, x1, y1))
        result = detoure_cell(cell, sat_thresh=sat_thresh, val_min=val_min, fade_range=fade_range, padding=padding)

        filename = f"{slug}_{version}.png"
        dest = out_dir / filename

        print(f"  [{row},{col}] {slug} → {dest}  ({result.size[0]}×{result.size[1]}px)")

        if not dry_run:
            result.save(dest, "PNG", optimize=True)
            exported.append(dest)

    return exported


def main() -> int:
    # Déterminer la racine du projet (parent du dossier tools/)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    parser = argparse.ArgumentParser(description="Découpe + détoure la feuille d'icônes tâches en fichiers individuels")
    parser.add_argument(
        "--source",
        type=Path,
        default=project_root / DEFAULT_SOURCE,
        help=f"Chemin du fichier source (défaut: {DEFAULT_SOURCE})",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=project_root / DEFAULT_OUT,
        help=f"Dossier de sortie (défaut: {DEFAULT_OUT})",
    )
    parser.add_argument(
        "--version",
        default="v02",
        help="Suffixe de version pour les fichiers PNG (défaut: v02)",
    )
    parser.add_argument(
        "--sat-thresh",
        type=float,
        default=DEFAULT_SAT_THRESHOLD,
        help=f"Saturation HSV max pour le fond (défaut: {DEFAULT_SAT_THRESHOLD})",
    )
    parser.add_argument(
        "--val-min",
        type=float,
        default=DEFAULT_VAL_MIN,
        help=f"Luminosité HSV min pour le fond (défaut: {DEFAULT_VAL_MIN})",
    )
    parser.add_argument(
        "--fade-range",
        type=float,
        default=DEFAULT_FADE_RANGE,
        help=f"Zone de fondu anti-aliasing saturation (défaut: {DEFAULT_FADE_RANGE})",
    )
    parser.add_argument(
        "--padding",
        type=int,
        default=DEFAULT_PADDING,
        help=f"Marge en pixels après crop serré (défaut: {DEFAULT_PADDING})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Afficher ce qui serait fait sans écrire les fichiers",
    )
    args = parser.parse_args()

    if not args.source.exists():
        print(f"❌  Fichier source introuvable : {args.source}", file=sys.stderr)
        print(f"    → Place l'image dans {project_root / DEFAULT_SOURCE}", file=sys.stderr)
        return 1

    print(f"📦  Source : {args.source}  ({Image.open(args.source).size})")
    print(f"📁  Sortie : {args.out}")
    print(f"🏷️   Version : {args.version}  |  sat_thresh={args.sat_thresh}  val_min={args.val_min}  padding={args.padding}px")
    if args.dry_run:
        print("🔍  Mode dry-run — aucun fichier écrit\n")
    else:
        print()

    exported = extract_icons(
        args.source,
        args.out,
        version=args.version,
        sat_thresh=args.sat_thresh,
        val_min=args.val_min,
        fade_range=args.fade_range,
        padding=args.padding,
        dry_run=args.dry_run,
    )

    if not args.dry_run:
        print(f"\n✅  {len(exported)} icônes détourées et exportées dans {args.out}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
