# Visual Evidence Retention Policy

## Scope

This policy applies to screenshots, snapshots, and visual captures produced during visual kickoff and visual validation.

## Storage Layout

- Evidence root: `_grimoire-runtime-output/implementation-artifacts/visual-evidence/`
- Retention manifest: `_grimoire-runtime-output/implementation-artifacts/visual-evidence/retention-manifest.json`

## Mandatory Metadata Per Capture

1. `id`
2. `ticket_id`
3. `objective`
4. `source_tool`
5. `file_path`
6. `viewport` (`desktop` or `mobile` at minimum)
7. `state` (interaction state label)
8. `created_at`
9. `ttl_days`
10. `expires_at`
11. `status` (`active` or `expired`)

## Default Retention

- Default `ttl_days`: 14
- Short-living exploratory captures can use 7 days.
- Compliance or release evidence can be extended explicitly by decision log.

## Cleanup Rules

1. Keep only captures linked to the current objective or active ticket.
2. Mark entries as `expired` when `expires_at` is reached.
3. Delete expired files at regular maintenance.
4. Remove manifest entries for deleted files after one maintenance cycle.
5. Enforce minimum evidence set per ticket: 3 captures, both `desktop` and `mobile`, and at least 2 distinct states.

## Completion Gate

A visual task is not considered complete if:

- `proof-pack.md` is missing, or
- captures are stored outside the evidence root, or
- retention metadata is missing for new captures, or
- `ticket_id` is missing on any new capture, or
- `proof-pack.md` has no `## Non-regression visuelle` section with explicit pass markers.
