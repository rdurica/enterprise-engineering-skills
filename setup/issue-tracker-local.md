# Issue tracker: Local Markdown

Issues and analyses live as markdown files in `.scratch/analysis/` — one `.md` per ticket, no per-ticket directories.

Also read `docs/agents/workflow.md` for branch-owner and push defaults.

## Layout

```
.scratch/analysis/
├── 001-<slug>.md
├── 002-<slug>.md
└── done/
    └── 001-<slug>.md
```

IDs are three digits, unique across **`.scratch/analysis/`** and **`.scratch/analysis/done/`**. Never reuse. `001` already in either ⇒ next is `002`.

Bugs are the same files with `Kind: bug` — no separate `bugs/` folder.

## Next ID

Scan leading `NNN` from files:

- `.scratch/analysis/NNN-*.md`
- `.scratch/analysis/done/NNN-*.md`

Next ID = `max(found) + 1`, or `001` if none. Pad to three digits.

## File format

```markdown
# Analysis: <title>

Status: in-progress | needs-attention
Kind: feature | bug | chore

## Delivery

- Kind: feature | bug | chore
- Branch: `feature/analysis-NNN-<short-slug>`
- Branch owner: agent | human
- Push: finalize | never

<analysis body sections>
```

A file in `.scratch/analysis/` is ready. Write `Status: in-progress` only when `/implement` starts. Do **not** write `ready-to-review`. Terminal state is the path under `.scratch/analysis/done/`.

No GitHub-style `ready-for-agent` analog.

## Status transitions

File in `.scratch/analysis/` → `in-progress` → move to `.scratch/analysis/done/` (after verify is green).

`needs-attention` is the local equivalent of the GitHub label: the agent stopped and cannot continue without a human decision or fix (verify fail, or remaining work blocked by open `## FAQ`). It **replaces** `in-progress` in `Status:`. The file stays in `.scratch/analysis/` — never move it to `done/`. `/implement` writes `Status: in-progress` again on resume.

If the session dies, leave `in-progress` in the **active** file — that state is resumable. Re-run `/implement` to resume.

Update `Status:` while the file is active. Append comments under `## Comments` with timestamp.

After the move: leave `Status: in-progress`. Do not add `ready-to-review`.

## Skill operations

### `/analyze` — publish analysis

1. Compute next ID (scan above)
2. Choose `<slug>` from the analysis title (lowercase, hyphenated)
3. Create `.scratch/analysis/NNN-<slug>.md` (no Status line yet)
4. Include `## Delivery` with Kind, `feature/analysis-NNN-<short-slug>`, and branch-owner/push from `docs/agents/workflow.md`

### `/implement` — fetch by number or slug

| Operation | Action |
|-----------|--------|
| Fetch analysis | `.scratch/analysis/NNN-<slug>.md` |
| Set in-progress | Write `Status: in-progress` (also on resume from `needs-attention`) |
| Blocked by open FAQ | Write `Status: needs-attention` |
| Update Acceptance checkboxes | Check off items in `## Acceptance` |
| Comment | Append under `## Comments` (session death only — not per part) |

`/implement 001`, `/implement #1`, or `/implement <slug>` resolve the same way. If the only match is under `done/`, **stop**.

### `/verify` — comment on the analysis only

**Green:**

1. Append PR URLs (or “local verify green — user should push”) under `## Comments`
2. `mkdir -p .scratch/analysis/done` and `mv` the file there. Leave Status as `in-progress`

**Fail:** write `Status: needs-attention` and append what failed, what was tried, what remains (and draft PR URLs if any) under `## Comments`. Leave the file in the active folder. Do not move to `done/`.

## When a skill says "publish to the issue tracker"

Create `.scratch/analysis/NNN-<slug>.md`. Allocate next ID first.

## When a skill says "fetch the relevant ticket"

Read the active file (or the path the user passed). Do not treat `done/` as implementable.
