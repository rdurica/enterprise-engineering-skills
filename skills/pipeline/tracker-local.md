# Issue tracker: Local Markdown

Issues and analyses live as markdown files in `docs/agents/analysis/` — one `.md` per ticket, no per-ticket directories.

## Layout

```
docs/agents/analysis/
├── 001-<slug>.md
├── 002-<slug>.md
└── done/
    └── 001-<slug>.md
```

IDs are three digits, unique across **`docs/agents/analysis/`** and **`docs/agents/analysis/done/`**. Never reuse. `001` already in either ⇒ next is `002`.

Bugs are the same files with `Kind: bug` — no separate `bugs/` folder.

## Next ID

Scan leading `NNN` from files:

- `docs/agents/analysis/NNN-*.md`
- `docs/agents/analysis/done/NNN-*.md`

Next ID = `max(found) + 1`, or `001` if none. Pad to three digits.

## File format

```markdown
# Analysis: <title>

Kind: feature | bug | chore

## Delivery

- Ticket: [AB#4821](https://dev.azure.com/org/project/_workitems/edit/4821)
- Kind: feature | bug | chore
- Branch: `feature/4821-<short-slug>`

<analysis body sections>
```

`Ticket` is the external tracker item when there is one, written as a clickable link; without one it is the plain file number `NNN`. `Branch` reuses that same number as `feature/<ticket>-<short-slug>`.

## State

The local tracker has **no status**. Never write a `Status:` line or track `in-progress`, `needs-attention` or `ready-to-review` in the file — those are GitHub labels only. The folder is the only state:

- `docs/agents/analysis/` — active: ready to implement, in progress, interrupted or blocked. `/implement` can always run or resume it.
- `docs/agents/analysis/done/` — verified; moved there by a green `/verify`. Not implementable.

When work stops on a blocker (verify fail, or open `## FAQ`), the file stays active and the reason goes under `## Comments` with a timestamp.

## Skill operations

### `/analyze` — publish analysis

1. Compute next ID (scan above)
2. Choose `<slug>` from the analysis title (lowercase, hyphenated)
3. Create `docs/agents/analysis/NNN-<slug>.md` (no Status line)
4. Include `## Delivery` with Ticket, Kind and branch `feature/<ticket>-<short-slug>` (ticket falls back to `NNN`)

### `/analyze-modify` — revise analysis

| Operation | Action |
|-----------|--------|
| Fetch analysis | `docs/agents/analysis/NNN-<slug>.md`, or `docs/agents/analysis/done/NNN-<slug>.md` |
| Update | Rewrite the file in place; keep ID, slug and `## Delivery` |
| Revised after verify | `mv` the file from `done/` back to `docs/agents/analysis/` and note the revision under `## Comments` as `## Revision`; for a still unchecked revision update that note instead of appending |

### `/implement` — fetch by number or slug

| Operation | Action |
|-----------|--------|
| Fetch analysis | `docs/agents/analysis/NNN-<slug>.md` |
| Blocked by open FAQ | Append the open question under `## Comments` |
| Update Acceptance checkboxes | Check off items in `## Acceptance` and the realized entries in `## Revisions` |
| Comment | Append under `## Comments` (brief interruption/blocker note when needed — not per part) |

`/implement 001`, `/implement #1`, or `/implement <slug>` resolve the same way. If the only match is under `done/`, **stop**.

### `/verify` — comment on the analysis only

**Green:**

1. Append verified SHA, local gate results, push/CI outcome and PR URLs when applicable under `## Comments`. Human-owned completion does not require a PR; `push: never` or a session no-push instruction permits a locally verified delivery
2. `mkdir -p docs/agents/analysis/done` and `mv` the file there

**Fail:** append what failed, what was tried, what remains (and draft PR URLs if any) under `## Comments`. Leave the file in the active folder. Do not move to `done/`.

### `/complete` — merge only

Runs only when the file is in `done/` and an agent-owned PR is open. It merges the PR and syncs `main`; the file stays in `done/` unchanged.

## When a skill says "publish to the issue tracker"

Create `docs/agents/analysis/NNN-<slug>.md`. Allocate next ID first.

## When a skill says "fetch the relevant ticket"

Read the active file (or the path the user passed). Do not treat `done/` as implementable.
