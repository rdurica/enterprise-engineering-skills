---
name: implement
description: >-
  Implement a published analysis — spawn TDD sub-agents for the work, commit,
  then run verify. Use when picking up an analysis issue or /implement #N.
disable-model-invocation: true
---

# Implement

Fetch the analysis, set `in-progress`, follow `docs/agents/workflow.md` for branch and monorepo. Sub-agents write product code and tests. Parent orchestrates, commits, checks off `## Acceptance`, then runs verify. Do not push or open a PR.

Source of truth is the analysis body. Run `/setup` if `docs/agents/` is missing.

Skills root: parent of this file. Read `{skills-root}/tdd/SKILL.md` (and `integration-tests/SKILL.md` for PHP HTTP). Pass those paths in any sub-agent prompt. When committing, follow `{skills-root}/commit/SKILL.md`.

Read `language` from `workflow.md`.

## 1. Preflight

Fetch the analysis per `docs/agents/issue-tracker.md`. GitHub: `#N`. Local: `/implement 001`, `#1`, or `<slug>` → `.scratch/analysis/NNN-<slug>.md`. **Stop** if GitHub has `ready-to-review`, or the only local match is under `.scratch/analysis/done/`. User invoked `/implement` → proceed (do not require `ready-for-agent`). Auto-start without the user → only if `ready-for-agent` or already `in-progress`; **never** when `needs-attention` is set. Set `in-progress` (removing `needs-attention` if present — this is the resume path after a human acted). User may pass `human` or `agent` to override branch-owner for this session.

Open `## FAQ`: do **not** invent answers. Implement decided parts only; skip parts that depend on open FAQ, or leave the session for later.

## 2. Branch

From analysis `## Delivery`, else `workflow.md`. **human:** stay on HEAD. Never commit on a monorepo container root.

**agent:** in each delivery root (not the container root):

1. `git status` — creating a new branch and the tree is dirty → **stop**. Existing branch: unrelated dirty files → **stop**.
2. `git fetch origin` — missing `origin` or fetch fails → **stop**.
3. Default base: `origin/HEAD`, else `origin/main`, else `origin/master`.
4. `<branch>` exists locally or on origin → checkout; if `origin/<branch>` exists, `git pull --rebase`. Do not reset onto origin/default.
5. `<branch>` does not exist → create from origin, never from HEAD:

```bash
git checkout --no-track -b <branch> origin/<default>
```

`--no-track` so the new branch does not track `origin/main`.

## 3. Plan

Product code always goes through **sub-agents** — a flat Architecture does not skip agents.

- Architecture `###` subsections present → one sub-agent per subsection (faster split)
- No subsections → still spawn agents: one for the whole analysis, or more sequentially when the work is large

`## Acceptance` is verify + TDD constraint, not a WBS. Print one line per part and start. Resume: skip work already in the branch / checked Acceptance.

## 4. Execute

One part, then commit, then the next. Never parallel implement sub-agents.

**Sub-agent:** one `generalPurpose` `Task`. It writes code and tests only — no commit, push, PR, branch change, nested agents, or container-root commits. Prompt: this part only; analysis Change / Architecture (relevant `###`) / API Contracts / Acceptance as constraints; open FAQ to skip; skill paths; `AGENTS.md` commands; delivery-root paths; no scope creep (stay inside Change/Architecture).

**Parent** does not write product code except a one-file follow-up after the agent (import, typo).

Then: diff, relevant tests. Small failures: fix yourself (one file). Large: another sub-agent with the error. Commit in each affected delivery root per `commit/SKILL.md` (`feat(scope): <part title> (#<N>)`).

Check off matching `## Acceptance` items. Do not comment on the ticket after each part. Commit messages stay English. Then the next part.

## 5. Verify

Decided parts done (or all parts if no blocking FAQ) → read and follow `{skills-root}/verify/SKILL.md` in this session. If FAQ skipped work remains: set `needs-attention` (replacing `in-progress`), comment what remains in `language`; do not run verify as if the analysis were complete. If the session dies first: leave `in-progress` — that state is resumable and needs no human — comment what remains in `language`; re-run `/implement` to resume.
