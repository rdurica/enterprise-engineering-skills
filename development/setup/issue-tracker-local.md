# Issue tracker: Local Markdown

Issues and PRDs live as markdown files in `.scratch/prd/` — one `.md` per ticket, no per-ticket directories.

Also read `docs/agents/workflow.md` for branch-owner and push defaults.

## Layout

```
.scratch/prd/
├── 001-<slug>.md
├── 002-<slug>.md
└── done/
    └── 001-<slug>.md
```

IDs are three digits, unique across **`.scratch/prd/` and `.scratch/prd/done/`**. Never reuse. `001` already in `done/` ⇒ next is `002`.

Bugs are the same files with `Kind: bug` — no separate `bugs/` folder.

Existing unnumbered `.scratch/<slug>/PRD.md` remains readable until `/verify` assigns an ID and writes `.scratch/prd/done/NNN-<slug>.md`.

## Next ID

Scan leading `NNN` from files:

- `.scratch/prd/NNN-*.md`
- `.scratch/prd/done/NNN-*.md`

Also include leftover IDs from older layouts if present (`.scratch/NNNN-*` dirs, `.scratch/bugs/`, `.scratch/done/`) so numbers never collide.

Next ID = `max(found) + 1`, or `001` if none. Pad to three digits.

## File format

```markdown
# PRD: <title>

Status: in-progress
Kind: feature | bug | chore

## Delivery

- Branch: `feature/prd-NNN-<short-slug>`
- Branch owner: agent | human
- Push: finalize | never

<prd body sections>
```

A file in `.scratch/prd/` is ready. Write `Status: in-progress` only when `/implement` starts. Do **not** write `ready-to-review`. Terminal state is the path under `.scratch/prd/done/`.

No GitHub-style `ready-for-agent` analog.

## Status transitions

File in `.scratch/prd/` → `in-progress` → move to `.scratch/prd/done/` (after verify is green).

If the session dies, leave `in-progress` in the **active** file. Re-run `/implement` to resume.

Update `Status:` while the file is active. Append comments under `## Comments` with timestamp.

After the move: leave `Status: in-progress`. Do not add `ready-to-review`.

## Skill operations

### `/to-prd` — publish PRD

1. Compute next ID (scan above)
2. Choose `<slug>` from the PRD title (lowercase, hyphenated)
3. Create `.scratch/prd/NNN-<slug>.md` (no Status line yet)
4. Include `## Delivery` with `feature/prd-NNN-<short-slug>` and branch-owner/push from `docs/agents/workflow.md`

### `/implement` — fetch by number or slug

| Operation | Action |
|-----------|--------|
| Fetch PRD | Active only: `.scratch/prd/NNN-<slug>.md` (or unnumbered `.scratch/<slug>/PRD.md`) |
| Set in-progress | Write `Status: in-progress` |
| Update AC checkboxes | Check off items in `## Acceptance criteria` |
| Comment | Append under `## Comments` (session death only — not per increment) |

`/implement 001`, `/implement #1`, or `/implement <slug>` resolve the same way. If the only match is under `.scratch/prd/done/`, **stop**.

### `/verify` — comment on the PRD only

**Green:**

1. Append PR URLs (or “local verify green — user should push”) under `## Comments`
2. If the path has no `NNN-` prefix, assign next ID
3. `mkdir -p .scratch/prd/done` and `mv` the file to `.scratch/prd/done/NNN-<slug>.md`. Leave Status as `in-progress`

**Fail:** append what failed, what was tried, what remains (and draft PR URLs if any) under `## Comments`. Leave the file in `.scratch/prd/`. Do not move to `done/`.

## When a skill says "publish to the issue tracker"

Create `.scratch/prd/NNN-<slug>.md`. Allocate next ID first.

## When a skill says "fetch the relevant ticket"

Read the active file (or the path the user passed). Do not treat `.scratch/prd/done/` as implementable.
