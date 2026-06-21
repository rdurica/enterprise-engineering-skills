# Domain Docs

How engineering skills consume domain documentation in this repo.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root, or
- **`CONTEXT-MAP.md`** if it exists — then read each relevant per-context `CONTEXT.md`
- **`docs/adr/`** — ADRs for the area you are touching (in multi-context repos also `src/<context>/docs/adr/`)

If these files do not exist, proceed silently. `/align` creates or updates them when terms and decisions land.

## Layout

**Single-context** (most repos):

```
/
├── CONTEXT.md
├── docs/adr/
└── src/
```

**Multi-context** (`CONTEXT-MAP.md` at root):

```
/
├── CONTEXT-MAP.md
├── docs/adr/
└── src/<context>/
    ├── CONTEXT.md
    └── docs/adr/
```

## Vocabulary

Use terms as defined in `CONTEXT.md` in issue titles, test names, and proposals. Do not drift to synonyms the glossary avoids.

## ADR conflicts

If output contradicts an existing ADR, surface it explicitly:

> _Contradicts ADR-0007 — but worth reopening because…_
