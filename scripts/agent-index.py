#!/usr/bin/env python3
"""Agrège les deux piles d'agents du projet en une carte unique et vérifiable.

La Forge expose deux piles qui s'ignorent : les wrappers BMM de ``.github/agents/``
(hôte Copilot, ``handoffs:`` déclarés en frontmatter) et les agents du kit de
``.claude/agents/`` (hôte Claude Code, régénérés par ``grimoire host sync``, donc
incapables de déclarer quoi que ce soit). Les relations qui traversent la frontière
vivent dans ``_grimoire-runtime/_config/agent-bridges.yaml``.

La carte est écrite dans ``.github/copilot-instructions.md``, entre marqueurs : c'est
le seul fichier que Copilot charge nativement et que ``CLAUDE.md`` importe, donc le
seul endroit où une écriture atteint les deux piles à la fois.

Usage :
    python3 scripts/agent-index.py            # régénère le bloc
    python3 scripts/agent-index.py --check    # échoue si le bloc a dérivé
"""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass, field
from pathlib import Path

from ruamel.yaml import YAML

REPO_ROOT = Path(__file__).resolve().parent.parent
BMM_DIR = REPO_ROOT / ".github" / "agents"
KIT_DIR = REPO_ROOT / ".claude" / "agents"
BRIDGES = REPO_ROOT / "_grimoire-runtime" / "_config" / "agent-bridges.yaml"
MANIFEST = REPO_ROOT / "_grimoire-runtime" / "_config" / "agent-manifest.csv"
TARGET = REPO_ROOT / ".github" / "copilot-instructions.md"

START = "<!-- agent-index:start — généré par scripts/agent-index.py, ne pas éditer à la main -->"
END = "<!-- agent-index:end -->"

_yaml = YAML(typ="safe")


@dataclass
class Agent:
    """Un agent, tel que son fichier le déclare."""

    name: str
    pile: str
    surface: str
    persona: str
    description: str
    tools: str
    handoffs: list[str] = field(default_factory=list)
    roster: list[str] = field(default_factory=list)
    user_invocable: bool = False


def personas() -> dict[str, str]:
    """La persona ne vit que dans le manifeste BMM, jamais dans le frontmatter."""
    if not MANIFEST.is_file():
        return {}
    with MANIFEST.open(encoding="utf-8", newline="") as handle:
        return {row["name"]: row.get("displayName", "") for row in csv.DictReader(handle)}


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.lstrip().startswith("---"):
        # Les agents du kit portent un commentaire d'archétype avant le frontmatter.
        head, sep, rest = text.partition("---\n")
        if not sep:
            return {}
        text = "---\n" + rest
    body = text.split("---", 2)
    if len(body) < 3:
        return {}
    return _yaml.load(body[1]) or {}


def _as_list(value: object) -> list[str]:
    if isinstance(value, list):
        # Le master déclare ses `handoffs:` comme des suggestions VS Code
        # (label/agent/prompt), pas comme des noms d'agents. Ce n'est pas une
        # relation entre agents : on ne la met pas dans le graphe.
        return [str(v) for v in value if not isinstance(v, dict)]
    if isinstance(value, str) and value.strip():
        return [part.strip() for part in value.split(",") if part.strip()]
    return []


def _short(description: str, limit: int = 110) -> str:
    """Garde le rôle, coupe le « Use when: » qui n'a de sens que pour l'activation."""
    head = description.split("Use when:")[0].strip().rstrip(".").replace("|", "/")
    if len(head) <= limit:
        return head
    return head[:limit].rsplit(" ", 1)[0] + "…"


def _tools(tools: list[str], limit: int = 6) -> str:
    """Un orchestrateur porte la surface d'outils entière : la lister n'apprend rien."""
    if not tools:
        return "—"
    if len(tools) <= limit:
        return ", ".join(tools)
    return f"{len(tools)} outils — surface hôte complète"


def collect() -> list[Agent]:
    agents: list[Agent] = []
    known_personas = personas()
    for path in sorted(BMM_DIR.glob("*.agent.md")):
        fm = _frontmatter(path)
        if not fm.get("name"):
            continue
        agents.append(
            Agent(
                name=str(fm["name"]),
                pile="bmm",
                surface="Copilot",
                persona=known_personas.get(str(fm["name"]), ""),
                description=_short(str(fm.get("description", ""))),
                tools=_tools(_as_list(fm.get("tools"))),
                handoffs=_as_list(fm.get("handoffs")),
                roster=_as_list(fm.get("agents")),
                user_invocable=bool(fm.get("user-invocable", False)),
            )
        )
    for path in sorted(KIT_DIR.glob("*.md")):
        fm = _frontmatter(path)
        if not fm.get("name"):
            continue
        agents.append(
            Agent(
                name=str(fm["name"]),
                pile="kit",
                surface="Claude Code",
                persona="",
                description=_short(str(fm.get("description", ""))),
                tools=_tools(_as_list(fm.get("tools"))),
            )
        )
    return agents


def load_bridges() -> dict:
    if not BRIDGES.is_file():
        return {"bridges": [], "duplicates": []}
    return _yaml.load(BRIDGES.read_text(encoding="utf-8")) or {}


def verify(agents: list[Agent], bridges: dict) -> list[str]:
    """Retourne les incohérences — un handoff ou un pont sans destinataire réel."""
    errors: list[str] = []
    by_pile: dict[str, set[str]] = {"bmm": set(), "kit": set()}
    for agent in agents:
        by_pile[agent.pile].add(agent.name)
    known = by_pile["bmm"] | by_pile["kit"]

    for agent in agents:
        for target in agent.handoffs:
            if target not in by_pile[agent.pile]:
                errors.append(f"{agent.name} ({agent.pile}) passe la main à '{target}', qui n'existe pas dans sa pile")
        for target in agent.roster:
            if target not in known:
                errors.append(f"{agent.name} dispatche vers '{target}', qui n'existe dans aucune pile")
    for bridge in bridges.get("bridges", []):
        if bridge["from"] not in known:
            errors.append(f"pont depuis '{bridge['from']}', qui n'existe dans aucune pile")
        for target in bridge.get("to", []):
            if target not in known:
                errors.append(f"pont de '{bridge['from']}' vers '{target}', qui n'existe dans aucune pile")
    for dup in bridges.get("duplicates", []):
        for name, pile in zip(dup["names"], dup["piles"], strict=True):
            if name not in by_pile.get(pile, set()):
                errors.append(f"doublon déclaré sur '{name}' en pile {pile}, introuvable")
    return errors


def _mermaid(agents: list[Agent], bridges: dict) -> list[str]:
    lines = ["```mermaid", "graph LR"]
    linked = {a.name for a in agents if a.handoffs}
    linked |= {t for a in agents for t in a.handoffs}
    for agent in agents:
        if agent.handoffs:
            for target in agent.handoffs:
                lines.append(f"  {agent.name} --> {target}")
    for bridge in bridges.get("bridges", []):
        for target in bridge.get("to", []):
            lines.append(f"  {bridge['from']} -.pont.-> {target}")
            linked.add(bridge["from"])
            linked.add(target)
    # Un orchestrateur n'est pas isolé : son roster le relie à tout le monde.
    # Tracer ses arêtes noierait le graphe, on le pose comme nœud central.
    for agent in agents:
        if agent.roster and agent.user_invocable:
            lines.append(f"  {agent.name}[\"{agent.name} — dispatche {len(agent.roster)} agents\"]")
            linked.add(agent.name)
    isolated = sorted({a.name for a in agents} - linked)
    if isolated:
        lines.append(f"  isoles[\"activés au cas par cas, sans relation déclarée : {', '.join(isolated)}\"]")
    lines.append("```")
    return lines


def render(agents: list[Agent], bridges: dict) -> str:
    bmm = [a for a in agents if a.pile == "bmm"]
    kit = [a for a in agents if a.pile == "kit"]
    out: list[str] = [
        START,
        "",
        f"Carte générée depuis les fichiers d'agents eux-mêmes : {len(bmm)} sur la pile BMM,",
        f"{len(kit)} sur la pile kit. Régénérer avec `python3 scripts/agent-index.py`.",
        "",
        "### Pile BMM — `_grimoire-runtime/`, exposée à Copilot",
        "",
        "| Agent | Persona | Rôle | Outils | Passe la main à | Visible utilisateur |",
        "|---|---|---|---|---|---|",
    ]
    for agent in bmm:
        handoffs = ", ".join(f"`{h}`" for h in agent.handoffs) if agent.handoffs else "—"
        out.append(
            f"| `{agent.name}` | {agent.persona or '—'} | {agent.description} | {agent.tools or '—'} | "
            f"{handoffs} | {'oui' if agent.user_invocable else 'non'} |"
        )
    out += [
        "",
        "### Pile kit — `_grimoire/kit/`, exposée à Claude Code",
        "",
        "Ces fichiers sont régénérés par `grimoire host sync` : ils ne peuvent pas",
        "déclarer de relation. Leurs liens vers la pile BMM sont déclarés dans",
        "`_grimoire-runtime/_config/agent-bridges.yaml`.",
        "",
        "| Agent | Rôle | Outils | Pont vers la pile BMM |",
        "|---|---|---|---|",
    ]
    bridge_map = {b["from"]: b for b in bridges.get("bridges", [])}
    for agent in kit:
        bridge = bridge_map.get(agent.name)
        link = ", ".join(f"`{t}`" for t in bridge["to"]) if bridge else "—"
        out.append(f"| `{agent.name}` | {agent.description} | {agent.tools or '—'} | {link} |")

    for agent in bmm:
        if not agent.roster or not agent.user_invocable:
            continue
        missing = sorted({a.name for a in bmm} - set(agent.roster) - {agent.name})
        out += [
            "",
            f"### Ce que `{agent.name}` sait dispatcher",
            "",
            f"Son frontmatter déclare {len(agent.roster)} agents. Les agents de la pile BMM",
            "qu'il ne nomme pas ne lui sont pas accessibles par dispatch :",
            "",
            f"- hors roster : {', '.join(f'`{m}`' for m in missing) if missing else 'aucun'}",
        ]

    duplicates = bridges.get("duplicates", [])
    if duplicates:
        out += ["", "### Doublons entre piles", "", "| Noms | Piles | Arbitrage |", "|---|---|---|"]
        for dup in duplicates:
            names = " / ".join(f"`{n}`" for n in dup["names"])
            piles = " / ".join(dup["piles"])
            out.append(f"| {names} | {piles} | {dup['resolution'].strip()} |")

    out += ["", "### Graphe des relations", ""] + _mermaid(agents, bridges) + ["", END]
    return "\n".join(out)


def splice(block: str) -> tuple[str, str]:
    text = TARGET.read_text(encoding="utf-8")
    start = text.find(START)
    end = text.find(END)
    if start == -1 or end == -1:
        raise SystemExit(f"marqueurs absents de {TARGET.relative_to(REPO_ROOT)} — ajoutez-les d'abord")
    return text, text[:start] + block + text[end + len(END) :]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="échouer si la carte a dérivé")
    args = parser.parse_args()

    agents = collect()
    bridges = load_bridges()
    errors = verify(agents, bridges)
    if errors:
        for err in errors:
            print(f"[INCOHERENT] {err}", file=sys.stderr)
        return 2

    current, updated = splice(render(agents, bridges))
    if args.check:
        if current != updated:
            print(
                "[DERIVE] la carte des agents ne correspond plus aux fichiers — "
                "lancez `python3 scripts/agent-index.py`",
                file=sys.stderr,
            )
            return 1
        print(f"[OK] carte à jour — {len(agents)} agents, {len(bridges.get('bridges', []))} ponts")
        return 0

    if current == updated:
        print(f"[OK] carte déjà à jour — {len(agents)} agents")
        return 0
    TARGET.write_text(updated, encoding="utf-8")
    print(f"[ECRIT] carte régénérée — {len(agents)} agents, {len(bridges.get('bridges', []))} ponts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
