# Workflow presets

Used by `/setup` when configuring `docs/agents/config/workflow.md` in a target repo.

## full-agentic

Agent manages branches and PRs, and pushes during `/verify` finalization: ready PR if green, draft PR if a gate fails.

| Setting | Value |
|---------|-------|
| Preset name | `full-agentic` |
| Tracker | `github` |
| branch-owner | `agent` |
| push | `finalize` |

## human-owned

Human creates the branch before `/implement`; agent stays on HEAD and the user manages PRs. The parent agent commits, may push during `/verify` finalization and checks CI according to the independent push policy.

| Setting | Value |
|---------|-------|
| Preset name | `human-owned` |
| Tracker | `github` (user may switch to `local`) |
| branch-owner | `human` |
| push | `finalize` |

## custom

User answers the setup questions individually (tracker, branch-owner, push). Language (`en` | `cs`) is resolved separately; reuse known session or repo settings before asking.

Push policy is independent of branch ownership. Either preset can use `push: never`. An explicit session instruction to avoid pushing takes precedence; a `human` branch-owner override alone does not disable pushing. Working subagents do not commit or push.
