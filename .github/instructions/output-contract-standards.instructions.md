---
description: "Contrats de sortie standards par type de tâche. Déclare le format attendu avant de produire."
applyTo: "**"
created: "2026-05-08"
---

# Output Contract Standards

<!-- SEVERITY: MUST — ZONE CRITIQUE ≤ 60 tokens -->
## Règles critiques

1. **Déclare le format de sortie** avant de produire quoi que ce soit de substantiel.
2. **Respecte le contrat de l'agent actif** (`<output_preferences>` de son persona).
3. **Ne dépasse jamais les limites** de longueur définies ci-dessous sans justification explicite.

---

<!-- SEVERITY: MUST -->
## Contrats par type de tâche

### Code / Implémentation

<!-- TOKENS: ~40 -->
| Champ | Requis | Format | Limite |
| --- | --- | --- | --- |
| Fichiers modifiés | OUI | `path:line` liste | 10 items max |
| Tests | OUI | count passés / count total | 1 ligne |
| Résumé du changement | OUI | 1-2 phrases | 40 mots |
| Effets de bord | SHOULD | Bullet list | 3 items max |

**Ne pas inclure** : prose d'explication du code, docstrings non demandées, commentaires inline sauf WHY non-évident.

---

### Architecture / Analyse / ADR

<!-- TOKENS: ~40 -->
| Champ | Requis | Format | Limite |
| --- | --- | --- | --- |
| Contexte | OUI | 2-3 phrases | 60 mots |
| Options évaluées | OUI | Table (option \| avantages \| inconvénients) | 2-4 lignes |
| Décision | OUI | **Gras**, 1 phrase | 20 mots |
| Conséquences | OUI | Bullet list | 5 items max |
| Réversibilité | SHOULD | Score L1-L4 + justification | 1 ligne |

---

### Documentation / Tech Writing

<!-- TOKENS: ~30 -->
| Champ | Requis | Format | Limite |
| --- | --- | --- | --- |
| Résumé | OUI | 1 phrase | 20 mots |
| Corps | OUI | CommonMark strict | selon sujet |
| Exemples | SHOULD | Code block ou liste | ≥ 1 exemple |
| Références | MAY | Liens relatifs | — |

**Interdits** : estimations temporelles, pronoms à la première personne non-persona, titres avec numérotation manuelle.

---

### Planning / Sprint / Backlog

<!-- TOKENS: ~35 -->
| Champ | Requis | Format | Limite |
| --- | --- | --- | --- |
| Objectif | OUI | 1 phrase mesurable | 20 mots |
| Items | OUI | Table MoSCoW ou bullet | — |
| Critères d'acceptation | OUI | Bullet list vérifiable | par item |
| Out of Scope | SHOULD | Bullet list | 3 items max |

---

### Debug / Diagnostic

<!-- TOKENS: ~30 -->
| Champ | Requis | Format | Limite |
| --- | --- | --- | --- |
| Symptôme | OUI | Citation exacte du message d'erreur | verbatim |
| Root cause | OUI | 1-2 phrases + fichier:ligne si connu | — |
| Fix appliqué | OUI | diff ou description précise | — |
| Vérification | OUI | commande ou test à lancer | 1 ligne |

---

<!-- SEVERITY: SHOULD -->
## Longueurs par défaut

| Type de réponse | Cible | Maximum strict |
| --- | --- | --- |
| Réponse courte (question, status) | 2-4 phrases | 100 mots |
| Livrable code | selon tâche | pas de limite |
| Livrable doc | selon tâche | pas de limite |
| Analyse / ADR | 200-400 mots | 600 mots |
| Résumé de session | 3-5 bullets | 150 mots |

---

<!-- SEVERITY: MAY -->
## Modules adaptatifs conditionnels

<!-- WHEN: utilisateur marque niveau expert dans config -->
Saute les explications pédagogiques. Va directement au résultat, pas au cheminement.
<!-- /WHEN -->

<!-- WHEN: tâche cross-fichiers > 5 fichiers -->
Commence par un tableau récapitulatif des fichiers touchés avant tout code.
<!-- /WHEN -->

<!-- WHEN: output contient du code non-testé -->
Ajoute une section `## ⚠ Non testé` listant les cas limites à vérifier manuellement.
<!-- /WHEN -->
