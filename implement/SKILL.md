---
name: implement
description: >-
  Implement one slice for a ready-for-implementation PRD, verify Definition of
  Done before commit, then hand off to the next agent via label toggle. Use when
  picking up a PRD issue or /implement #PRD. Supports branch-owner agent|human
  and GitHub or local issue tracker.
disable-model-invocation: true
---

# Implement

Implement **exactly one slice** for the parent PRD, then **stop and hand off** so a fresh agent continues the next slice.

Do not implement slice issues directly — always enter via the parent PRD (or single-slice bug ticket with `ready-for-implementation`).

Read `docs/agents/issue-tracker.md`, `docs/agents/workflow.md`, and `docs/agents/domain.md` if present — run `/setup` if missing.

All tracker operations follow `docs/agents/issue-tracker.md` (GitHub `gh` commands or local `.scratch/` files — do not hardcode one backend).

## Workflow

### 1. Preflight

- **Tracker:** follow `docs/agents/issue-tracker.md` to fetch the ticket (GitHub `#N` or local `.scratch/<slug>/PRD.md`).
- Ticket must be in `ready-for-implementation` state (GitHub label or PRD `Status:` line).
- If it is a slice issue without `prd` → stop. Tell the user to run `/implement` on the parent PRD instead.
- Set in-progress on the PRD (remove `ready-for-implementation`, add `in-progress` / edit Status).
- Read `## Delivery` for branch name, epic label, branch-owner, and push (fallback to `docs/agents/workflow.md`).

**Session override:** if user passes `human` or `agent` in the prompt (e.g. `/implement #42 human`), override branch-owner for this session only.

### 2. Pick the next slice (one only)

List open slices for the epic per issue-tracker conventions.

- Exclude the PRD itself (title starts with `PRD:`).
- Keep slices whose `## Blocked by` references are all **closed**.
- Sort remaining slices topologically; take **only the first**.

**Single-slice mode:** if no eligible slice issues exist, implement acceptance criteria directly from the PRD/ticket body (bug fast-path).

If all slices are already done → go to **Finalize**.

### 3. Branch

Read **branch-owner** from PRD `## Delivery`, else `docs/agents/workflow.md`, else session override.

Run `git status` first.

**branch-owner: agent**

- Branch name from PRD `## Delivery`.
- If branch missing locally/remotely: `git checkout -b <branch>` from default branch.
- If branch exists: checkout, `git pull --rebase origin <branch>` when remote exists.
- **Stop** if working tree has unrelated uncommitted changes — ask user to stash or commit first.

**branch-owner: human**

- Do **not** checkout or create a branch.
- Record `git branch --show-current` for handoff comment.
- Delivery branch name is a hint for PR title only — not enforced.

### 4a. Implement this slice only

1. Read the slice (or PRD) acceptance criteria; implement using **`tdd`** at pre-agreed seams.
2. During TDD cycles, run checks incrementally:
   - Single test file after each red-green cycle
   - **PHP backend HTTP API (Symfony):** follow the `integration-tests` skill
3. Read stack-specific verify commands from target repo `AGENTS.md` (see **4b** for the full gate).

**Do not start the next slice in this session.**

### 4b. Verify — Definition of Done (mandatory)

Do not commit until every gate passes. **Loop:** fix → re-run failed gate → repeat.

| Gate | What to verify |
|------|----------------|
| **Acceptance criteria** | Re-read slice/PRD issue; every item in `## Acceptance criteria` satisfied |
| **Tests** | Full relevant suite green (single file per TDD cycle during 4a; full suite here) |
| **Tooling** | Commands from target repo `AGENTS.md` — e.g. PHP: style fix/check, static analysis; frontend: typecheck |
| **Linter** | No new diagnostics in touched files |
| **Git** | `git status` / `git diff` show only intentional changes — no debug or temp files |

If any gate fails → fix → re-run from the failed gate. Do **not** proceed to commit, close slice, push, or handoff until all gates pass.

Only after all gates pass → proceed to **4c. Ship**.

### 4c. Ship (only after Verify passes)

1. Commit: `feat(scope): <slice title> (#<sliceNum or slug>)`
2. Close slice per issue-tracker conventions (or mark PRD AC done in single-slice mode).
3. **Push** per push policy from Delivery / `workflow.md`:
   - `each-slice`: `git push -u origin <branch>` (skip if no remote or branch-owner human with no remote tracking)
   - `finalize`: skip push here
   - `never`: skip push; note in handoff comment

Current branch for handoff: `git branch --show-current`.

### 5. Hand off or finalize

Check for remaining open slices (same epic, excluding PRD):

**More slices remain:**

Update PRD to `ready-for-implementation` (remove `in-progress`) per issue-tracker conventions.

Handoff comment must include: branch-owner, current branch, push policy, slice completed, next slice ref, gates passed.

Stop. Do not implement further slices.

**Last slice done → Finalize:**

1. Run **`/to-review`** against merge-base when the branch was first created (or first commit on branch vs default branch).
2. Push if policy is `finalize` and not yet pushed: `git push -u origin <branch>`
3. Open PR when branch-owner is agent or user expects it (`gh pr create` for GitHub repos).
4. Update PRD to `ready-to-review`; comment with PR URL if created.

When branch-owner is `human` and push is `never`, skip PR creation unless user asked — note in comment that user should push and open PR.

### 6. Failure mid-slice

If the session ends before the slice is closed:

- Leave PRD in `in-progress` (do **not** re-add `ready-for-implementation`).
- Comment on PRD what was done and what remains on the slice.
- If failure happened during **4b Verify**, list which gates passed and which failed, plus the last error output from the failing gate.
- User recovery: manually restore `ready-for-implementation` on the PRD per issue-tracker conventions.

## Rules

- **One slice per session** — hand off via `ready-for-implementation` on PRD after each slice
- **Never** implement multiple slices in one session
- Minimal code per test cycle — no speculative features
- Do not close the parent PRD — only transition to `ready-to-review` after finalize
- Slice issues never get `ready-for-implementation` — trigger stays on PRD only
- **Verify before ship** — all DoD gates (4b) must pass before commit, close, push, or handoff

## Forbidden

- Hand off with failing tests or local CI checks (style, static analysis, typecheck)
- Commit with known PHPStan, style, or linter violations
- Skip the full test suite to save time
- Re-add `ready-for-implementation` on the PRD before Verify (4b) passes
- Checkout or create branches when branch-owner is `human`
