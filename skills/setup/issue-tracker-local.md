# Issue tracker: Local Markdown

Issues and analyses live as markdown files in `docs/agents/analysis/` — one `.md` per ticket, no per-ticket directories.

Also read `docs/agents/config/workflow.md` for branch-owner and push defaults.

Tracker configuration lives in `docs/agents/config/` (`local-path` in the workflow). Analysis paths below are relative to the repository root, not to `local-path`.

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

Status: in-progress | needs-attention | ready-to-review
Kind: feature | bug | chore

## Delivery

- Ticket: [AB#4821](https://dev.azure.com/org/project/_workitems/edit/4821)
- Kind: feature | bug | chore
- Branch: `feature/4821-<short-slug>`

<analysis body sections>
```

`Ticket` is the external tracker item when there is one, written as a clickable link; without one it is the plain file number `NNN`. `Branch` reuses that same number as `feature/<ticket>-<short-slug>`.

A file in `docs/agents/analysis/` is ready. Write `Status: in-progress` only when `/implement` starts, and `Status: ready-to-review` only on a green verify, right before moving the file to `docs/agents/analysis/done/`.

No GitHub-style `ready-for-agent` analog.

## Status transitions

File in `docs/agents/analysis/` → `in-progress` → `ready-to-review` + move to `docs/agents/analysis/done/` (after verify is green).

`needs-attention` is the local equivalent of the GitHub label: the agent stopped and cannot continue without a human decision or fix (verify fail, or remaining work blocked by open `## FAQ`). It **replaces** `in-progress` in `Status:`. The file stays in `docs/agents/analysis/` — never move it to `done/`. `/implement` writes `Status: in-progress` again on resume.

If the session dies, leave `in-progress` in the **active** file — that state is resumable. Re-run `/implement` to resume.

Update `Status:` while the file is active. Append comments under `## Comments` with timestamp.

In `done/` the file reads `Status: ready-to-review`, mirroring the GitHub label.

## Skill operations

### `/analyze` — publish analysis

1. Compute next ID (scan above)
2. Choose `<slug>` from the analysis title (lowercase, hyphenated)
3. Create `docs/agents/analysis/NNN-<slug>.md` (no Status line yet)
4. Include `## Delivery` with Ticket, Kind and branch `feature/<ticket>-<short-slug>` (ticket falls back to `NNN`)

### `/implement` — fetch by number or slug

| Operation | Action |
|-----------|--------|
| Fetch analysis | `docs/agents/analysis/NNN-<slug>.md` |
| Set in-progress | Write `Status: in-progress` (also on resume from `needs-attention`) |
| Blocked by open FAQ | Write `Status: needs-attention` |
| Update Acceptance checkboxes | Check off items in `## Acceptance` |
| Comment | Append under `## Comments` (brief interruption/blocker note when needed — not per part) |

`/implement 001`, `/implement #1`, or `/implement <slug>` resolve the same way. If the only match is under `done/`, **stop**.

### `/verify` — comment on the analysis only

**Green:**

1. Append verified SHA, local gate results, push/CI outcome and PR URLs when applicable under `## Comments`. Human-owned completion does not require a PR; `push: never` or a session no-push instruction permits a locally verified delivery
2. Write `Status: ready-to-review`, then `mkdir -p docs/agents/analysis/done` and `mv` the file there

**Fail:** write `Status: needs-attention` and append what failed, what was tried, what remains (and draft PR URLs if any) under `## Comments`. Leave the file in the active folder. Do not move to `done/`.

## When a skill says "publish to the issue tracker"

Create `docs/agents/analysis/NNN-<slug>.md`. Allocate next ID first.

## When a skill says "fetch the relevant ticket"

Read the active file (or the path the user passed). Do not treat `done/` as implementable.
