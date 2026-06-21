---
name: to-review
description: >-
  Review changes since a fixed point along two axes — Standards (repo coding
  conventions) and Spec (originating issue/PRD). Runs parallel sub-agents.
  Use when running `/to-review` on a branch, PR, or WIP changes, or when asked
  to review since a commit or branch.
disable-model-invocation: true
---

# To Review

Two-axis review of the diff between `HEAD` and a fixed point the user supplies:

- **Standards** — does the code follow this repo's documented conventions?
- **Spec** — does the code match the originating issue / PRD?

Both axes run as **parallel sub-agents**, then this skill aggregates findings.

Read `docs/agents/issue-tracker.md` if present — run `/setup` if missing.

## Process

### 1. Pin the fixed point

Use whatever the user specified — commit SHA, branch, tag, `main`, `HEAD~N`. Ask if not specified.

```bash
git rev-parse <fixed-point>
git diff <fixed-point>...HEAD
git log <fixed-point>..HEAD --oneline
```

Confirm the ref resolves and the diff is non-empty before spawning sub-agents.

### 2. Identify the spec source

1. Issue refs in commit messages (`#123`, `Closes #45`) — fetch via `docs/agents/issue-tracker.md`
2. Path the user passed
3. PRD under `docs/`, `specs/`, or `.scratch/` matching the branch or feature
4. Ask the user; if none, Spec sub-agent reports "no spec available"

### 3. Identify standards sources

`AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `CODING_STANDARDS.md`, ADRs, module `AGENTS.md` files.

### 4. Spawn both sub-agents in parallel

One message, two `Task` calls with `subagent_type: generalPurpose`.

**Standards prompt** — include diff command, commit list, standards file list:

> Report every place the diff violates a documented standard. Cite file + rule. Distinguish hard violations from judgement calls. Skip what tooling enforces. Under 400 words.

**Spec prompt** — include diff command, commit list, spec contents:

> Report: (a) missing or partial requirements; (b) scope creep; (c) requirements that look wrong. Quote the spec line per finding. Under 400 words.

Skip Spec sub-agent if no spec exists.

### 5. Aggregate

Present under `## Standards` and `## Spec` — do not merge or rerank across axes.

End with one line: finding count per axis and worst issue within each axis (if any).

## Why two axes

- Standards pass, Spec fail → correct style, wrong behaviour
- Spec pass, Standards fail → correct feature, wrong conventions

Reporting separately stops one axis masking the other.
