# Visual Kickoff Example

## Goal

Provide a ready-to-run example for the visual orchestration kickoff flow.

## Example Input Prompt

```text
Lance un flow visuel complet pour une landing page de produit B2B SaaS.
Je veux une direction artistique claire, une UX de conversion, un logo temporaire,
des animations web utiles, et un pack d'assets 2D exportables.
```

## Mandatory Pre-brief Batch (Expected)

1. Quel est le premier geste utilisateur attendu sur la landing page?
2. Qui est l'audience principale et quel est son contexte metier?
3. Quelle ambiance visuelle veux-tu (3 adjectifs) et que faut-il eviter?
4. Quels sont les 3 blocs d'information prioritaires au premier ecran?
5. Quel role doit jouer l'animation (guider, expliquer, rassurer, celebrer)?
6. Quels livrables visuels exacts veux-tu (logo, UI, icones, assets, FX, storyboards)?
7. Quels formats de sortie sont obligatoires (png, jpg, svg, gif, css, js)?
8. Quelles contraintes techniques dois-je respecter (stack, perf, cibles device)?

## Expected Deliverables

- `visual-brief.md`
- `brand-board.md`
- `ux-map.md`
- `motion-spec.md`
- `assets-manifest.csv`
- `implementation-pack/`
- `proof-pack.md`

## Quality Gates Checklist

- Clarity: first screen makes next action explicit.
- Coherence: palette, typography, icon language, and motion align.
- Accessibility: contrast, focus, and reduced-motion fallback are explicit.
- Performance: animation complexity is bounded.
- Operability: motion supports comprehension and task progression.

## Notes

- For non-design users, questions must be reformulated in plain language with options.
- No output should be marked final before passing all visual-first gates.
