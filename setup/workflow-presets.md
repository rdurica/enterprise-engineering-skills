# Workflow presets

Used by `/setup` when configuring `docs/agents/workflow.md` in a target repo.

## full-agentic

Agent manages branches and pushes after `/verify`: ready PR if green, draft PR if the gate fails.

| Setting | Value |
|---------|-------|
| Preset name | `full-agentic` |
| Tracker | `github` |
| branch-owner | `agent` |
| push | `finalize` |

## human-owned

Human creates branch before `/implement`; agent stays on HEAD and does not push — user owns git and PR.

| Setting | Value |
|---------|-------|
| Preset name | `human-owned` |
| Tracker | `github` (user may switch to `local`) |
| branch-owner | `human` |
| push | `never` |

## custom

User answers the setup questions individually (tracker, branch-owner, push). Language (`en` | `cs`) is always asked, including when a preset is chosen.
