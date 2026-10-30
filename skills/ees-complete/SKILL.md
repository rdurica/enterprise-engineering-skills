---
name: ees-complete
description: >-
  Completes a reviewed agent-owned delivery: rebase-merges its PR(s), deletes
  the Delivery branch, closes the analysis issue and drops ready-to-review,
  then switches local checkouts to main and pulls. Does nothing when the
  delivery is human-owned or has no PR. Use when the user runs /ees-complete with
  an analysis number after reviewing a ready-to-review delivery.
argument-hint: "[#N | NNN | slug]"
disable-model-invocation: true
model: haiku
effort: low
---

# Complete

Request: $ARGUMENTS

Final step after the human review of a `ready-to-review` delivery. Merge is irreversible: run every check in Step 2 before any write, and never merge part of a delivery.

## Step 1: Load config and analysis

1. Resolve configuration per `{skills-root}/ees-pipeline/config.md` (`branch-owner`, `push`, `tracker`, `language`, monorepo) and tracker operations per `{skills-root}/ees-pipeline/tracker-<tracker>.md`; skills root is the parent of this skill's directory.
2. Resolve the analysis like `/ees-implement`: `#N`, `NNN` or slug. No argument → the analysis whose `## Delivery` Branch is the current branch. GitHub: `gh issue view <N> [-R <container-repo>] --json number,state,labels,body,url`. Local: `docs/agents/analysis/` or `docs/agents/analysis/done/`.
3. Read `## Delivery` → Branch. Missing analysis or Branch → **STOP**.
4. Delivery roots: single repo → `.`; monorepo → every `delivery-roots` path. The container root is never merged or switched to a feature branch.

## Step 2: Applicability gate

Check everything first. If any line below holds, **stop without doing anything** — no merge, no branch deletion, no tracker change, no checkout — and report which line applied.

- `branch-owner: human` — PRs belong to the user.
- `push: never`, or the session forbids pushing — nothing was published.
- GitHub: the issue is closed, or lacks `ready-to-review`. Local: the file is not in `done/`.
- No open PR for the Delivery branch in any delivery root: `cd <path> && gh pr list --head <branch> --state open --json number,url`.

Then, for every root that has an open PR, check the PR and the local checkout:

```bash
cd <path>
gh pr view <pr> --json number,url,state,isDraft,mergeable,reviewDecision,headRefOid,baseRefName
gh pr checks <pr>
git status --porcelain --untracked-files=all
```

**STOP** when any PR:

- is a draft, or not `OPEN`
- is not `MERGEABLE` (conflicts or `UNKNOWN` — retry `gh pr view` once after a few seconds before stopping on `UNKNOWN`)
- has `reviewDecision: CHANGES_REQUESTED` (approval itself is not required)
- has a failing, pending or cancelled check (no checks at all is fine)
- has a local branch `<branch>` with commits missing from `headRefOid` (`git rev-list --count <headRefOid>..<branch>` > 0) — merging would lose them

Also **STOP** when a delivery root has uncommitted or untracked changes, or a merge/rebase in progress.

On STOP report a per-root table: path, PR URL, problem, suggested fix. Do not stash, discard, push or force anything.

## Step 3: Merge

Only after every root passed Step 2. In resolved-config order, for each root with a PR:

```bash
cd <path>
gh pr merge <pr> --rebase --delete-branch --match-head-commit <headRefOid>
```

`--delete-branch` removes the remote and local branch. If a merge fails, **STOP**: report which roots are already merged and which are not; never retry with another merge method.

## Step 4: Close the ticket

GitHub (monorepo → container-root `-R`):

```bash
gh issue edit <N> [-R …] --remove-label ready-to-review
gh issue close <N> [-R …] --comment "<body>"
```

The comment is one short paragraph in `language`: merged PR URLs and the merged commit on `<baseRefName>`. Preserve all other labels.

Local tracker: the file already sits in `done/` — change nothing.

An external `Ticket` link in `## Delivery` (Azure, Jira, …) is not closed here; mention it in the report.

## Step 5: Sync local checkouts

For each delivery root (also those without a PR in a monorepo):

```bash
cd <path>
git checkout <baseRefName>     # usually main
git pull --ff-only
git fetch --prune
git branch -d <branch> 2>/dev/null || true
```

`git branch -d` only, never `-D`. A pull that cannot fast-forward → report it, do not fix it.

Monorepo: leave the container root and its submodule pointers alone; recommend `/ees-monorepo-update` to bump them.

## Step 6: Report

Respond in the user's language. Per root: PR URL, merged, branch deleted, current branch and SHA. Then the issue state, any external ticket to close by hand, and the `/ees-monorepo-update` hint in a monorepo.

## Forbidden

- Merge methods other than `--rebase`; `--admin` or any bypass of branch protection
- Merging when any Step 2 check fails, or merging some roots while others are blocked
- Commenting on the PR
- Force-push, `git branch -D`, stash, reset or discard
- Committing anything, including container submodule pointers
