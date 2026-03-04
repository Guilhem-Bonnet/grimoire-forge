# bmad-custom — Meta-Projet

> Workspace dédié à **l'amélioration de bmad-custom-kit**, piloté par le kit lui-même.

## Modèle Dual-Workspace

Ce projet utilise une architecture à **2 espaces de travail séparés** :

```
bmad-custom/              ← CE REPO — Meta-Projet (usage "client")
├── _bmad/                  BMAD installé (instance de travail)
├── _bmad-output/           Artefacts de planification du kit
├── docs/                   Documentation de la roadmap du kit
└── .github/                Instructions Copilot mode "client"

bmad-custom-kit/          ← REPO SÉPARÉ — Le Produit (développement)
├── framework/              Code source du framework
├── archetypes/             Archetypes de projets
├── tests/                  Tests du kit
└── .github/                Instructions Copilot mode "dev"
```

### Pourquoi 2 workspaces ?

1. **Séparation de contexte Copilot** — Chaque workspace a ses propres `copilot-instructions.md`. Quand on travaille ici, Copilot est en mode "utilisateur du kit". Quand on travaille dans `bmad-custom-kit/`, Copilot est en mode "développeur du kit".

2. **Boucle récursive d'auto-amélioration** — Le kit s'utilise lui-même pour planifier ses propres évolutions :
   - **Planifier** ici → PRD, stories, specs (dans `_bmad-output/`)
   - **Implémenter** dans `bmad-custom-kit/`
   - **Réinstaller** ici → `bmad-init.sh` pour tester les changements
   - **Valider** ici → vérifier que l'amélioration fonctionne en conditions réelles
   - **Boucler** → nouvelles frictions → nouvelles améliorations

3. **Dogfooding permanent** — Chaque utilisation du kit dans ce workspace fait remonter des améliorations vers le produit.

## Flux de travail

### Mettre à jour l'installation BMAD depuis le kit local

```bash
# Depuis la racine de ce repo
cd /chemin/vers/bmad-custom
/chemin/vers/bmad-custom-kit/bmad-init.sh install \
  --name "bmad-custom" --user "Guilhem" --lang "Français"
```

### Cycle d'amélioration

```
  ┌──────────────────────────────────────────────────────┐
  │               LA BOUCLE RÉCURSIVE                    │
  │                                                      │
  │   ┌────────────┐   installe   ┌────────────────┐    │
  │   │ Kit (dev)  ├─────────────►│ Meta-Projet    │    │
  │   │ v2.X      │              │ (utilisation)  │    │
  │   └─────▲──────┘              └───────┬────────┘    │
  │         │                             │              │
  │         │   PRD / stories / specs     │              │
  │         │   générés PAR le kit        │              │
  │         └─────────────────────────────┘              │
  │                                                      │
  │   Chaque amélioration rend le cycle suivant          │
  │   PLUS EFFICACE → effet composé                      │
  └──────────────────────────────────────────────────────┘
```

## Contenu des artefacts

- `_bmad-output/planning-artifacts/` — PRD, plans d'innovation, validations
- `_bmad-output/implementation-artifacts/` — Specs techniques, stories prêtes
- `_bmad-output/bmb-creations/` — Agents/workflows créés via le module BMB
- `docs/` — Roadmap, ADR, notes de design du kit
