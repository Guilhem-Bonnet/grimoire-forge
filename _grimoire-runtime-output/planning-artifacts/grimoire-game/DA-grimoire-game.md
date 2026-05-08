# Direction Artistique — Grimoire Game

> Projet : **Grimoire Game** — DA et charte graphique
> Version : 1.2 — Avril 2026
> Auteurs : BMad Master + UX Designer Sally + Creative Director

---

## 1. Identité visuelle

### 1.1 Concept DA

**"Dark Cozy Magic Office"**

L'espace de travail de Grimoire Game est un bureau de nuit qui baigne dans une lumière bleue/dorée, où la technologie rencontre la magie. Comme une bibliothèque mystérieuse mais ultra-connectée : des écrans qui luisent dans l'obscurité, des plantes qui poussent entre les serveurs, des livres qui s'ouvrent seuls pour partager leur savoir.

**Références visuelles :**
- Stardew Valley (chaleur, pixel art 16-bit, intimité)
- Undertale (personnages expressifs, pixel art stylisé)
- Night in the Woods (ambiance nocturne, couleurs riches)
- Disco Elysium (profondeur, atmosphere bureau)
- Habbo Hotel (vue top-down isométrique, mobilier dense)

### 1.2 Mots-clés

`Cozy` · `Mysterious` · `Functional` · `Warm-in-Dark` · `Techno-Magic` · `Inhabited` · `Alive`

---

## 2. Palette de couleurs

### 2.1 Palette primaire

```css
/* Backgrounds */
--bg-deepnight:    #0A0E18;  /* Fond principal le plus sombre */
--bg-room:         #0D1117;  /* Floor de base */
--bg-wall:         #0F1525;  /* Mur sombre */
--bg-panel:        #161B22;  /* Panels UI */
--bg-card:         #21262D;  /* Cards, modals */
--bg-elevated:     #2A3140;  /* Elements surélevés */

/* Accents chauds */
--warm-gold:       #FFB800;  /* Or magique, XP, achievements */
--warm-amber:      #FF9000;  /* Lumières de lampe de bureau */
--warm-copper:     #CD7F32;  /* Mobilier, frames */

/* Accents froids */
--cool-blue:       #58A6FF;  /* UI principale, agent orch */
--cool-cyan:       #39D2C0;  /* Agent architect, tech */
--cool-purple:     #8B5CF6;  /* Magie, mémoire, bibliothèque */

/* Agents (couleurs de rôle) */
--agent-dev:       #3FB950;  /* Vert développeur */
--agent-qa:        #BC8CFF;  /* Violet QA */
--agent-pm:        #F0883E;  /* Orange PM */
--agent-arch:      #39D2C0;  /* Cyan architecte */
--agent-orch:      #58A6FF;  /* Bleu orchestrateur */
--agent-writer:    #7EE787;  /* Vert clair tech-writer */
--agent-analyst:   #D29922;  /* Ambre analyste */
--agent-sm:        #F778BA;  /* Rose SM */
--agent-ux:        #FF9EE7;  /* Rose clair UX */

/* Status */
--status-green:    #2EA043;  /* OK, done, approve */
--status-yellow:   #D29922;  /* Warning, in progress */
--status-red:      #DA3633;  /* Error, critical */
--status-blue:     #388BFD;  /* Info, working */

/* Borders */
--border-soft:     #30363D;  /* Bordures normales */
--border-accent:   #58A6FF40;/* Bordures actives (transparence) */
--border-magic:    #8B5CF640;/* Bordures magiques */
```

### 2.2 Palette de tiles

```
Floors:
  Parquet chaud:   #3D2208, #4A2E0A, #5C3A12  (3 nuances pour variation)
  Carpet bleu:     #1A2340, #1E2A4A, #223254  (gradation)
  Carrelage tech:  #1A1F2E, #1E2338, #222742
  Terre battue:    #2A1A0A, #3A2414, #4A2E1E  (factory)

Walls:
  Mur neutre:      #0F1525, #131A2E, #172038
  Fenêtre (lueur): #8BC4FF  (la lumière extérieure)
  Boiseries:       #4A2E0A, #5C3A12
  Briques:         #2A1A1A, #3A2020, #4A2828
```

---

## 3. Typographie in-game

```css
/* UI principale */
--font-ui:      'Segoe UI', system-ui, sans-serif;
--font-mono:    'SF Mono', 'Cascadia Code', Consolas, monospace;
--font-game:    'VT323', 'Press Start 2P', monospace;  /* pour les textes in-world */
  /* ⚠️ Press Start 2P: taille minimum lisible = 16px. Pour --text-game (8px): utiliser VT323 exclusivement. */
/* Tailles */
--text-xs:   10px;  /* Labels minimaux */
--text-sm:   12px;  /* Corps standard */
--text-md:   14px;  /* Titres de panel */
--text-lg:   18px;  /* Titres de section */
--text-xl:   24px;  /* Titres majeurs */
--text-game: 8px;   /* Texte pixel dans la grid (VT323 à 8px minimum) */
```

---

## 4. Iconographie

### 4.1 Icônes d'état agent

Chaque état est représenté par une icône pixel art 8×8 flottante au-dessus du personnage :

```
IDLE:          ○  (point neutre, léger pulse)
THINKING:      💭 (bulle de pensée, animation points ...)
TYPING:        ⌨  (clavier, animation touches)
READING:       📖 (livre ouvert, animation page)
SEARCHING:     🔍 (loupe, animation rotation)
EXECUTING:     ⚡ (éclair, animation clignotement)
WAITING:       ⏳ (sablier, animation grain qui coule)
ERROR:         🚨 (alerte rouge, animation pulse rapide)
WARNING:       ⚠️ (triangle jaune, clignotement lent)
DONE:          ✅ (check vert, flash 1s puis disparaît)
CELEBRATING:   🎆 (feux d'artifice, 2s animation)
MEETING:       💬 (bulles, animation alternance)
PRESENTING:    📊 (graphique, static)
SLEEPING:      💤 (ZZZ flottant, animation très lente 0.5fps)
PANIC:         ❗  (point d'exclamation rouge, animation shake 2f)
CONFUSED:      😕 (haussement épaules 2f, clignotement lent, boucle 2s)
WALKING:       (juste les pieds qui bougent, pas d'icône)
```

### 4.2 Icônes de tâches Kanban (8×8 pixels)

```
BUG:         🐛 rouge (pixel art antenne)
FEATURE:     ✨ bleu (étoile à 4 branches)
INFRA:       🏗️ orange (grue)
DOC:         📚 vert (livres)
RESEARCH:    🔬 violet (microscope)
TEST:        🧪 cyan (tube à essai)
REFACTOR:    ♻️ ambre (flèches circulaires)
SECURITY:    🔒 rouge sombre (cadenas)
DESIGN:      🎨 rose (palette)
```

### 4.3 Icônes de rooms (sur la minimap)

```
OpenSpace DEV:     💻
OpenSpace QA:      🧪  
Meeting Room:      🤝
Challenge Room:    ⚡
War Room:          🔭
Library:           📚
Agent Factory:     🔧
Retro Room:        📊
Corridor:          ───

Bouton header Observatory: 📡 (antenne satellite)
— Ouvre l'observatory.html en sidebar/panel (iframe sandbox, ADR-GAME-005)
```

### 4.4 Lien parent-enfant sous-agent

```
Tether cord (lien persistant entre agent parent et sous-agent actif):
  Style:     ligne en pointillés électriques (1px dashed, couleur de l'agent parent)
  Couleur:   teinte de l'agent parent à 60% opacité
  Animation: particules qui se déplacent de parent → enfant (1px/frame, 2fps)
  Lifetime:  visible tant que le sous-agent est ACTIF (disparait à IDLE final ou destroy)

Icône sous-agent (sprite overlay):
  Position:  coin supérieur gauche du sprite, 6×6 px
  Symbole:   🔗  (chaîne pixel art miniature)
  Tooltip:   "Sub-agent de [ParentName]"

Comportement multi-niveaux (sous-sous-agent):
  Lignes A → B → C enchaînées et visibles simultanément
  Couleur: dégradé de génération (parent bleu → enfant bleu clair → petit-enfant bleu pâle)
```

---

## 5. Animations détaillées

### 5.1 Animations de base en pixel art

**Cycle d'animation standard :**
- 16 px × 24 px par frame (personnages top-down)
- 4 directions (N/S/E/W) × 3-4 frames
- Frame rate: 8 fps pour l'animation normale, 12 fps pour run

**Descriptions frame par frame :**

```
walk_south (face caméra):
  Frame 0: pied droit avant, bras gauche avant
  Frame 1: pieds alignés, bras alignés
  Frame 2: pied gauche avant, bras droit avant

idle_breathe:
  Frame 0: position neutre
  Frame 1: légère expansion poitrine (+1px)
  Frame 2: retour position neutre
  (loop sur 2 secondes)

sit_type_fast:
  Frame 0: mains sur clavier, regard écran
  Frame 1: mains levées légèrement
  Frame 2: mains sur clavier, légère inclinaison
  Frame 3: position détendue momentanée
  (loop 4fps)

sit_think:
  Frame 0: main sur menton, regard penché
  Frame 1: regard vers le haut-gauche
  Frame 2: légère inclinaison de la tête
  (+ bulle ". . ." au-dessus, apparition progressive)

react_success:
  Frame 0: debout, bras levés
  Frame 1: saut (+4px Y)
  Frame 2: pic du saut, bras écartés
  Frame 3: descente
  Frame 4: atterrissage
  Frame 5: pose victorieuse
  (1 fois puis retour à idle)

react_error:
  Frame 0: normal
  Frame 1: se gratte la tête
  Frame 2: regard baissé
  Frame 3: geste d'incompréhension (haussement épaules)
  (+ flash rouge autour du personnage)

magic_cast (orchestrateur uniquement):
  Frame 0: bras levé, particules
  Frame 1: éclat de lumière
  Frame 2: onde qui se propage
  Frame 3: retour position normale
  (animation douce, 0.5s)

hand_raise (challenge uniquement):
  Frame 0: bras baissé
  Frame 1: bras levé à 90° (demande de parole)
  (loop jusqu'à désignation par l'orchestrateur)

react_respond (présentateur challenge):
  Frame 0: position debout, geste paume ouverte vers l'interlocuteur
  Frame 1: geste explicatif main droite (pointer ou dessiner dans l'air)
  (2 frames, durée variable)

vote_approve:
  Frame 0: bras tendu, thumb up pixel art
  Frame 1: légère oscillation du pouce (+1px)
  (hold 1s, puis retour idle)

vote_changes:
  Frame 0: main à l'horizontale, paume vers le bas
  Frame 1: légère oscillation horizontale
  (hold 1s, puis retour idle)

vote_reject:
  Frame 0: bras tendu, thumb down pixel art
  Frame 1: légère oscillation du pouce (-1px)
  (hold 1s, puis retour idle)

investigate_trace (Investigation Challenge — Debugger uniquement):
  Frame 0: agent penché avec loupe, regard vers le bas-gauche
  Frame 1: loupe se déplace (+2px X), trace data-flow visible
  Frame 2: loupe pointe une anomalie (flash sur le point ciblé)
  Frame 3: retour position, bulle "?" apparaît
  (4 fps, loop jusqu'à hypothèse validée ou escalade)

retro_present (présentation bilan hebdomadaire — orchestrateur ou SM):
  Frame 0: agent debout, pointer vers grand écran (graphique métriques visible)
  Frame 1: geste de présentation, paume ouverte vers le public
  Frame 2: regard qui balaie la salle (légère rotation de tête)
  (3 frames, 6 fps, non-loopé)

streak_celebrate (milestone shipping streak ≥ 7j consécutifs):
  Frame 0: bras levés, flamme pixel art dorée au-dessus de la tête
  Frame 1: saut (+3px Y), flamme élargie (+1px)
  Frame 2: atterrissage, flamme dorée persistante flottante
  (1 fois, puis retour idle avec flamme dorée flottante tant que streak actif)

merge_celebrate (fusion de branche validée — animation collective):
  Frame 0: agents rassemblés autour de l’écran War Room, bras levés
  Frame 1: burst de confetti pixels multi-couleurs (+5px spray, radius 20px)
  Frame 2: high-five entre agents adjacents (bras tendus vers le voisin +2px)
  Frame 3: retour positions normales, flamme dorée flottante +2s sur War Room screen
  (1 fois, non-loopé, 4fps — déclenché par événement WS BRANCH_MERGED)

sub_agent_spawn (Task tool sub-agent créé depuis l’agent parent):
  Frame 0: agent parent — éclat de lumière magenta à ses pieds (SPAWN_EFFECT réduit 0.5×)
  Frame 1: mini-sprite enfant apparaît à -2px sous le parent (scale 0.7×)
  Frame 2: mini-sprite s’écarte latéralement (+8px X) vers un bureau libre
  Frame 3: tether cord (cordon électrique, pointillés, couleur parent 60%) s’étire et persiste
  (4fps — cordon disparait quand le sous-agent termine ou est libéré)

verify_gate (avant passage carte DONE — Verification Gate):
  Frame 0: agent levè une main, tenant un écran terminal (vert fluo ASCII)
  Frame 1: icône ✅ giant (+6px) explose depuis l’écran, particules dorées
  Frame 2: agent range le terminal, pose de satisfaction
  (2fps, non-loopé — déclenché par WS VERIFICATION_GATE + résultat PASS)

parallel_dispatch (Orchestrateur lance N sous-agents en parallèle):
  Frame 0: Orchestrateur au centre, bras écartés, éclair de lumière sur les paumes
  Frame 1: N mini-arcs électriques (1 par sous-agent) jaillissent vers différents bureaux
  Frame 2: chaque arc forme un tether cord coloré (teinte unique par agent)
  Frame 3: Orchestrateur revient position bras croisés (monitoring)
  (4fps, non-loopé — tether cords persistent jusqu’à retour de tous les sous-agents)
spec_review (sous-agent vérificateur de conformité spec — 1ère étape review):
  Frame 0: agent assis, tient une feuille imprimée « SPEC » d'une main
  Frame 1: loupe sur le code (grossissement ×2), check visuel ligne par ligne
  Frame 2: coche verte ✅ apparaît sur la feuille spec (conformité validée)
  (2fps, non-loopé — déclenché par WS SPEC_REVIEW_REQUESTED)

quality_review (sous-agent vérificateur de qualité code — 2ème étape review):
  Frame 0: agent penché sur bureau, loupe bleue sur écran code
  Frame 1: annotations apparaissent (marqueurs 🔴🟡⚪ par ligne trouvée)
  Frame 2: rapport de revue posé sur le bureau (scroll JSON visible)
  (2fps, non-loopé — déclenché par WS QUALITY_REVIEW_REQUESTED)

branch_finish (agent présente les 4 options de fin de branche):
  Frame 0: agent debout devant un terminal, 4 numéros lumineux [1][2][3][4] sur l'écran
  Frame 1: agent désigne chaque option avec un pointeur, numéros clignotent
  Frame 2: agent attend, bras croisés — indicateur ⏳ sablier sur l'écran
  (1fps, boucle frames 1-2 — déclenché par WS BRANCH_FINISH_OPTIONS)

cso_audit (Security Officer scanne la salle — audit OWASP/STRIDE):
  Frame 0: agent avec badge 🔒 rouge se lève, ouvre un laptop avec logo STRIDE
  Frame 1: scan visuel (arc rouge balaie la salle de gauche à droite, 2 frames)
  Frame 2: findings apparaissent sur écran mural : grille OWASP Top 10 (✅❌ par case)
  Frame 3: agent repose le laptop, rapport imprimé dans le bac à sortie
  (2fps, non-loopé — déclenché par WS CSO_AUDIT_STARTED)```

### 5.2 Effets de particules

```
XP_BURST:      Texte « +NNN XP » doré (16 px, bold) qui flotte vers le haut (+16px en 1,5s) puis fade-out ; éclairé par 6 petites étoiles dorées (`*`) rayonnantes
ACHIEVEMENT_UNLOCK_BURST: badge achievement slide depuis le coin supérieur droit (fond violet, icône + nom), accompagné d’une explosion de 20 particules dorées rayonnant en étoile (radius 32px, 0,8s) — différent du CONFETTI
CONFETTI:      Rectangles colorés qui tombent (RGB aléatoire)
SPAWN_EFFECT:  Cercle magique qui apparaît puis disparaît (violet/or)
MEMORY_READ:   Lueur bleue qui se déplace vers l'agent
MEMORY_WRITE:  Lueur dorée qui se déplace vers la bibliothèque
HANDOFF:       Parchemin/enveloppe qui vole entre deux points (arc)
ERROR_FLASH:   Flash rouge 2 frames sur l'agent
DONE_SPARKLE:  Étoiles vertes 8 frames, radius 16px autour agent
CHALLENGE_WIN: Explosion de confettis, durée 3s
```

### 5.3 Transitions et effets UI

```
Room transition:
  Fade to black (0.3s) → Change map → Fade in (0.3s)

Panel slide:
  Transform: translateX(100%) → translateX(0) (0.25s ease-out)

Card Kanban drag:
  Scale: 1.05, shadow augmente, opacity 0.9

Modal:
  Backdrop fade in (0.2s), modal scale 0.95→1 (0.2s)

Achievement unlock:
  Badge slides from top-right (2s visible, then slides out)

Agent selected:
  Halo lumineux autour du sprite (animation pulse)
```

---

## 6. Mobilier et accessoires détaillés

### 6.1 Bureau de Developer (DEV Room)

```
Équipements DEV standard:
  - Desk dual-monitor: 2 écrans 24'' back-to-back, code affiché
  - Mechanical keyboard (pixel art, touches colorées)
  - Coffee mug (toujours plein, ☕ pixel)
  - Post-it notes (jaunes, sur l'écran)
  - Action figure Iron Man ou autre (fun detail)
  - Fan de processeur (RGB qui tourne doucement)
  - Plante cactus (résistante, comme les devs)

Spécificités selon le rôle:
  DEV senior: rack mini-serveur sur le côté
  DEV junior: pile de livres (O'Reilly style)
  Full-stack: double setup gauche/droite
```

### 6.2 Salle de Challenge

```
Layout:
  - Amphithéâtre (rangées de chaises en arc)
  - Grand écran de présentation (central, 48px wide)
  - Podium du présentateur (16px elevated)
  - Urne de vote (lors du vote: apparaît centro)
  - Timer géant (visible de partout)
  - "Results board" sur le côté (se remplit au fur et à mesure)
  
Décorations:
  - Trophy wall (achievements passés)
  - "Hall of Fame" poster (meilleures présentations)
  - "Wall of Shame" délibérément petite (failed challenges)
  - Plante verte (calming effect)
```

### 6.3 War Room (Orchestrateur)

```
Layout:
  - Bureau central circulaire (impressionnant)
  - 3 grands écrans en arc (monitoring)
  - Shelves de "agent cards" clonables
  - Console de déploiement (keyboard + switches)
  - "World map" affichant toutes les rooms (mural)
  - Ligne directe téléphone vintage (communication user)
  
Ambiance:
  - Plus sombre que les autres rooms
  - Écrans bleus dans l'obscurité
  - Clignotants rouges/verts sur les serveurs
  - Sensation de centre de commandement
```

### 6.4 Salle de Réunion (Meeting Room)

```
Layout:
  - Table ronde centrale (8 places, bois sombre, meeting_table tile)
  - Chaises rembourrées en cercle (chair_meeting)
  - Grand écran mural de présentation (16×8px, agenda ou slides)
  - Tableau blanc interactif (pencil props, 12px wide)
  - Paperboard à roulettes (bloc-notes avec notes visibles)
  - Plante haute dans un coin (palmier pixel art)

Accessoires:
  - Carafes d'eau au centre de table (3 unités)
  - Badge de porte 🤫 « En réunion » (icône do-not-disturb, visible depuis couloir)
  - Timer de réunion mural (décompte visible de partout)
  - Horloge rétro (animation tick 1fps, mur face à l'entrée)

Ambiance:
  - Murs ton gris-bleu neutre (--wall-accent)
  - Spots de conférence (lumière chaude localisée)
  - Occupée → badge 🔴 « Réunion en cours » sur la porte + lumières plus intenses
  - Vide → 2-3 chaises légèrement dérangées (trace de passage récent)
```

### 6.5 Bibliothèque / Memory Room

```
Mobilier principal:
  - Rayons court-terme (3 étagères bois clair, fiches flottantes semi-transparentes)
  - Archives long-terme (4 étagères murales hautes, livres colorés par type):
      · Rouge = code  · Bleu = documentation  · Vert = tests  · Jaune = notes
  - Bureau de consultation isolé (fauteuil en cuir, lampe de lecture chaude)
  - Skills Shelf (vitrine en verre, Power Cards posées sur présentoir)
  - Comptoir d'accueil (terminal de recherche, écran requête)

Zone Qdrant (vecteurs long-terme):
  - 3 orbes lumineuses en lévitation (teintes rouge/bleu/vert selon type)
  - Socles de cristal pixel (bases des orbes, animation scintillement 6fps)
  - Projection holographique 2D stylisée (grille vectorielle au sol, opacité 30%)

Incubateur d'idées (angle fenêtre):
  - 3 pots pixel art en rangée
  - Stades visuels : 🌱 pot + terre, 🌿 pousse verte, 🌳 arbre miniature 8px
  - Barre grow-light au-dessus (néon rose-violet 2px, animation flicker doux)

Ambiance:
  - Plus sombre que les openspaces, éclairage chaleureux et localisé
  - Badge 🤫 sur la porte (pas de SFX fort dans cette room)
  - Poussière dorée occasionnelle (particule idle 0.3× scale, 1/min)
  - Agent en recall : livre s'illumine + feuillète animation 4fps
```

### 6.6 Agent Factory

```
Équipements:
  - Forge pixel art centrale (feu bleu, animation flamme 4fps, enclume + marteau)
  - Établi configuration (outils MCP représentés comme objets physiques drag-drop)
  - Vitrine des templates RPG (cartes Warrior, Mage, Rogue, Healer exposées)
  - Machine à cloner (tube de verre vertical, bouton DEPLOY rouge clignotant)
  - Terminal sandbox (preview live de l'agent avant déploiement)
  - Rack d'inventaire tools (étagère murale, MCP servers = outils physiques empilables)

Décorations:
  - Blueprints d'agents épinglés (plans techniques pixelisés sur les murs)
  - Casque de soudure suspendu (accessoire de forge)
  - Compteur mural « Agents créés : N » (chiffre qui s'incrémente)
  - Étagère d'archives (dossiers d'agents supprimés/archivés, grisés)

Ambiance:
  - Lumière industrielle bleue + reflets orange de la forge
  - Étincelles ponctuelles au ralenti (particule SPAWN_EFFECT à 20% scale, 1/5s)
  - DEPLOY actif → forge qui s'embrase (flamme max 8px) + éclair violet 2 frames
```

### 6.7 Retro Room

```
Layout:
  - Grand écran mural principal (64px wide, tweetable summary centré)
  - Tableau de classement latéral (5 lignes agent + métriques commits/LOC)
  - Podium « 🏆 Ship of Sprint » (surélevé 2px, tapis rouge pixel art)
  - Arc de chaises pixel (8 places, disposition décontractée)
  - Tableau blanc « Start / Stop / Continue » (3 colonnes, post-its numériques)
  - Panneau de votes (post-its colorés qui s'accumulent, items ≥ 3 votes = surligné)

Décorations:
  - Flamme dorée flottante si streak global ≥ 7j (animation persistante streak_celebrate)
  - Trophy 🏆 sur socle (mis à jour à chaque retro, tâche la plus impactante)
  - Mur de photos pixelisées (commits highlights, agent selfies auto-générés)
  - Calendrier sprint (mur droit, jours cochés au feutre rouge)
  - Machine à café dans un coin (accessoire d'ambiance, cliquable pour SFX)

Ambiance:
  - Lumière tamisée, tons chauds (contraste avec l'intensité des autres rooms)
  - Son : Jazz café 85 BPM (cf. §7 sons)
  - Ouverte avec succès : confetti pastel si test ratio > 80%
  - Fermée : lumières éteintes, chaises retournées sur les tables
```

### 6.8 Worktree Room (dynamique — une room par branche git active)

```
Layout de base (généré à la création de la branche):
  - Murs tintés selon le type de branche :
      · Vert pâle (#2D6A4F à 30% opacité) → feature branch
      · Rouge pâle (#8B2020 à 30% opacité) → hotfix / bugfix branch
      · Bleu pâle (#1A2340 à 40% opacité) → release branch
      · Gris (--wall-dark + 10%)            → experiment / spike branch
  - Écran de clôture mural central (boutons [⬆️ Merge] [🔀 PR] [🗑️ Discard] [⏸ Keep])
  - Compteur d'entrée (enseigne de porte : nom de branche + « N commits · ±LOC »)
  - Bureau temporaire (desk_simple sur tréteaux, aspect provisoire)
  - Terminal de diff (affiche le dernier diff simplifié, scroll lecture seule)

Marqueurs d'identité:
  - Enseigne de porte : nom de branche court tronqué à 16 chars
  - Icône de type sur le mur d'entrée : 🌿 feature · 🔥 hotfix · 🔬 spike · 📦 release
  - Date de création + durée (« créée il y a Xj ») affichée sous l'enseigne

Ambiance:
  - Temporaire : boîtes de carton empilées dans un coin
  - Branch > 7j sans commit : murs légèrement jaunis (visual tech-debt indicator)
  - BRANCH_MERGED → animation merge_celebrate collective en War Room
  - Fermeture de room : fade-out progressif 0.3s → disparition minimap
```

### 6.9 Code Review Room

```
Layout:
  - Table de revue basse (2 terminaux face à face, spec-reviewer ↔ quality-reviewer)
  - Écran mural central (code à revoir affiché, diff colorisé)
  - Zone Stage 1 (bureau gauche, badge SPEC, loupe verte)
  - Zone Stage 2 (bureau droite, badge QUALITY, loupe bleue)
  - Tableau de findings (3 colonnes : 🔴 Critical / 🟡 Important / ⚪ Minor)
  - Imprimante post-it (sorties findings en papier, scroll JSON visible)

Accessoires:
  - Loupe pixel art sur chaque bureau (outil du reviewer)
  - Grille de critères affichée en poster mural (checklist YAGNI, perf, sécu)
  - Indicateur de stage à la porte : « STAGE 1 — En cours » / « STAGE 2 — En cours »
  - Badge YAGNI (icône ⚠️ orange, apparaît si endpoint non appelé détecté)

Ambiance:
  - Lumière froide et directionnelle (focus, concentration)
  - Critical finding → flash rouge 2 frames sur l'écran mural + badge 🔴 sur la porte
  - Review terminée sans critical → bref confetti vert clair (DONE_SPARKLE variant)
  - Porte verrouillée pendant Stage 1 : badge 🔒 « Stage 1 en cours »
```

### 6.10 Security Audit Room

```
Layout:
  - Bureau principal du CSO (desk_corner, laptop STRIDE ouvert, badge 🔒 rouge)
  - Grille OWASP Top 10 (mural gauche, 10 cases colorées ✅ ⚠️ ❌)
  - Grille STRIDE (mural droit, 6 cases : S-T-R-I-D-E avec couleurs dédiées)
  - Bac à sortie imprimante (findings imprimés, rapports empilés)
  - Zone de threat modeling (post-its noirs avec scénarios exploits, mur central)
  - Armoire des exclusions (17 faux positifs filtrés → dossier grisé visible sur étagère)

Accessoires:
  - Lampe de bureau rouge (teinte d'alerte permanente)
  - Cadenas pixel art sur la porte (icône 🔒, ouvert si salle accessible)
  - Score de confiance affiché (badge mural « Seuil : 8/10 »)
  - Écran latéral montrant le niveau de risque global (jauge colorée)

Ambiance:
  - Couleur dominante rouge sombre (#8B2020 murs, ambiance sécuritaire)
  - Lumière rouge atténuée de service (spots directionnels froids)
  - Animation cso_audit : arc de scan rouge balayant la salle de gauche à droite
  - CRITICAL finding → clignotants rouges + badge 🚫 « SHIP BLOCKED » sur l'entrée
  - Salle normalement fermée : store baissé, lumière off, badge 🔒 grisé
```

---

## 7. Sons et musique

### 7.1 Ambiance sonore

**Bande-son principale :** Lo-fi pixel art ambient
- Source: pistes libres de droits (ccMixter, Freesound)
- Style: chiptune calme, bpm 70-90, pas distractif
- Variation selon la room: War Room = plus intense, Library = plus calme

**Suggestions de styles :**
- Dev room: lo-fi hip-hop instrumental + sons de frappe clavier
- Challenge room: musique tendue, petite fanfare au résultat
- Library: ambient calme, pages qui tournent
- War room: électronique tendu, bip de monitoring

### 7.2 Sound effects

```
ui_click:     tick bref (2-3ms)
ui_hover:     très bref whoosh (1ms)
agent_spawn:  son magique montant (0.5s)
task_done:    ding satisfaisant (0.3s)
task_create:  pop léger (0.1s)
error_soft:   buzzer court (0.2s)
error_critical: alarme 3 bips (0.6s)
meeting_bell: cloche réunion (0.5s)
challenge_start: fanfare courte (1s)
challenge_approve: applaudissements (1.5s)
challenge_reject: wah-wah trombone (0.8s)
walk_footstep: pixel tap (0.05s, every 4 frames)
memory_access: page qui tourne (0.3s)
xp_gain:      chime montant (0.4s)
message_receive: notification douce (0.2s)
workflow_transition: click mécanique (0.15s)
```

---

## 8. Responsive et adaptation

### 8.1 Résolutions supportées

| Résolution | Comportement |
|---|---|
| 1920×1080 | Full experience, minimap visible |
| 1440×900 | Full experience, timeline bar réduite |
| 1280×768 | Compact: side panels se réduisent |
| 1024×768 | Mode minimal: panels en overlay |
| < 1024px | Read-only mode (pas de config) |

### 8.2 Mode plein écran

`F11` toggle fullscreen — le canvas prend tout l'écran, l'UI se réduit au minimum (juste les badges état et la minimap).

---

*Fin de la Direction Artistique — Version 1.2*
