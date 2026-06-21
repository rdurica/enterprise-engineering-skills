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
- **List slices for PRD:** `gh issue list --label "epic-<N>" --state open --json number,title,body`

## Labels

| Label | On | Meaning |
|-------|-----|---------|
| `prd` | PRD issue | Meta — identifies a PRD |
| `needs-slicing` | PRD after `/to-prd` | Waiting for `/to-issues` |
| `sliced` | PRD during implementation | Slice issues exist |
| `epic-<N>` | PRD + all its slices | Group under parent issue `#N` |
| `ready-for-implementation` | **PRD only** (or single-slice bug ticket) | Triggers next agent session |
| `ready-to-review` | PRD after all slices done | PR open, waiting for human review |
| `in-progress` | PRD while agent works | Prevents double-trigger; removed on handoff |

**Slice issues never get `ready-for-implementation`.** Trigger label lives on the PRD.

**Handoff cycle:** `ready-for-implementation` → agent starts → `in-progress` → slice done → `ready-for-implementation` again (or `ready-to-review` when finished).

**Deprecated:** `ready-for-agent` — do not use.

## PRD Delivery section

After `/to-prd`, prepend to issue body:

```markdown
## Delivery

- Branch: `feature/prd-<number>-<short-slug>`
- Epic label: `epic-<number>`
- Branch owner: agent | human    # default from docs/agents/workflow.md
- Push: each-slice | finalize | never
```

## Skill operations

### `/to-prd` — publish PRD

```bash
gh issue create --title "PRD: ..." --body "..." --label "prd,needs-slicing"
gh issue edit <number> --add-label "epic-<number>"
gh issue edit <number> --body "$(cat <<'EOF'
## Delivery
...
<prd body>
EOF
)"
```

### `/to-issues` — publish slices + ready PRD

```bash
gh issue create --title "..." --body "..." --label "epic-<parent>"
# repeat per slice
gh issue edit <parent> --remove-label needs-slicing --add-label sliced,ready-for-implementation
```

### `/implement` — fetch, status, close, comment

| Operation | Command |
|-----------|---------|
| Fetch PRD/ticket | `gh issue view <N> --comments` |
| List slices | `gh issue list --label "epic-<N>" --state open --json number,title,body` |
| Set in-progress | `gh issue edit <N> --remove-label ready-for-implementation --add-label in-progress` |
| Handoff (more slices) | `gh issue edit <N> --remove-label in-progress --add-label ready-for-implementation` |
| Close slice | `gh issue close <sliceNum> --comment "..."` |
| Comment | `gh issue comment <N> --body "..."` |
| Finalize PRD | `gh issue edit <N> --remove-label in-progress,sliced,ready-for-implementation --add-label ready-to-review` |

### Single-slice mode (bug fast-path)

When PRD/ticket has `ready-for-implementation` but **no open slice issues** under `epic-<N>`, `/implement` reads acceptance criteria from the PRD/ticket body directly.

## When a skill says "publish to the issue tracker"

Create a GitHub issue using the operations above.

## When a skill says "fetch the relevant ticket"

Run `gh issue view <number> --comments`.
