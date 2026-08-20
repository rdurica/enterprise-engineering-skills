---
name: monorepo-update
description: >-
  Syncs a monorepo after sub-repo PRs merge — enters each delivery root, runs
  git checkout main and git pull, then commits and pushes submodule pointer bumps on the
  container root. Use when the user runs /monorepo-update or asks to bump
  submodules / sync monorepo to latest main.
disable-model-invocation: true
---

# Monorepo update

Enter every delivery root, run `git checkout main` and `git pull`, then bump and push submodule pointers on the container root. Complements `/implement` — agents never commit pointer bumps during implementation.

Run from the **container root** of the target project (not `~/.cursor/skills`).

## When to use

- After sub-repo PRs are merged to `main`
- User runs `/monorepo-update`, or asks to bump submodules / sync monorepo to latest `main`

## Prerequisites

- Prefer `docs/agents/workflow.md` with `## Monorepo` and `delivery-roots`
- If `## Monorepo` or `delivery-roots` is missing, fall back to `git submodule status` for delivery-root paths
- Stop only if neither `workflow.md` nor `git submodule status` can identify delivery roots; then suggest `/setup`
- `git` and network access; `origin` remote must exist on the container root for push

## Step 1: Load config

Read `## Monorepo` from `docs/agents/workflow.md` when available (same terms as `/implement`):

- **container-root** — monorepo wrapper (usually `.`)
- **delivery-roots** — list of `{ path, remote }` entries

If the file, section, or paths are missing, fall back to `git submodule status` for paths.

Record each delivery-root HEAD before sync (`git -C <path> rev-parse HEAD`) for the final report.

## Step 2: Preflight (mandatory — all roots)

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

A delivery root being on a feature branch, ahead of `origin/main`, or behind `origin/main` is not a blocker by itself. If the delivery root is clean, continue and switch it to `main` in Step 3.

**STOP** if the container root has:

- Merge or rebase in progress
- Uncommitted changes outside the delivery-root submodule paths
- Untracked files outside the delivery-root submodule paths

Submodule pointer changes for delivery-root paths are allowed in the container root. They are the refs this skill is expected to stage, commit, and push.

On STOP, report a per-repo table: `path`, branch, problem, suggested fix. Do not stash, discard, or force anything.

## Step 3: Sync delivery roots

In `workflow.md` order, for each delivery root:

```bash
cd <path>
git checkout main
git pull
```

On failure (dirty tree, missing `main`, diverged branch, conflict, network error) → **STOP**. Do not commit on the container root.

## Step 4: Bump container root

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

## Step 5: Report

Respond in the user's language. Include:

- Each delivery root: previous SHA → new SHA (`git -C <path> rev-parse HEAD`)
- Container: commit hash and push status, or noop if pointers unchanged
- On STOP: concrete commands to fix each blocked root

## Forbidden

- Edit code in delivery roots — checkout and pull only
- Commit or push in delivery roots
- Use `git pull --rebase`
- Force-push
- Auto-stash — user fixes dirty trees manually
- Commit anything on the container root except submodule pointer updates

## Checklist

```
- [ ] Delivery-root config loaded from workflow.md or fallback
- [ ] Delivery-root paths loaded from workflow.md or git submodule status
- [ ] Delivery roots clean; container has no changes except allowed submodule refs
- [ ] Each delivery root checked out to main and pulled
- [ ] Container pulled; submodule paths staged
- [ ] Commit + push (or noop if already up to date)
- [ ] Per-repo SHA report delivered
```
