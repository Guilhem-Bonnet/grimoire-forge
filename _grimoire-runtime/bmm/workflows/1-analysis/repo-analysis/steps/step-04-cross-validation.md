# Step 04 — Cross-validation CVTL (automatique)

## MANDATORY EXECUTION RULES (READ FIRST):

- 📖 CRITICAL: Lire ce fichier EN ENTIER avant toute action
- 🛑 OBJECTIF : Valider les outputs des steps 02 et 03 par raisonnement indépendant
- 🔒 CE STEP EST UNE GATE BLOQUANTE : les conclusions non validées NE PEUVENT PAS passer à step-05
- ⚡ Ce step s'exécute en mode `deep_reasoning` (CVTL requis — voir model-routing.yaml)
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`

## EXECUTION PROTOCOLS:

- Relire la fiche contextuelle `_memory/repo-contexts/{repo_name}.md` AVANT de valider
- Challenger chaque affirmation majeure des steps 02 et 03
- Produire un verdict PASS / FAIL / PARTIAL avec justification
- Si FAIL ou PARTIAL : décrire les corrections requises avant de continuer
- Attendre [C] avant de passer à step-05

## CONTEXT BOUNDARIES:

**ZONE 1 — CRITIQUE** :
```
OBJECTIF : Valider indépendamment les outputs des analyses structurelle et sémantique de {repo_name}
CONTRAINTE ABSOLUE : Raisonner indépendamment — ne pas simplement approuver les analyses précédentes
FORMAT DE SORTIE : Verdict PASS|FAIL|PARTIAL + liste de findings + corrections requises
RAPPEL OBJECTIF GLOBAL : {analysis_objective}
```

## ACCUSÉ DE RÉCEPTION OBLIGATOIRE:

```
✅ COMPRIS :
- Objectif : valider les outputs de step-02 et step-03 de façon indépendante
- Contrainte : raisonnement critique, pas d'approbation automatique
- Je vais relire : la fiche contextuelle + les fichiers cités comme sources
```

## YOUR TASK:

### 1. Relire la fiche contextuelle

Charger `{project-root}/_grimoire-runtime/_memory/repo-contexts/{repo_name}.md` en entier.

Identifier les affirmations clés à valider (extraire de la fiche) :
- Affirmations architecturales (step-02)
- Risques structurels signalés (step-02)
- Domaines métier identifiés (step-03)
- Anti-patterns signalés (step-03)
- Verdict d'alignement objectif (step-03)

### 2. Cross-validation des affirmations architecturales

Pour chaque affirmation architecturale majeure de step-02 :

**Protocole de validation** :
1. Aller lire le fichier source cité
2. Vérifier que le fichier prouve réellement ce qui est affirmé
3. Chercher des contre-exemples dans le même repo

**Format verdict par affirmation** :
```
Affirmation : "{claim}"
Source citée : {file}:{line}
Verdict : CONFIRMÉE | INFIRMÉE | PARTIELLE
Justification : {evidence_or_counterevidence}
Correction requise : {correction_if_partial_or_false}
```

### 3. Cross-validation des risques signalés

Pour chaque risque de sévérité HIGH signalé en step-02 et step-03 :

```
Risque : {risk_description}
Source : {file}:{line}
Verdict : CONFIRMÉ | FAUX POSITIF | SOUS-ESTIMÉ | SUR-ESTIMÉ
Sévérité réévaluée : {low|med|high|critical}
Justification : {evidence}
```

### 4. Détection des hallucinations

Chercher explicitement :
- Fichiers cités qui n'existent pas dans `{file_tree}`
- Lignes citées hors des bornes des fichiers
- Patterns affirmés sans fichier source
- Contradictions internes entre step-02 et step-03

Pour chaque hallucination détectée :
```
🚨 HALLUCINATION : {description}
- Affirmation : "{claim}"
- Problème : {file_does_not_exist|line_out_of_bounds|no_source|contradiction}
- Correction : {what_to_do}
```

### 5. Vérification de l'alignement objectif

Évaluer : les analyses répondent-elles à `{analysis_objective}` ?

```
Alignement avec "{analysis_objective}" :
- Couverture : {complete|partial|missing}
- Éléments manquants : {list_if_any}
- Éléments hors-scope : {list_if_any}
```

### 5b. Consensus via swarm-consensus.py (si divergence détectée)

Si step-02 et step-03 produisent des claims contradictoires sur un élément critique :

```bash
python3 {project-root}/grimoire-kit/framework/tools/swarm-consensus.py \
  vote \
  --topic "{claim_en_question}" \
  --votes '{"structural_analysis": true_or_false, "semantic_analysis": true_or_false}' \
  --mode MAJORITY \
  --json
```

- `true` = l'analyse considère le claim comme valide
- `false` = l'analyse considère le claim comme invalide/exagéré
- Résultat JSON : `{"consensus": true/false, "ratio": 0.0-1.0, "mode": "MAJORITY"}`

Si `ratio < 0.5` → claim rejeté, annoter comme "INFIRMÉ par consensus"
Si `ratio > 0.5` → claim retenu, annoter comme "CONFIRMÉ par consensus"

### 6. Verdict global et décision de continuation

**PASS** : < 2 findings mineurs, 0 hallucination, alignement complet ou partiel acceptable
→ Passer à step-05 adversarial review

**PARTIAL** : 2-5 findings, 0 hallucination critique, alignement partiel
→ Lister les corrections à apporter, puis continuer si l'utilisateur valide [C]

**FAIL** : ≥ 1 hallucination, ≥ 3 findings hauts, ou misalignment total
→ Retourner à step-02 avec liste des corrections obligatoires [R] Recommencer | [C] Forcer la continuation

### 7. Mettre à jour la fiche contextuelle

```markdown
## Résultats de la validation croisée

**Verdict CVTL** : {PASS|PARTIAL|FAIL}
**Affirmations validées** : {N}/{total}
**Hallucinations détectées** : {count}
**Corrections requises** : {list_if_any}
**Alignement objectif** : {complete|partial|missing}
```

## SUCCESS METRICS:

✅ Chaque affirmation majeure challengée indépendamment
✅ Hallucinations détectées et signalées
✅ Verdict global clair avec justification
✅ Fiche contextuelle mise à jour
✅ [C] continue ou [R] recommencer présenté selon verdict

## FAILURE MODES:

❌ Approuver automatiquement les analyses précédentes sans raisonnement critique
❌ Ne pas relire les fichiers sources pour vérifier les affirmations
❌ Ignorer les contradictions entre step-02 et step-03
❌ Passer PASS quand des hallucinations ont été détectées

## NEXT STEP:

Après [C] : charger `{project-root}/_grimoire-runtime/bmm/workflows/1-analysis/repo-analysis/steps/step-05-adversarial-review.md`
