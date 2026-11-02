# Subagent tool for Pi

Pi has no built-in subagents: delegating to another agent with its own context window is an example
extension. When Pi is selected, `install.sh` links this directory into
`~/.pi/agent/extensions/subagent/`, where Pi loads it as the `subagent` tool; the agents it
dispatches to are the `~/.pi/agent/agents/*.md` files built from `agents/<name>.md` and
`agents.toml` (`generated/pi/agents/`).

Vendored from the Pi release, `examples/extensions/subagent/` (`index.ts`, `agents.ts`). One local
change: the tool description lists the installed user agents with the first sentence of their
description, so the model dispatches by name instead of discovering the names through a failed call.
`README` of the upstream example documents modes, output display and limits.

Frontmatter of an agent file:

```markdown
---
name: ees-check-runner
description: What the agent does and when to use it
model: opencode-go/deepseek-v4.1-flash:low
tools: read, bash
---
```

- `model` accepts `provider/id` plus Pi's `:<thinking>` suffix, which is how `variant` from
  `agents.toml` reaches the agent. Without `model` the agent inherits the dispatching model and
  thinking level.
- `tools` is an allowlist of Pi tools (`read`, `bash`, `edit`, `write`); leaving it out gives the
  agent every tool, which is how the pack writes `readonly = false` roles.
- The body is appended to Pi's own system prompt, so a delegated agent keeps the harness rules and
  only gains its role instructions.
- Project agents (`.pi/agents/`) are only used with `agentScope: "both"` or `"project"`; the default
  is the user-level directory.
