---
name: monorepo-update
description: >-
  Syncs monorepo delivery roots: no args checks out main and bumps submodule
  pointers; a PRD number (#N / 123 / 001) checks out that PRD's Delivery branch
  in affected roots (others to main) for human review. Use when the user runs
  /monorepo-update, passes a PRD number, or asks to bump submodules / set up
  checkout for review.
disable-model-invocation: true
---

# Monorepo update

Two modes. Complements `/implement` — agents never commit pointer bumps during implementation.

Run from the **container root** of the target project (not `~/.cursor/skills`).

| Invocation | Mode | What happens |
|------------|------|----------------|
| `/monorepo-update` (no PRD) | **main** | Each delivery root → `main` + pull; container commits and pushes submodule pointer bumps |
| `/monorepo-update 123`, `#123`, or `001` | **PRD** | Fetch PRD `## Delivery` branch; affected roots → that branch; others → `main`. No container commit |

## When to use

- After sub-repo PRs merge to `main` → mode **main**
- Before human review of a PRD, so every delivery root is on the right branch → mode **PRD**
- User runs `/monorepo-update` with or without a PRD number

## Prerequisites

- Prefer `docs/agents/workflow.md` with `## Monorepo` and `delivery-roots`
- If `## Monorepo` or `delivery-roots` is missing, fall back to `git submodule status` for delivery-root paths
- Stop only if neither `workflow.md` nor `git submodule status` can identify delivery roots; then suggest `/setup`
- `git` and network access
- Mode **main**: `origin` on the container root (for push)
- Mode **PRD**: `docs/agents/issue-tracker.md` to resolve the PRD

## Step 1: Load config

Read `## Monorepo` from `docs/agents/workflow.md` when available (same terms as `/implement`):

- **container-root** — monorepo wrapper (usually `.`)
- **delivery-roots** — list of `{ path, remote }` entries

If the file, section, or paths are missing, fall back to `git submodule status` for paths.

Record each delivery-root HEAD before sync (`git -C <path> rev-parse HEAD`) for the final report.

## Step 2: Choose mode

- User passed a PRD id (`123`, `#123`, `001`, or a slug that resolves like `/implement`) → **PRD**
- Otherwise → **main**

## Step 3: Preflight (mandatory — all roots)

For the container root and **each** delivery root:

```bash
cd <path>
git status -sb
git branch --show-current
```

For the container root, also inspect porcelain status:

```bash
git status --porcelain --untracked-files=all
```

**STOP** if any delivery root has:

- Uncommitted changes (tracked or untracked outside `.gitignore`)
- Merge or rebase in progress

A delivery root being on a feature branch, ahead of `origin/main`, or behind `origin/main` is not a blocker by itself. If the delivery root is clean, continue and switch it in the mode step.

**STOP** if the container root has:

- Merge or rebase in progress
- Uncommitted changes outside the delivery-root submodule paths
- Untracked files outside the delivery-root submodule paths

Submodule pointer changes for delivery-root paths are allowed on the container root. Mode **main** stages, commits, and pushes them. Mode **PRD** leaves them dirty — do not commit.

On STOP, report a per-repo table: `path`, branch, problem, suggested fix. Do not stash, discard, or force anything.

## Step 4a: Mode main — sync delivery roots

In `workflow.md` order, for each delivery root:

```bash
cd <path>
git checkout main
git pull
```

On failure (dirty tree, missing `main`, diverged branch, conflict, network error) → **STOP**. Do not commit on the container root.

## Step 4b: Mode main — bump container root

```bash
cd <container-root>
git checkout main
git pull
git add <submodule-paths>   # paths from delivery-roots
git status
```

If `git diff --cached` is empty → report **submodules already up to date** and finish (no empty commit).

Otherwise:

```bash
git commit -m "$(cat <<'EOF'
chore: bump submodules to latest main

EOF
)"
git push origin main
```

## Step 4c: Mode PRD — checkout for review

1. Fetch the PRD per `docs/agents/issue-tracker.md` (GitHub: `#N` on the **container-root** remote; local: `.scratch/prd/NNN-<slug>.md`). Same resolution as `/implement`.
2. Read **`## Delivery` → Branch**. Missing PRD or Delivery branch → **STOP**.
3. Container **stays on `main`**. Do not `git add`, commit, or push submodule pointers (that would write feature SHAs onto container `main`).
4. In `workflow.md` order, for each delivery root:

```bash
git -C <path> fetch origin
```

**Affected** if any of:

- `origin/<branch>` exists
- local `<branch>` exists
- a PR with head `<branch>` exists on that root's remote (`gh pr list -R <delivery-remote> --head <branch>`)
- local `<branch>` has commits vs `origin/main`

Affected:

```bash
git -C <path> checkout <branch>
```

Then pull: tracking branch → `git pull`; else if `origin/<branch>` exists → `git pull origin <branch>`; else leave the local checkout (do not create a missing remote branch).

Not affected:

```bash
git -C <path> checkout main
git -C <path> pull
```

Do **not** create a branch that does not already exist locally or on origin.

5. If **no** delivery root was affected → **STOP** (nothing to review). Roots already switched to `main` in this step may stay on `main`; report that the Delivery branch was not found.

On failure (dirty tree, missing ref, diverged branch, conflict, network error) → **STOP**.

## Step 5: Report

Respond in the user's language.

**Both modes:** each delivery root: previous SHA → new SHA (`git -C <path> rev-parse HEAD`), current branch.

**Mode main:** container commit hash and push status, or noop if pointers unchanged.

**Mode PRD:** PR URL per affected root when one exists (`gh pr view` / `gh pr list --head <branch>` on that remote). State that container submodule pointers are expected dirty and must not be committed; they are for local review only.

On STOP: concrete commands to fix each blocked root.

## Forbidden

- Edit code in delivery roots — checkout and pull only
- Commit or push in delivery roots
- Use `git pull --rebase`
- Force-push
- Auto-stash — user fixes dirty trees manually
- Mode **main**: commit anything on the container root except submodule pointer updates
- Mode **PRD**: any commit or push on the container root; creating a Delivery branch that does not exist

## Checklist

```
- [ ] Delivery-root config loaded from workflow.md or fallback
- [ ] Mode chosen (main vs PRD)
- [ ] Delivery roots clean; container has no changes except allowed submodule refs
Mode main:
- [ ] Each delivery root checked out to main and pulled
- [ ] Container pulled; submodule paths staged
- [ ] Commit + push (or noop if already up to date)
Mode PRD:
- [ ] PRD and Delivery branch loaded
- [ ] Affected roots on Delivery branch; others on main
- [ ] No container commit/push
- [ ] Per-repo SHA / branch / PR URL report delivered
```
