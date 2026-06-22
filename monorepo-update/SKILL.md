---
name: monorepo-update
description: >-
  Syncs a monorepo after sub-repo PRs merge — checks out main and pulls each
  delivery root, then commits and pushes submodule pointer bumps on the
  container root. Use when the user runs /monorepo-update or asks to bump
  submodules / sync monorepo to latest main.
disable-model-invocation: true
---

# Monorepo update

Sync delivery roots to latest `main`, then bump and push submodule pointers on the container root. Complements `/implement` — agents never commit pointer bumps during implementation.

Run from the **container root** of the target project (not `~/.cursor/skills`).

## When to use

- After sub-repo PRs are merged to `main`
- User runs `/monorepo-update`, or asks to bump submodules / sync monorepo to latest `main`

## Prerequisites

- `docs/agents/workflow.md` contains `## Monorepo` with `delivery-roots` — if missing, stop and suggest `/setup`
- `git` and network access; `origin` remote must exist on the container root for push

## Step 1: Load config

Read `## Monorepo` from `docs/agents/workflow.md` (same terms as `/implement`):

- **container-root** — monorepo wrapper (usually `.`)
- **delivery-roots** — list of `{ path, remote }` entries

If paths are missing but the section exists, fall back to `git submodule status` for paths.

Record each delivery-root HEAD before sync (`git -C <path> rev-parse HEAD`) for the final report.

## Step 2: Preflight (mandatory — all roots)

For the container root and **each** delivery root:

```bash
cd <path>
git status -sb
git branch --show-current
```

**STOP** if any root has:

- Uncommitted changes (tracked or untracked outside `.gitignore`)
- Merge or rebase in progress
- A delivery root not on `main`/`master` **and** local commits or changes vs remote

On STOP, report a per-repo table: `path`, branch, problem, suggested fix. Do not stash, discard, or force anything.

Resolve default branch per root when not `main`: `git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@'` or `main` then `master`.

## Step 3: Sync delivery roots

In `workflow.md` order, for each delivery root:

```bash
cd <path>
git checkout <default-branch>
git fetch origin
git pull --ff-only origin <default-branch>
```

Use `--ff-only` deliberately — no merge commits on default branch.

On failure (diverged branch, conflict, network error) → **STOP**. Do not commit on the container root.

## Step 4: Bump container root

```bash
cd <container-root>
git checkout <default-branch>
git fetch origin
git pull --ff-only origin <default-branch>
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
git push origin <default-branch>
```

## Step 5: Report

Respond in the user's language. Include:

- Each delivery root: previous SHA → new SHA (`git -C <path> rev-parse HEAD`)
- Container: commit hash and push status, or noop if pointers unchanged
- On STOP: concrete commands to fix each blocked root

## Forbidden

- Edit code in delivery roots — checkout and pull only
- Commit or push in delivery roots
- Use `git pull --rebase` on default branch (only `--ff-only`)
- Force-push
- Auto-stash — user fixes dirty trees manually
- Commit anything on the container root except submodule pointer updates

## Checklist

```
- [ ] ## Monorepo loaded from workflow.md
- [ ] Preflight clean in container + all delivery roots
- [ ] Each delivery root on default branch, pulled --ff-only
- [ ] Container pulled; submodule paths staged
- [ ] Commit + push (or noop if already up to date)
- [ ] Per-repo SHA report delivered
```
