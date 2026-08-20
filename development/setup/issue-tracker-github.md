# Issue tracker: GitHub

Issues and PRDs live as GitHub issues. Use the `gh` CLI.

Infer repo from `git remote -v` when run inside a clone.

Also read `docs/agents/workflow.md` for branch-owner and push defaults.

## Conventions

- **Create:** `gh issue create --title "..." --body "..." --label "..."`
- **Read:** `gh issue view <number> --comments`
- **Edit body:** `gh issue edit <number> --body "..."`
- **List:** `gh issue list --state open --json number,title,body,labels`
- **Comment:** `gh issue comment <number> --body "..."`
- **Labels:** `gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **Close:** `gh issue close <number> --comment "..."`

## Labels

| Label | Set by | Meaning |
|-------|--------|---------|
| `prd` | `/to-prd` | This issue is a PRD |
| `ready-for-agent` | human, after validating the PRD | Auto-trigger may start `/implement`. Agent never adds this |
| `in-progress` | `/implement` | Agent is working |
| `ready-to-review` | `/verify` (green) | PR open, waiting for human review |

User invoked `/implement` → run it (do not require `ready-for-agent`). Stop if `ready-to-review`.

Auto-start without the user → only if `ready-for-agent` or already `in-progress`.

**Lifecycle:** `prd` → human adds `ready-for-agent` (optional if they call `/implement`) → `in-progress` → `ready-to-review`. Session died → leave `in-progress`; re-run `/implement`.

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
gh issue create --title "PRD: ..." --body "..." --label "prd"
gh issue edit <number> --body "$(cat <<'EOF'
## Delivery
...
<prd body>
EOF
)"
```

Do not add `ready-for-agent`.

### `/implement` — fetch, status, comment

| Operation | Command |
|-----------|---------|
| Fetch PRD/ticket | `gh issue view <N> --comments` |
| Set in-progress | `gh issue edit <N> --add-label in-progress` |
| Update AC checkboxes | `gh issue edit <N> --body "..."` (checked items in `## Acceptance criteria`) |
| Comment | `gh issue comment <N> --body "..."` |

Do not add `ready-for-agent`.

### `/verify` — finalize PRD

| Operation | Command |
|-----------|---------|
| Finalize PRD | `gh issue edit <N> --remove-label in-progress --add-label ready-to-review` |
| Comment | `gh issue comment <N> --body "..."` (PR URLs) |

## When a skill says "publish to the issue tracker"

Create a GitHub issue using the operations above.

## When a skill says "fetch the relevant ticket"

Run `gh issue view <number> --comments`.
