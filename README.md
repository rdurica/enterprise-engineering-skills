# Enterprise Engineering Skills

Claude Code skills and agents for changes in an existing codebase. You make the decisions; agents write the tests and code, review them and deliver the result.

The goal is not just working code. Whoever owns the project should understand the change well enough to explain it, so behaviour and boundaries are agreed first and implemented second. Trivial fixes skip the pipeline.

## Quick start

```bash
git clone git@github.com:rdurica/enterprise-engineering-skills.git ~/Projects/enterprise-engineering-skills
~/Projects/enterprise-engineering-skills/install.sh
```

`install.sh` links every skill into `~/.claude/skills/` and `~/.agents/skills/` (read by Codex and Cursor), and every agent into `~/.claude/agents/`, `~/.codex/agents/`, `~/.cursor/agents/` and `~/.config/opencode/agents/` (see [Agents for each provider](#agents-for-each-provider)). It never overwrites a different skill or agent with the same name, removes dangling links left by deleted ones, points the pack's `core.hooksPath` at `.githooks`, and `--dry-run` shows the plan. When opencode is installed it also merges the pack's model keys into `opencode.json`; the original is kept as `opencode.json.bak` and `--dry-run` prints the changes. Afterwards `git pull` is enough; re-run the script when a skill or agent is added, renamed or removed. After a release that renames skills or agents, run `install.sh` again and start a new session: the old links are dangling, `cleanup` removes them and the new `ees-` names are linked. Old folders copied by hand are not links — delete them yourself.

A project works without any configuration: the tracker and monorepo are detected and every other setting has a built-in default. Optionally create your personal defaults in the global file `~/.config/enterprise-engineering-skills/workflow.md`, either through `/ees-setup` or by hand:

```markdown
# Agent workflow

- branch-owner: agent
- push: finalize
- language: en
- ux-review: disabled
```

## Workflow

You take part in only a few steps. Everything after `/ees-implement #N` is a chain of agents: each one gets a fresh context, finishes one job and hands its result to the next. The main session sits between them, reviews every handoff and makes the commits.

```mermaid
flowchart TD
    Idea(["<b>/ees-idea</b><br/>note a change for later"])
    Analyze(["<b>/ees-analyze</b><br/>agree on the change"])
    Modify(["<b>/ees-analyze-modify</b><br/>revise an analysis"])
    Ideas[("<b>ideas</b><br/>label idea · ideas/")]
    Analyses[("<b>analyses</b><br/>label analysis")]
    Implement(["<b>/ees-implement #N</b><br/>after your review"])

    subgraph Auto["automatic"]
        direction TB
        testWriter["<b>ees-test-writer</b><br/>failing tests first"]
        implementer["<b>ees-implementer</b><br/>code until tests pass"]
        functional["<b>ees-functional-reviewer</b><br/>matches the analysis?"]
        codeReview["<b>ees-code-reviewer</b><br/>fixes bugs and craft"]
        ux["<b>ees-ux-reviewer</b><br/>walks the UI"]

        testWriter --> implementer --> functional --> codeReview --> ux
        functional -. "fix list" .-> implementer
    end

    Ready(["<b>ready-to-review</b><br/>your turn · /ees-complete"])
    Attention(["<b>needs-attention</b><br/>you decide, then rerun"])
    Done[("<b>done</b><br/>closed · done/")]

    Idea -. "writes" .-> Ideas
    Analyze <-. "when due" .-> Ideas
    Analyze -- "publishes" --> Analyses
    Modify <-- "revises" --> Analyses
    Analyses -- "reads" --> Implement --> testWriter
    ux --> Ready -- "merged" --> Done
    Auto -. "blocked" .-> Attention

    classDef human fill:#dbeafe,stroke:#1d4ed8,color:#1e3a8a
    classDef agent fill:#ffedd5,stroke:#c2410c,color:#7c2d12
    classDef optional stroke-dasharray:5 5
    classDef store fill:#f3f4f6,stroke:#4b5563,color:#111827
    classDef ready fill:#dcfce7,stroke:#15803d,color:#14532d
    classDef blocked fill:#fee2e2,stroke:#b91c1c,color:#7f1d1d
    class Idea,Analyze,Modify,Implement human
    class Idea,Ideas,ux optional
    class testWriter,implementer,functional,codeReview,ux agent
    class Ideas,Analyses,Done store
    class Ready ready
    class Attention blocked
    style Auto fill:#f9fafb,stroke:#9ca3af
```

**Blue** = you · **orange** = agents · **grey** = where ideas and analyses are stored (GitHub issues or `docs/agents/analysis/`) · **dashed** = optional. `/ees-implement` continues into `/ees-verify` on its own. Every step runs tests, lint and type checks through `ees-check-runner`, which returns only the failures.

0. **`/ees-idea`** (optional) — write a change down as a short idea: Goal, Change and optional `Depends on`. No code is read in depth and no decisions are settled; the detailed analysis comes later with **`/ees-analyze #N`** on the same issue, once the change is due and against the code as it is then.
1. **`/ees-analyze`** — you and Claude explore the code and settle decisions one question at a time. Once you confirm the list of decisions, Claude turns them into a published analysis: current state, change, architecture, API contracts and Acceptance, with each decision and its rejected alternative in Further Notes.
2. **You review it** and run **`/ees-implement #N`** (or a local analysis path). The agents in the diagram take over: tests first, committed before any code, then the code, the functional review against the analysis, the code review and, if enabled, the UX review. It ends as `ready-to-review`, or as `needs-attention` when a decision is yours.

3. **You review the delivery** and run **`/ees-complete #N`**. For agent-owned delivery with an open PR it checks that CI is green, nothing is a draft and no changes are requested, then rebase-merges the PR, deletes the branch, closes the issue without `ready-to-review` and pulls `main` locally. Human-owned delivery, or delivery without a PR, is left to you and `/ees-complete` does nothing.

To **plan several follow-up changes**, write each as an idea and give it `Depends on: #41, #42` in its Delivery. `/ees-idea` proposes dependencies from the open ideas and analyses and warns about duplicates. `/ees-analyze #N` on an idea whose dependency is still open stops and asks whether to continue; `/ees-implement` refuses an idea and an analysis with an unmet dependency, with no override. A dependency is met when its issue is closed (locally, its file is in `done/`).

A **simple bug** skips step 1: a ticket with Acceptance goes straight to `/ees-implement`.

**Work without an analysis** — "add an endpoint", "fix this bug", "refactor that module" — starts the **`ees-change`** skill on its own when the change adds behaviour or touches more than one file. It writes a short brief, then runs `ees-test-writer`, `ees-implementer`, `ees-check-runner` and `ees-code-reviewer` the same way, and commits only when you ask. A typo or one-line fix is edited directly; a large or open-ended change gets a suggestion to run `/ees-analyze` first.

**Decisions** live only in `## Further Notes` of each analysis, each with its rejected alternative. The pack writes and reads no ADRs.

To **change an existing analysis** — before `/ees-implement`, or after it when a change request arrives — run **`/ees-analyze-modify #N`** with what should be different. Claude checks the analysis, decisions in earlier analyses and any committed code for what the change contradicts, names the risks and agrees each one with you, then rewrites the analysis in place so it reads as one consistent state. Changed Acceptance items are unchecked. For an analysis that is not yet implemented only the text changes; once work exists, `## Revisions` at the end records the modification as an unchecked item (an unchecked one is updated instead of adding another) and `/ees-implement #N` continues on the same branch with only the unchecked items, then checks the revision off.

## Agents

| Agent | Used by | What it does | Model |
|-------|---------|--------------|-------|
| `ees-test-writer` | `/ees-implement`, `ees-change` | Writes tests for one slice of the change and proves they fail | Sonnet, high |
| `ees-implementer` | `/ees-implement`, `ees-change`, repairs | Writes production code against the committed tests | Sonnet, high |
| `ees-functional-reviewer` | `/ees-verify` | Checks Acceptance, scope, API contracts, test coverage and documented project rules (read-only) | Sonnet, medium |
| `ees-code-reviewer` | `/ees-code-review`, `ees-change` | Fixes bugs and security issues, then leftovers, duplication and readability | Sonnet, medium |
| `ees-ux-reviewer` | `/ees-ux-review` | Walks the affected screens in a browser; checks accessibility | Sonnet, medium |
| `ees-check-runner` | all pipeline skills, any full check run | Runs tests, lint and type checks; returns only failures | Haiku, low |

Agents never commit, push or open PRs; the main session does. Tests are committed before the code, and assertions are never weakened to make code pass.

### Agents for each provider

Each agent is written once and built for Claude Code, Codex, Cursor and opencode:

- `agents/<name>.md` holds the `name`, the `description` and the instructions.
- `agents.toml` holds every agent's settings for every provider: shared `readonly` and `skills`, then `claude` (`model`, `effort`, `tools`, `color`), `codex` (`model`, `effort`), `cursor` (`model`, the full Cursor ID with effort, e.g. `grok-4.7-medium`) and `opencode` (`model` as `provider/model`, optional `variant`). Leaving out a provider's table skips the agent for that provider.
- `scripts/build-agents` writes `generated/<provider>/agents/`, which is committed and linked by `install.sh`. Never edit `generated/` by hand; the pre-commit hook runs `scripts/build-agents --check` and refuses a commit where it is out of date.

```toml
[ees-check-runner]
readonly = true
claude = { model = "haiku", effort = "low", tools = ["Bash", "Read", "Grep", "Glob"], color = "cyan" }
codex = { model = "gpt-6-luna", effort = "low" }
cursor = { model = "grok-4.7-low" }
opencode = { model = "opencode-go/deepseek-v4.1-flash" }
```

Claude preloads `skills`; Codex and Cursor get a first line telling the agent to read them. opencode takes `model` and a separate `variant` (`model: …#max` is ignored there) and turns `readonly` into `edit: deny`. Cursor enforces `readonly`; Codex cannot restrict tools per agent, so there read-only roles rely on their instructions. The main Codex session keeps the model from `~/.codex/config.toml`. Cursor reads skills from `~/.agents/skills/` and `~/.claude/skills/`, so nothing is linked into `~/.cursor/skills/`. opencode reads skills from `~/.claude/skills/` and `~/.agents/skills/` too and starts them with `@ees-analyze #N` instead of a slash command.

## Models

Opus is used where decisions are made; the pipeline and its agents run on Sonnet or Haiku. Keep **Opus** as your default model: unpinned work — `ees-change`, debugging, questions — is mostly judgment and costs little.

In opencode every skill runs on the main session (`claude-agent/opus`), which spends Claude tokens only there; pack agents and built-in helpers run on `opencode-go/deepseek-v4.1-flash`. The `variant` is a separate setting; `-` means none. `max` is reserved for writing changes (`ees-implementer`, `ees-test-writer`), reviewers run on `high`, and the check runner plus the built-in `general`/`explore` run on `low`, where the quality difference is smallest.

| Skill or agent | Claude Code | opencode |
|----------------|-------------|----------|
| `/ees-analyze`, `/ees-analyze-modify`, `/ees-discuss` | Opus | `claude-agent/opus` |
| `/ees-idea` | Sonnet, medium | `claude-agent/opus` |
| `/ees-implement` | Sonnet, high | `claude-agent/opus` |
| `/ees-verify`, `/ees-code-review` | Opus, medium when run directly; inside `/ees-implement` they follow its session | `claude-agent/opus` |
| `/ees-ux-review`, `/ees-git-release`, `/ees-monorepo-update` | Sonnet, medium | `claude-agent/opus` |
| `/ees-setup` | Sonnet, high | `claude-agent/opus` |
| `/ees-commit`, `/ees-complete` | Haiku, low | `claude-agent/opus` |
| `ees-change` | your selected model | `claude-agent/opus` |
| `ees-test-writer`, `ees-implementer` | Sonnet, high | `opencode-go/deepseek-v4.1-flash`, variant `max` |
| `ees-functional-reviewer`, `ees-code-reviewer`, `ees-ux-reviewer` | Sonnet, medium | `opencode-go/deepseek-v4.1-flash`, variant `high` |
| `ees-check-runner` | Haiku, low | `opencode-go/deepseek-v4.1-flash`, variant `low` |
| `general`, `explore` (built-in) | - | `opencode-go/deepseek-v4.1-flash`, variant `low` |
| `compaction`, `title`, `summary` (built-in) | - | `opencode-go/deepseek-v4.1-flash`, variant `-` |

- **Opus only for decisions.** An analysis decides what every later step builds and checks, so it gets the strongest model; the pipeline then follows the agreed analysis.
- **One task per conversation.** Switching models mid-conversation throws away the prompt cache, so start each `/ees-analyze` and each `/ees-implement` in a fresh conversation.
- **opencode prerequisites.** The `claude-agent` provider needs Claude Code >= 2.1.248 logged in with `claude auth login`. opencode reads `AGENTS.md`, not `CLAUDE.md`, so global rules from `~/.claude/CLAUDE.md` do not apply there. `/ees-implement` has no model to escalate to in opencode; the main session takes over a failing cluster.

How the pipeline keeps its own cost down — summaries instead of logs, checks in tiers, delta reviews and escalation on evidence — is in the Execution contract of [`ees-implement`](skills/ees-implement/SKILL.md#execution-contract).

Change a role's model or effort in `agents.toml` (see [Agents for each provider](#agents-for-each-provider)); opencode's main session and built-in agents are set in `config/opencode.json`. `CLAUDE_CODE_EFFORT_LEVEL` overrides every Claude `effort`.

## Status

With the local tracker there is no status: an analysis in `docs/agents/analysis/` is active, an idea in `docs/agents/analysis/ideas/` is waiting for `/ees-analyze`, and a green `/ees-verify` moves it to `done/`. Blockers are noted under `## Comments`. On GitHub, the issue carries these labels:

| Label | Meaning |
|-------|---------|
| `idea` | An idea not yet analyzed; `/ees-analyze #N` converts it to `analysis`, `/ees-implement` refuses it |
| `in-progress` | `/ees-implement` is running or was interrupted; rerun it to resume |
| `needs-attention` | A blocker needs your decision; resolve it and rerun `/ees-implement` |
| `ready-to-review` | All gates passed; your turn to review, then `/ees-complete` |

Notes go on the analysis, never on the PR.

## Configuration

No configuration is required. Each setting has a built-in default (agentic mode: the agent manages the branch and PR, pushes at finalize and watches CI):

| Key | Built-in value | Options |
|-----|----------------|---------|
| `branch-owner` | `agent` | `agent` (agent manages branch and PR) · `human` (stays on your branch, PRs are yours) |
| `push` | `finalize` | `finalize` (push and watch CI) · `never` (local commits only) |
| `ux-review` | `disabled` | `enabled` · `disabled` |
| `language` | conversation language for `/ees-idea`, `/ees-analyze` and `/ees-analyze-modify`; the analysis language for `/ees-implement`, `/ees-verify` and `/ees-complete` | `en` · `cs` for analysis prose, comments and the PR Summary |
| `tracker` | detected | `github` · `local` |
| Monorepo | detected | `## Monorepo` section (project file only) |

Each key is resolved separately and the first level that sets it wins: session (`/ees-implement #N human|agent`, "don't push") → project file `docs/agents/config/workflow.md` → global file → built-in value or detection. The project file holds only deviations and is the only place for `tracker` and `## Monorepo`. Detection and the file format are described in [`ees-pipeline/config.md`](skills/ees-pipeline/config.md). `/ees-setup` is optional: it checks the installation and writes the global file or project deviations.

Project-specific rules go in the overlays `docs/agents/config/verify.md`, `code-review.md` and `ux-review.md`. Local-only skills go in the gitignored `skills/personal/`.

## Other skills

Most skills run only as slash commands. Claude starts these on its own when the request fits: `ees-change` (implementation without an analysis), `ees-implement` (a request naming an analysis), `ees-discuss` (weighing options), `ees-tdd`, `ees-integration-tests`, `ees-commit` and `ees-git-release`.

- **`ees-change`** — implementation without an analysis through the same agents; see [Workflow](#workflow).
- **`/ees-discuss`** — talk a question through with options and trade-offs; changes nothing.
- **`/ees-commit`** — Conventional Commits from the diff; `/ees-commit push` also pushes.
- **`/ees-git-release`** — semver tag and GitHub release with a changelog.
- **`/ees-monorepo-update`** — bump submodules or check out an analysis branch in every delivery root.
- **`ees-tdd`**, **`ees-integration-tests`** — testing playbooks used by `ees-test-writer`.
- **`ees-pipeline`** — hidden shared library (not invokable): built-in defaults, resolution order, detection and the GitHub and local tracker instructions that the pipeline skills read.
