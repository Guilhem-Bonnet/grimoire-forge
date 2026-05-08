# UX Audit — Switchboard v1 (Grimoire-adapté)

- **Contexte** : fork de `TentacleOpera/switchboard` embarqué dans le cockpit via iframe `?mode=mission-board` + direct `/switchboard/*.html`.
- **État après harmonisation DA v1** : palette Grimoire (`#0B0C0E` / `#FF6B3D`), typographie Geist, FX ambient + grid mask, badges Grimoire (room / agent / provenance / trust) injectés sur les cartes.
- **Preuves runtime** : `daLinkFound=true`, `accent=#FF6B3D`, `79 badges Grimoire rendus sur 37 cartes`, `0 erreur console`.

## 1. Forces

1. **Densité fonctionnelle élevée** — 9 colonnes (CREATED → SHIP GATE → COMPLETED), AUTOBAN strip, mini-map, 15 icônes pixel Sci-Fi. Le contenu métier de Switchboard est préservé intégralement.
2. **Charte Grimoire appliquée** — fond, accent, typographie, FX ambient radial, mask grid, scrollbars. Non-invasif (override par variables CSS).
3. **Extensions Grimoire visibles** — badges `▣ INTAKE`, `◆ ARCHITECT`, `⚠ ATTRIB?`, `◆ DIVERGED` apparaissent en pied de carte quand les cartes portent les métadonnées correspondantes.

## 2. Points à améliorer (prioritisés)

| # | Severité | Problème | Recommandation |
|---|---|---|---|
| 1 | **HIGH** | La view switcher overlay (top-right KANBAN/SETUP/IMPL/REVIEW) couvre le `refresh` natif de Switchboard quand le viewport est étroit | Migrer vers la header-bar Switchboard ou conditionner au breakpoint `>1400px` |
| 2 | **HIGH** | Les badges Grimoire s'accumulent (4 badges × 37 cartes) et peuvent surcharger visuellement en mode dense | Limite à 2 badges prioritaires (trust+provenance si non-clean, sinon room+agent), les autres en tooltip |
| 3 | **MED** | Les couleurs Switchboard upstream (rouge `#da3633`, jaune `#d29922`) ne sont pas harmonisées avec la palette sémantique Grimoire (`#FF5B5B`, `#FFB84D`, `#73C991`) | Ajouter `--accent-red`, `--accent-orange` aux overrides |
| 4 | **MED** | `#3ddbd9` résiduel dans quelques text-shadows et borders inline (seeds Switchboard originale) | Passer le kanban.html au `sed` pour substituer `#3ddbd9` → `var(--accent-teal)` (qui est désormais #FF6B3D) |
| 5 | **MED** | Le `controls-strip` (barre secondaire) a un fond quasi identique au header → faible hiérarchie | Augmenter le contraste `--panel-bg2` ou ajouter un séparateur accent left-border |
| 6 | **LOW** | Les transitions de cards (180ms) sont appliquées avec `!important` et overrides les animations d'erreur upstream | Retirer `!important` sur `transition` et cibler uniquement `.kanban-card` |
| 7 | **LOW** | Absence d'indicateur de chargement quand le shim remonte les seeds | Skeleton column pendant `~200ms` au premier paint |
| 8 | **LOW** | Le switcher top-right dépasse le header Switchboard quand un workspace trop long est affiché | `max-width: 40vw` + ellipsis sur `.workspace-select` |

## 3. Alignements conceptuels Grimoire à pousser

- **Ship Gate** : la colonne custom Grimoire a la même largeur que les autres → donner un traitement "gate" (fond gradient orange, badge ⚡) pour la distinguer visuellement.
- **Rooms → colonnes virtuelles** : filtre "par room" (intake-desk / war-room / workshop / branch-finisher / seance-archive / watchtower) via le `settings-strip`, en complément des rôles.
- **Trust status bloquant** : un card `trustStatus: blocked` devrait geler le drag-and-drop et afficher un overlay `BLOCKED BY PROVENANCE`.
- **Party mode hook** : bouton dans le header qui lance un debate view (pce-room) quand plusieurs agents partagent un card.

## 4. Scope 3 — deferred

- Dispatch réel via extension VSIX (terminal.sendText, clipboard, real agent spawn).
- Sync bidirectionnel avec `_grimoire-runtime-output/GRIMOIRE_TRACE.jsonl`.
- Persistance multi-workspace (aujourd'hui `localStorage` uniquement).

## 5. Artefacts

- CSS overlay : [grimoire-kit/apps/grimoire-game/public/switchboard/grimoire-da.css](../../grimoire-kit/apps/grimoire-game/public/switchboard/grimoire-da.css)
- Shim/dispatcher : [grimoire-kit/apps/grimoire-game/public/switchboard/grimoire-shim.js](../../grimoire-kit/apps/grimoire-game/public/switchboard/grimoire-shim.js)
- Embed iframe : [grimoire-kit/apps/grimoire-game/app/main.ts](../../grimoire-kit/apps/grimoire-game/app/main.ts#L1792)

## 6. URLs

| Surface | URL |
|---|---|
| Cockpit Mission Board (iframe) | http://127.0.0.1:4175/?mode=mission-board |
| Switchboard Kanban direct | http://127.0.0.1:4175/switchboard/kanban.html |
| Switchboard Setup | http://127.0.0.1:4175/switchboard/setup.html |
| Switchboard Implementation | http://127.0.0.1:4175/switchboard/implementation.html |
| Switchboard Review | http://127.0.0.1:4175/switchboard/review.html |
