# Workflow presets

Used by `/setup` when configuring `docs/agents/workflow.md` in a target repo.

## full-agentic

Agent manages branches and pushes after each slice — for multi-agent handoff and automated PR flow.

| Setting | Value |
|---------|-------|
| Preset name | `full-agentic` |
| Tracker | `github` |
| branch-owner | `agent` |
| push | `each-slice` |

## human-owned

Human creates branch before `/implement`; agent stays on HEAD and does not push — user owns git and PR.

| Setting | Value |
|---------|-------|
| Preset name | `human-owned` |
| Tracker | `github` (user may switch to `local`) |
| branch-owner | `human` |
| push | `never` |

## custom

User answers the three setup questions individually. No preset defaults beyond repo auto-detection.
