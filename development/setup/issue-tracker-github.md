# Issue tracker: GitHub

Issues and PRDs live as GitHub issues. Use the `gh` CLI.

Also read `docs/agents/workflow.md` for branch-owner and push defaults.

## Which GitHub repo

- **Single repo:** infer from `git remote -v` in the clone (cwd).
- **Monorepo** (`## Monorepo` in `workflow.md`, or nested git repos / submodules): **always** the **container-root** remote — never a delivery-root (`backend`, `frontend`, …).

Resolve container-root `owner/repo` from `git -C <container-root> remote get-url origin` (or `remote:` on `container-root` in `workflow.md` if set). Pass it on every `gh issue` call:

```bash
gh issue create -R <owner/container-repo> ...
gh issue view <N> -R <owner/container-repo> ...
gh issue edit <N> -R <owner/container-repo> ...
```

Do not invent a delivery-root issue tracker. PRs still open in delivery roots (`/verify`); only issues/PRDs live on the monorepo.

## Conventions

Always add `-R <owner/repo>` in a monorepo (container-root remote — see above).

- **Create:** `gh issue create [-R …] --title "..." --body "..." --label "..."`
- **Read:** `gh issue view <number> [-R …] --comments`
- **Edit body:** `gh issue edit <number> [-R …] --body "..."`
- **List:** `gh issue list [-R …] --state open --json number,title,body,labels`
- **Comment:** `gh issue comment <number> [-R …] --body "..."`
- **Labels:** `gh issue edit <number> [-R …] --add-label "..."` / `--remove-label "..."`
- **Close:** `gh issue close <number> [-R …] --comment "..."`

## Labels

| Label | Set by | Meaning |
|-------|--------|---------|
| `prd` | `/to-prd` | This issue is a PRD |
| `ready-for-agent` | human, after validating the PRD | Auto-trigger may start `/implement`. Agent never adds this |
| `in-progress` | `/implement` | Agent is working |
| `ready-to-review` | `/verify` (green) | Ready PR open, waiting for human merge |

User invoked `/implement` → run it (do not require `ready-for-agent`). Stop if `ready-to-review`.

Auto-start without the user → only if `ready-for-agent` or already `in-progress`.

**Lifecycle:** `prd` → human adds `ready-for-agent` (optional if they call `/implement`) → `in-progress` → `ready-to-review`. Verify fail (agent) → draft PR, stay `in-progress`, comment on this issue. Session died → leave `in-progress`; re-run `/implement`.

## PRD Delivery section

After `/to-prd`, prepend to issue body:

```markdown
## Delivery

- Branch: `feature/prd-<number>-<short-slug>`
- Branch owner: agent | human    # default from docs/agents/workflow.md
- Push: finalize | never
```

## Skill operations

### `/to-prd` — publish PRD

```bash
# Add -R <owner/container-repo> when ## Monorepo (required — never a delivery-root remote)
gh issue create -R <owner/repo> --title "PRD: ..." --body "..." --label "prd"
gh issue edit <number> -R <owner/repo> --body "$(cat <<'EOF'
## Delivery
...
<prd body>
EOF
)"
```

Do not add `ready-for-agent`.

### `/implement` — fetch, status, comment

Same `-R` rule as `/to-prd` (container-root in monorepo).

| Operation | Command |
|-----------|---------|
| Fetch PRD/ticket | `gh issue view <N> [-R …] --comments` |
| Set in-progress | `gh issue edit <N> [-R …] --add-label in-progress` |
| Update AC checkboxes | `gh issue edit <N> [-R …] --body "..."` (checked items in `## Acceptance criteria`) |
| Comment | `gh issue comment <N> [-R …] --body "..."` (session death only — not per increment) |

Do not add `ready-for-agent`.

### `/verify` — comment on the PRD only (never on the PR)

| Operation | Command |
|-----------|---------|
| Green | `gh issue edit <N> [-R …] --remove-label in-progress --add-label ready-to-review` then `gh issue comment` (ready PR URLs) |
| Fail | leave `in-progress`; `gh issue comment` (what failed, draft PR URLs). Agent still opens/keeps a **draft** PR |

## When a skill says "publish to the issue tracker"

Create a GitHub issue using the operations above (monorepo → container-root `-R`).

## When a skill says "fetch the relevant ticket"

Run `gh issue view <number> [-R …] --comments`.
