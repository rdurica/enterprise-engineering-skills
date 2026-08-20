---
name: implement
description: >-
  Implement a PRD — plan increments, do small work in the parent, spawn TDD
  sub-agents only for large changes, then run verify. Use when picking up a
  PRD issue or /implement #PRD.
disable-model-invocation: true
---

# Implement

Fetch the PRD, set `in-progress`, follow `docs/agents/workflow.md` for branch and monorepo. Plan increments from `## Acceptance criteria`. Do small/polish work yourself; `Task` sub-agents only for large cross-layer work. One increment at a time, TDD, commit, check off AC. When AC are done, read and follow `verify/SKILL.md`. Do not push or open a PR.

Source of truth is the PRD body. Run `/setup` if `docs/agents/` is missing.

Skills root: parent of this file. Read `{skills-root}/tdd/SKILL.md` (and `integration-tests/SKILL.md` for PHP HTTP). Pass those paths in any sub-agent prompt. When committing, follow `{skills-root}/commit/SKILL.md`.

## 1. Preflight

Fetch the PRD per `docs/agents/issue-tracker.md`. GitHub: `#N`. Local: `/implement 001`, `#1`, or `<slug>` → `.scratch/prd/NNN-<slug>.md`. **Stop** if GitHub has `ready-to-review`, or the only local match is under `.scratch/prd/done/`. User invoked `/implement` → proceed (do not require `ready-for-agent`). Auto-start without the user → only if `ready-for-agent` or already `in-progress`. Set `in-progress`. User may pass `human` or `agent` to override branch-owner for this session.

## 2. Branch

From PRD `## Delivery`, else `workflow.md`. **agent:** checkout/create the Delivery branch in each delivery root (`pull --rebase` if it exists). **human:** stay on HEAD. Never commit on a monorepo container root. Stop if a delivery root has unrelated dirty files.

## 3. Plan

Ordered increments from `## Acceptance criteria`. Each is a thin vertical slice, test-first — not a horizontal layer.

- **parent** (default) — small, localized, polish, few files
- **sub-agent** — large: new behaviour across layers, new modules, or would drown this context

A tiny PRD can be entirely parent (still list increments, still TDD). Print one line each with `parent` or `sub-agent` and start. Resume: skip done AC (checkboxes / already in the branch).

## 4. Execute

One increment, then commit, then the next. Never parallel implement sub-agents.

**Parent:** write code and tests yourself.

**Sub-agent:** one `generalPurpose` `Task`. It writes code and tests only — no commit, push, PR, branch change, nested agents, or container-root commits. Prompt: this increment only, PRD Problem/Solution/Out of Scope/AC, skill paths, `AGENTS.md` commands, delivery-root paths, no scope creep.

Then: diff, relevant tests. Small failures: fix yourself. Large: another sub-agent with the error. Commit in each affected delivery root per `commit/SKILL.md` (`feat(scope): <increment title> (#<PRD>)`).

Check off matching AC on the PRD. Ticket comments in `prd-language` from `workflow.md`. Commit messages stay English. Then the next increment.

## 5. Verify

All AC done → read and follow `{skills-root}/verify/SKILL.md` in this session. If the session dies first: leave `in-progress`, comment what remains in `prd-language`; re-run `/implement` to resume.
