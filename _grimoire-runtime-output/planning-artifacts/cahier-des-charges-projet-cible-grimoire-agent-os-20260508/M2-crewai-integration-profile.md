---
title: M2 — Profil d'intégration CrewAI → Grimoire
description: Contrat d'intégration CrewAI, mapping primitives, guardrails
lot: M2
status: complete
updated: 2026-05-08
---

# M2 — Profil d'intégration CrewAI → Grimoire

## Principe directeur

CrewAI **ne remplace pas** le RuntimeKernel Grimoire. Il est une source
d'entrée externe : ses flows/tâches deviennent des `Recipe` expérimentaux
importés via `CrewAIAdapter`. La source de vérité reste le `MissionLedger`.

---

## Mapping primitives CrewAI → Grimoire

| Primitive CrewAI | Destination Grimoire | Règle |
|---|---|---|
| `Flow` | `Recipe` (expérimental, tag: `crewai`) | Import via `CrewAIAdapter.import_flow()` |
| `Task` | `RecipeStep` | `task.agent` → `step.roles` ; `task.depends_on` → description |
| `Agent` | `RecipeStep.roles` | Référence seulement — l'agent Grimoire reste distinct |
| `Crew` | `WorkflowInstance` | Instancié via `RuntimeKernel` après import |
| `expected_output` | `step.outputs` | Conservé comme déclaration d'intention |
| `output_schema` | `Recipe.output_schema` | **Obligatoire** — refus d'import si absent |
| Résultat d'exécution | `EvidenceItem` (REPORT) | Normalisé + stocké via `EvidenceService` |
| Trace d'exécution | `TraceRecord` via `TraceLedger` | Normalisé via `normalize_crewai_trace()` |

---

## Contrat d'adapter (guardrails M2)

### G1 — Output schema obligatoire

```python
recipe, report = adapter.import_flow(flow_dict)
if report.missing_output_schema:
    raise ValueError("output_schema required for CrewAI import")
```

### G2 — Pas de fermeture autonome de tâche

Les `VerificationGate` générées par `CrewAIAdapter` sont toutes en mode
`blocking=False`. Un flow CrewAI terminé atterrit en `NEEDS_VERIFICATION`,
pas en `CLOSED`. La fermeture requiert une vérification humaine ou une
politique `task_close_requires_verification`.

### G3 — CrewAI n'est pas source de vérité

| Interdit | Raison |
|---|---|
| Écrire dans le `MissionLedger` depuis un flow CrewAI | Créerait une source parallèle |
| Fermer une tâche Grimoire via callback CrewAI | Contourne la politique de vérification |
| Stocker des secrets dans `expected_output` | Champ traçable et logué |

### G4 — Trace normalisée obligatoire

```python
safe_trace = CrewAIAdapter.normalize_crewai_trace(raw_crewai_result)
trace_ledger.record(run_id=..., ..., tags=["crewai"])
```

`normalize_crewai_trace()` supprime `thoughts`, `tool_output`, `context`,
`memory` et les remplace par des digests SHA-256 (16 hex chars).

---

## Sample import (exemple de référence)

```python
from grimoire.runtime.crewai_adapter import CrewAIAdapter
from grimoire.traces.ledger import TraceLedger
from grimoire.runtime.recipes import RecipeRegistry
from pathlib import Path

trace = TraceLedger(Path(".grimoire/traces"))
adapter = CrewAIAdapter(trace_ledger=trace)

flow = {
    "name": "research-and-report",
    "version": "1.0.0",
    "output_schema": {"report": {"type": "string"}},
    "tasks": [
        {"id": "research", "name": "Research", "agent": "researcher",
         "expected_output": "findings", "output_schema": {"type": "string"}},
        {"id": "write", "name": "Write Report", "agent": "writer",
         "depends_on": ["research"], "expected_output": "report",
         "output_schema": {"type": "string"}},
    ],
}

recipe, report = adapter.import_flow(flow)
assert report.ok, f"Import failed: {report.errors}"

registry = RecipeRegistry(Path(".grimoire/recipes"))
registry.register(recipe)
print(f"Recipe {recipe.id} registered — tags: {recipe.tags}")
# → Recipe crewai.research-and-report registered — tags: ('experimental', 'crewai')
```

---

## Gate M2 — Validation

- [x] CrewAI ne crée pas de source de vérité parallèle
- [x] Output schema obligatoire (refus d'import sinon)
- [x] CrewAI runner optionnel — Grimoire RuntimeKernel reste le kernel
- [x] Traces normalisées (PII strippées/hashées)
- [x] Sample flow importé et enregistré dans RecipeRegistry

## Implémentation

| Fichier | Rôle |
|---|---|
| `grimoire/runtime/crewai_adapter.py` | `CrewAIAdapter`, `CrewAIFlow`, `CrewAITask`, `CrewAIImportReport` |
| `tests/unit/test_crewai_adapter.py` | 23 tests — import, guardrails, normalize |
