# Issue tracker: GitHub

Issues and analyses live as GitHub issues. Use the `gh` CLI.

## Which GitHub repo

- **Single repo:** infer from `git remote -v` in the clone (cwd).
- **Monorepo** (resolved configuration: `## Monorepo` or detected nested repos, see `config.md`): **always** the **container-root** remote — never a delivery-root (`backend`, `frontend`, …).

Resolve container-root `owner/repo` from `git -C <container-root> remote get-url origin` (or `remote:` on `container-root` in the resolved configuration if set). Pass it on every `gh issue` call:

```bash
gh issue create -R <owner/container-repo> ...
gh issue view <N> -R <owner/container-repo> ...
gh issue edit <N> -R <owner/container-repo> ...
```

Do not invent a delivery-root issue tracker. Agent-owned PRs still open in delivery roots (`/verify`); human-owned PRs remain with the user; only issues/analyses live on the monorepo.

## Conventions

Always add `-R <owner/repo>` in a monorepo (container-root remote — see above).

- **Create:** `gh issue create [-R …] --title "..." --body-file <file> --label "..."`
- **Read:** `gh issue view <number> [-R …] --comments`
- **Edit body:** `gh issue edit <number> [-R …] --body-file <file>`
- **List:** `gh issue list [-R …] --state open --limit 200 --json number,title,body,labels`
- **Comment:** `gh issue comment <number> [-R …] --body-file <file>`
- **Labels:** `gh issue edit <number> [-R …] --add-label "..."` / `--remove-label "..."`
- **Close:** `gh issue close <number> [-R …] --comment "..."`

## Labels

| Label | Set by | Meaning |
|-------|--------|---------|
| `idea` | `/idea` | Idea, not yet analyzed. `/analyze #N` replaces it with `analysis`; `/implement` refuses it |
| `analysis` | `/analyze` | This issue is an analysis |
| `in-progress` | `/implement` | Agent is working |
| `needs-attention` | `/verify` (fail), `/implement` (blocked by open FAQ) or `/analyze-modify` (delivered work revised) | Agent stopped and cannot continue without a human decision or fix. **Replaces** `in-progress` — never both |
| `ready-to-review` | `/verify` (green) | Verified delivery ready for human review; publishing-enabled agent-owned delivery also has a ready PR. `/complete` removes it when it merges the PR and closes the issue |

`/implement` drops `needs-attention` when it sets `in-progress`. A green `/verify` removes pipeline working labels and sets `ready-to-review`. Preserve unrelated labels (team, priority, kind). Keep `analysis` when present; bug fast-path tickets need not have it. Human-owned delivery does not require a PR. The completion comment records verified SHA, local gates, push and CI outcome, and PR URLs when applicable.

`/implement` stops if `ready-to-review`. `needs-attention` does **not** stop it — that is the resume path.

Create a label on first use if it is missing (`gh label create <name> [-R …]`; ignore "already exists").

**Lifecycle:** `idea` → `/analyze #N` → `analysis` → user reviews, then `/implement` → `in-progress` → `ready-to-review` → `/complete` (agent-owned with a PR: rebase-merge, close). Verify fail → `needs-attention` and a comment on this issue; agent-owned delivery may have a draft PR only when push and PR operations are allowed. Remaining work blocked by open `## FAQ` → `needs-attention`. Session died → leave `in-progress` (resumable); re-run `/implement`.

## Delivery section

After `/analyze`, prepend to issue body:

```markdown
## Delivery

- Ticket: [AB#4821](https://dev.azure.com/org/project/_workitems/edit/4821)
- Kind: feature | bug | chore
- Branch: `feature/4821-group-pricing`
- Depends on: #41, #42               (optional)
```

`Ticket` is the external tracker item when there is one (clickable link), otherwise this issue: `Ticket: [#<N>](<issue url>)`. `Branch` reuses that same number as `feature/<ticket>-<short-slug>`. Commits and PRs still reference the analysis issue as `#N` — that is the number GitHub autolinks.

`Depends on` (optional, written by `/idea`, kept on conversion) lists issue numbers that must be closed first. A dependency is satisfied when `gh issue view <dep> [-R …] --json state` reports `CLOSED`; `ready-to-review` does not count, because the code is not on main yet.

## Skill operations

### `/idea` — create and edit an idea

Ensure the `idea` label exists (`gh label create idea --description "Idea, not yet analyzed"`; ignore "already exists").

| Operation | Command |
|-----------|---------|
| Create | `gh issue create [-R …] --title "Idea: ..." --body-file <file> --label idea` |
| Add Delivery | `gh issue edit <N> [-R …] --body-file <file-with-delivery>` (the number is known only after creating) |
| Rewrite (`/idea #N`) | `gh issue edit <N> [-R …] --body-file <file>` |
| List open ideas and analyses | `gh issue list [-R …] --state open --limit 200 --json number,title,body,labels` |

Refuse `/idea #N` when the issue has the `analysis` label.

### `/analyze` — publish analysis

Ensure the `analysis` label exists (`gh label create analysis --description "Published analysis"`; ignore "already exists").

Write the complete analysis to a temporary file, then pass it with `--body-file`. After creating the issue, add Delivery to that file and update the issue body. Preserve real newlines and literal contract values.

```bash
# Add -R <owner/container-repo> when ## Monorepo
gh issue create -R <owner/repo> --title "Analysis: ..." --body-file <analysis-file> --label analysis
gh issue edit <number> -R <owner/repo> --body-file <analysis-file-with-delivery>
```

**Converting an idea** (`/analyze #N` on an issue labelled `idea`) reuses the same issue; no new one is created. First check `Depends on` with `gh issue view <dep> [-R …] --json state`. Then write the full analysis (with the idea's `## Delivery`) to a file and:

```bash
gh issue edit <N> [-R …] --title "Analysis: ..." --body-file <analysis-file> --remove-label idea --add-label analysis
```

### `/analyze-modify` — revise analysis

Same `-R` rule as `/analyze`. Write the full revised body to a temporary file.

| Operation | Command |
|-----------|---------|
| Fetch analysis | `gh issue view <N> [-R …] --comments` (refuse an issue labelled `idea`; point to `/idea #N` or `/analyze #N`) |
| Update body | `gh issue edit <N> [-R …] --body-file <file>` |
| Comment | `gh issue comment <N> [-R …] --body-file <file>` (one-paragraph summary headed `## Revision`; only for an implemented analysis) |
| Update revision comment | `gh api -X PATCH repos/<owner>/<repo>/issues/comments/<id> -F body=@<file>` (find `<id>` via `gh api repos/<owner>/<repo>/issues/<N>/comments`; used when the revision is still unchecked) |
| Delivered work revised | `gh issue edit <N> [-R …] --remove-label ready-to-review --add-label needs-attention` (only when `ready-to-review` was set) |

Keep `in-progress` and `needs-attention` as they are.

### `/implement` — fetch, status, comment

Same `-R` rule as `/analyze` (container-root in monorepo). Fetch `#N` by number.

| Operation | Command |
|-----------|---------|
| Fetch analysis/ticket | `gh issue view <N> [-R …] --comments` |
| Refuse | An issue labelled `idea`, or with an open `Depends on` (`gh issue view <dep> [-R …] --json state` is not `CLOSED`), stops before any label changes. Checked on every run, resume included |
| Set in-progress | `gh issue edit <N> [-R …] --remove-label needs-attention --add-label in-progress` |
| Blocked by open FAQ | `gh issue edit <N> [-R …] --remove-label in-progress --add-label needs-attention` |
| Update Acceptance checkboxes | `gh issue edit <N> [-R …] --body-file <file>` (checked items in `## Acceptance` and realized entries in `## Revisions`) |
| Comment | `gh issue comment <N> [-R …] --body-file <file>` (brief interruption/blocker note when needed — not per part) |

### `/verify` — comment on the analysis only (never on the PR)

| Operation | Command |
|-----------|---------|
| Green | `gh issue edit <N> [-R …] --remove-label in-progress --remove-label needs-attention --add-label ready-to-review` then `gh issue comment` (verified SHA, local gates, push/CI outcome, PR URLs when applicable). Preserve unrelated labels |
| Fail | `gh issue edit <N> [-R …] --remove-label in-progress --remove-label ready-to-review --add-label needs-attention` then `gh issue comment` (what failed, draft PR URLs when applicable). Human-owned never manages PRs; agent-owned draft PR delivery follows push policy and session restrictions |

### `/complete` — merge and close

Only for agent-owned delivery with an open PR on an open `ready-to-review` issue; otherwise `/complete` does nothing.

| Operation | Command |
|-----------|---------|
| Merge | `gh pr merge <pr> --rebase --delete-branch --match-head-commit <sha>` in each delivery root |
| Close | `gh issue edit <N> [-R …] --remove-label ready-to-review` then `gh issue close <N> [-R …] --comment "..."` (merged PR URLs and commit). Preserve unrelated labels |

## When a skill says "publish to the issue tracker"

Create a GitHub issue using the operations above (monorepo → container-root `-R`).

## When a skill says "fetch the relevant ticket"

Run `gh issue view <number> [-R …] --comments`.
