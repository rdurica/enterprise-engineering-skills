# Issue tracker: Local Markdown

Issues and PRDs live as markdown files in `.scratch/`.

Also read `docs/agents/workflow.md` for branch-owner and push defaults.

## Layout

```
.scratch/<feature-slug>/
├── PRD.md
└── issues/
    ├── 01-<slug>.md
    └── 02-<slug>.md
```

Bug fast-path (optional): `.scratch/bugs/NN-<slug>.md`

## File format — PRD.md

```markdown
# PRD: <title>

Status: needs-slicing | ready-for-implementation | in-progress | ready-to-review
Kind: feature | bug | chore
Epic: <feature-slug>

## Delivery

- Branch: `feature/prd-<slug>`
- Branch owner: agent | human
- Push: each-slice | finalize | never

<prd body sections>
```

## File format — slice issue

Path: `.scratch/<feature-slug>/issues/<NN>-<slug>.md`

```markdown
# <slice title>

Status: open | closed
Parent: .scratch/<feature-slug>/PRD.md

## What to build
...

## Acceptance criteria
- [ ] ...

## Blocked by
None - can start immediately
```

## Status transitions

Same handoff cycle as GitHub labels:

`ready-for-implementation` ↔ `in-progress` (per slice) → `ready-to-review`

Update the `Status:` line in `PRD.md`. Append comments under `## Comments` with timestamp.

## Skill operations

### `/to-prd` — publish PRD

1. Create `.scratch/<feature-slug>/PRD.md` with `Status: needs-slicing`
2. Include `## Delivery` with branch-owner and push from `docs/agents/workflow.md`

### `/to-issues` — publish slices

1. Create `.scratch/<feature-slug>/issues/<NN>-<slug>.md` per slice (numbered from `01`)
2. Update PRD: `Status: ready-for-implementation`

### `/implement` — fetch by path or slug

| Operation | Action |
|-----------|--------|
| Fetch PRD | Read `.scratch/<slug>/PRD.md` (or path user passed) |
| List slices | Glob `.scratch/<slug>/issues/*.md`; filter `Status: open` |
| Set in-progress | Edit PRD `Status: in-progress` |
| Handoff | Edit PRD `Status: ready-for-implementation` |
| Close slice | Set slice `Status: closed`; check AC boxes |
| Comment | Append to PRD or slice under `## Comments` |
| Finalize | PRD `Status: ready-to-review` |

Reference PRD by directory slug: `/implement <feature-slug>` reads `.scratch/<feature-slug>/PRD.md`.

### Single-slice mode

When PRD has `ready-for-implementation` and **no open slice files**, implement acceptance criteria from PRD body directly.

## When a skill says "publish to the issue tracker"

Create files under `.scratch/<feature-slug>/` (create directories as needed).

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path or `.scratch/<slug>/PRD.md`.
