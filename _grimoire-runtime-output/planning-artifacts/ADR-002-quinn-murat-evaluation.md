# ADR-002 : Évaluation de la consolidation Quinn (QA) / Murat (TEA)

- **Statut** : Accepté — GARDER SÉPARÉS
- **Date** : 2026-03-10
- **Décideurs** : Revue externe + BMad Master

## Contexte

Le projet possède deux agents de test :
- **Quinn** (QA, module BMM) — QA pragmatique, test rapide
- **Murat** (TEA, module TEA) — Architecte test, stratégie complète

La question : faut-il fusionner Quinn comme "quick mode" de Murat ?

## Analyse comparative

| Critère | Quinn (QA) | Murat (TEA) |
|---------|-----------|-------------|
| **Cible** | Petits-moyens projets | Projets enterprise |
| **Approche** | 80/20, coverage first | Risk-based, depth scales with impact |
| **Temps** | Minutes | Heures |
| **Output** | Tests exécutables directement | Stratégie + tests + matrices + CI |
| **Workflows** | 1 (qa-generate-e2e-tests) | 9 (framework, ATDD, automate, design, trace, NFR, CI, review, teach) |
| **Module** | BMM (inclus par défaut) | TEA (module optionnel) |
| **Voice** | "Ship it and iterate" | "Risk score: 8.2/10" |
| **Escalation** | → Murat pour stratégie | → Winston/Bob/Amelia selon le cas |

## Décision

**Garder Quinn et Murat comme agents séparés.**

### Arguments pour la séparation

1. **Modules différents** : Quinn fait partie de BMM (toujours disponible), Murat fait partie de TEA (module optionnel). Les fusionner impliquerait soit de rendre TEA obligatoire, soit d'appauvrir Quinn.

2. **Audiences différentes** : Quinn sert les développeurs solo ou petites équipes qui veulent "juste des tests qui marchent". Murat sert les équipes enterprise avec des besoins de compliance, traçabilité, et gouvernance CI.

3. **Onboarding** : Un débutant qui lance Quinn n'a pas besoin d'être submergé par les 9 workflows test design, ATDD, NFR assessment, etc. La simplicité de Quinn a une valeur pédagogique.

4. **Escalation naturelle** : Quinn escalade déjà vers Murat dans sa persona enrichie. Le chemin `Quinn → Murat` est documenté et fonctionne comme un mode progressif.

5. **Workflows non-chevauchants** : Quinn a 1 workflow (generate-e2e-tests). Murat en a 9, aucun ne duplique celui de Quinn.

### Risques identifiés

- **Confusion utilisateur** : "Quinn ou Murat ?" → Mitigé par le prompt `welcome` de Quinn qui explique quand utiliser TEA.
- **Maintenance double** : Deux personas de "testeur" à maintenir → Impact faible, les personas sont très distinctes.

## Conséquences

1. Quinn reste dans BMM, Murat reste dans TEA
2. L'escalation Quinn → Murat est formalisée dans la persona de Quinn (déjà fait)
3. Le SOG (bmad-master) route automatiquement : demandes simples → Quinn, demandes stratégiques → Murat
4. Pas de fusion à planifier

## Score de réversibilité

**9/10** — Cette décision peut être changée à tout moment sans impact sur le code existant.
