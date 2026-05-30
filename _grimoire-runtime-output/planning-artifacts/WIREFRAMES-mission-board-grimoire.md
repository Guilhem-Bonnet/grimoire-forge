# Wireframes — Mission Board Grimoire

> Projet : **Grimoire**
> Portee : **ecrans, rooms, drawer, first-run, etats critiques**
> Sources : [UX-MAP-mission-board-grimoire.md](./UX-MAP-mission-board-grimoire.md), [VISUAL-BRIEF-mission-board-grimoire.md](./VISUAL-BRIEF-mission-board-grimoire.md), [MOTION-SPEC-mission-board-grimoire.md](./MOTION-SPEC-mission-board-grimoire.md)

---

## 1. Regles de lecture

- Desktop d'abord ;
- une question primaire par room ;
- drawer a droite ;
- frise causale basse ;
- pas de KPI dominant la lecture.

## 2. First-run - Intake Desk

```text
+----------------------------------------------------------------------------------+
| Rooms | Mission Board | Search | Filters | Session | Proof Mode                  |
+-------+--------------------------------------------------------------------------+
| Intake|  Nouvelle task                                                            |
| War   |  [Template] Recherche  Architecture  Implementation  Incident  Document  |
| Work  |                                                                          |
| Finish|  Titre .................................................................   |
| Seance|  Description ...........................................................   |
| Watch |  Labels ...............................................................    |
|       |  Acceptance criteria                                                     |
|       |   - ..................................................................   |
|       |   - ..................................................................   |
|       |                                                                          |
|       |  [Options de ticket] v                                                   |
|       |    Severity  Dependencies  Flow hint  Evidence profile  Policy pack      |
|       |                                                                          |
|       |  [Preview qualification et routage]                                      |
|       |    Complexity: complex                                                   |
|       |    Lane: dev                                                             |
|       |    Recipe: implementation-standard                                       |
|       |    Why: type=implementation, evidence=strict                             |
|       |                                                                          |
|       |  [Creer la task] [Ajuster]                                               |
+-------+--------------------------------------------------------------------------+
| Canonical events: task.created -> task.qualified -> task.routed.preview         |
+----------------------------------------------------------------------------------+
```

## 3. War Room - Vue tactique mission

```text
+---------------------------------------------------------------------------------------------------+
| Rooms | Mission: Board Native | Bundle: Control Plane | Filters | Search | Session                |
+-------+-------------------------------------------------------------------------------------------+
| Intake| [Intake]      [Qualified]      [Assigned]       [Running]       [Review]                  |
| War   | task-041      task-042         task-043         task-044        task-045                  |
| Work  | route fix     seance query     strict gate      runtime hook     closure guard             |
| Finish| p1 complex    p1 standard       p0 strict        p1 standard      p0 strict                |
| Seance| deps:1 ev:0   deps:0 ev:1       deps:1 ev:2      deps:0 ev:1      deps:0 ev:3             |
| Watch |                                                                                           |
|       | [Verified]                      [Blocked]                               [Done]              |
|       | task-046                        task-047                                 task-001           |
|       | accept path                     stale run                               schema locked       |
+-------+---------------------------------------------------+---------------------------------------+
| Dependency loom overlay on selected card                  | Drawer                                |
| task-045 -> task-047                                      | task-047                              |
|                                                           | blocked: missing evidence             |
|                                                           | next: escalate or resolve dep         |
+---------------------------------------------------------------------------------------------------+
| Canonical events: workflow.stale.detected -> task.blocked -> mission.closure.blocked             |
+---------------------------------------------------------------------------------------------------+
```

## 4. Carte detaillee et drawer

```text
+-----------------------------------------+ +--------------------------------------+
| task-047                                | | Overview                              |
| [Ember corner] [ID] [freshness] [seal]  | | Title: Closure guard E2E             |
|                                         | | Type: implementation                  |
| Closure guard mission parent            | | Complexity: complex                   |
| Reopen when required child still open   | | Lane: dev                             |
| p0  strict  deps:1  ev:2                | | Recipe: implementation-rigorous       |
|                                         | | Why: p0 + closure guard + strict      |
| [Escalader]                             | |                                      |
+-----------------------------------------+ | Acceptance                            |
                                            | - Refuse close_mission child open      |
                                            | - Preserve evidence refs               |
                                            |                                      |
                                            | Verification                          |
                                            | state: needs_work                     |
                                            | evidence gap: missing fail case       |
                                            |                                      |
                                            | Commands                              |
                                            | [request_verification] [block_task]   |
                                            +--------------------------------------+
```

## 5. Workshop - Runs et checkpoints

```text
+------------------------------------------------------------------------------------+
| Rooms | Workshop | Lane filter | Runtime filter | Search                            |
+-------+----------------------------------------------------------------------------+
| Intake| Lane: dev                                                                  |
| War   |  task-044 [edge pulse Storm]   checkpoint 3/5   next: verify               |
| Work  |  task-045 [paused]             waiting review   last cp: recent             |
| Finish| Lane: tech-writer                                                          |
| Seance|  task-050 [idle]               no run active                                   |
| Watch |                                                                            |
+-------+------------------------------------------------------+----------------------+
| Run timeline mini-strip                                      | Drawer               |
| cp1 -> cp2 -> cp3 -> cp_due                                  | workflowInstanceId   |
|                                                              | traceId              |
|                                                              | currentStep          |
+------------------------------------------------------------------------------------+
```

## 6. Branch Finisher - Verification Queue

```text
+--------------------------------------------------------------------------------------+
| Rooms | Branch Finisher | Queue filter | Evidence mode | Session                       |
+-------+------------------------------------------------------------------------------+
| Intake| task-045  verify queued    evidence:2   policy: strict                       |
| War   | task-047  needs_work       evidence:1   gap: negative case                   |
| Work  | task-052  accepted         evidence:4   ready to close                       |
| Finish|                                                                              |
| Seance| [Selected task details]                                                       |
| Watch |  verdict: accepted                                                            |
|       |  close_task: allowed                                                           |
|       |  close_mission: denied, child task-047 still open                              |
+-------+------------------------------------------------------------------------------+
| Canonical events: verification.requested -> verification.accepted -> close denied    |
+--------------------------------------------------------------------------------------+
```

## 7. Seance Archive - Lineage inter-session

```text
+--------------------------------------------------------------------------------------+
| Rooms | Seance Archive | Mission | Session filters | As-of                           |
+-------+------------------------------------------------------------------------------+
| Intake| decision card: route override task-044                                       |
| War   | decision card: close_mission denied                                          |
| Work  | evidence card: verification pass task-052                                    |
| Finish| reopen episode: task-047 after reject                                        |
| Seance|                                                                              |
| Watch | timeline: session-a -> session-b -> session-c                                |
+-------+-------------------------------------------------------------+----------------+
| Query: who decided what, when, on which proof?                      | Drawer         |
|                                                                     | trace refs     |
|                                                                     | evidence refs  |
|                                                                     | verification   |
+--------------------------------------------------------------------------------------+
```

## 8. Watchtower - Supervision

```text
+--------------------------------------------------------------------------------------+
| Rooms | Watchtower | Severity filter | Stale only | Search                           |
+-------+------------------------------------------------------------------------------+
| Intake| task-047  stale        reason: no checkpoint recent   next: nudge           |
| War   | task-061  escalated    reason: policy deny            next: reroute         |
| Work  | task-062  quarantined  reason: suspicious output      next: manual review   |
| Finish|                                                                              |
| Seance| [Selected incident]                                                           |
| Watch |  taskId: task-062                                                             |
|       |  supervision: quarantined                                                     |
|       |  nextAction: request security review                                          |
+-------+------------------------------------------------------------------------------+
| Canonical events: workflow.stale.detected -> mission_supervision_state               |
+--------------------------------------------------------------------------------------+
```

## 9. Compact layout

```text
+----------------------------------------------------------------+
| Rooms | Mission | Filters | Search                             |
+-------+--------------------------------------------------------+
| War   | [Column tabs]                                           |
| Work  | task-045  review queued                                 |
| Watch | task-047  blocked stale                                 |
+-------+------------------------------------+-------------------+
| Selected card summary                      | Drawer sheet       |
| title, state, deps, evidence, next action  | tabbed details     |
+----------------------------------------------------------------+
```

## 10. Non-regression wireframe

- une carte reste lisible a 1x ;
- le drawer n'inonde pas le contexte ;
- la frise d'evenements ne remplace pas la room primaire ;
- la room ne ment jamais sur le statut canonique.
