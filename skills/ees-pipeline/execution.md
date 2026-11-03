# Execution contract

How the main session delegates to the pack's agents and keeps its own context lean. Read by `/ees-implement`, verify, `/ees-code-review`, `ees-ux-review`, `/ees-change` and the testing skills whenever they delegate work.

Give each worker a fresh, scoped context: its phase, the analysis reference (`gh issue view <N>`, with `-R` in a monorepo, or the local path) or, outside an analysis, the brief, the names of its Acceptance items and of the Architecture units of its cluster, allowed paths, dependencies, skill paths and project commands. The worker reads those items, the whole units (Path, Files, Follow, Seams, prose) and the relevant Change/API Contracts verbatim from the analysis itself; the parent neither copies nor paraphrases them, because every copied line is expensive parent output. Link source files rather than copying the whole conversation. `Files` is a guide, not the allowed paths, which the parent still sets. Workers return changed files, test results, completed items and blockers; they do not commit, push, change branches or manage PRs.

The parent primarily coordinates and delegates code/test work. A trivial one-file follow-up such as an import or typo may be fixed directly; substantial work goes to workers.

**Keep the main window lean.** Every turn resends its whole context. Review worker results from their report and `git diff --stat`; read the full diff only for files where the report, the stat or a failing check gives reason to doubt it. Pass workers paths and bases, not pasted diffs or logs.

**Agents.** Delegate through the Agent tool with these `subagent_type` values. Each agent definition fixes its model and effort, so the expensive orchestrator model only plans, reviews and commits:

| Agent | Work | Claude model / effort |
|-------|------|-----------------------|
| `ees-test-writer` | Phase A tests, justified test corrections | sonnet / high |
| `ees-implementer` | Phase B production code, delegated repairs | sonnet / medium |
| `ees-check-runner` | Project tests, lint and type checks; compact summary | haiku / low |
| `ees-functional-reviewer` | Functional review in `/ees-verify` (spec and standards) | sonnet / medium |
| `ees-code-reviewer` | `/ees-code-review` findings (read-only) | opus / medium |
| `ees-ux-reviewer` | `/ees-ux-review` findings (read-only) | sonnet / high |

Models for other harnesses are in `agents.toml`.

The parent runs every test, lint and type check through `ees-check-runner`, never directly, so logs stay out of the main window. Workers run their own cluster tests.

**Checks in tiers.** After a wave or a repair, run only the tests and tooling for the affected paths. Run the full documented suite once at the start of `/ees-verify` Functional and once before Ship, the latter only when code changed since the last full run; in `ees-change` once after implementation.

**Escalation.** When a worker returns the same cluster unfinished or wrong twice, start a new one with `model: "opus", effort: "low"` and a sharper brief (failure evidence, the decision it missed). If that also fails, take the cluster with `model: "opus"` at its default effort, or mark the cluster blocked when the cause is an undecided contract. Do not escalate on the first attempt. The same applies to `ees-code-reviewer`: when a cycle misses an issue that a later check or cycle exposes, run the next cycle with `effort: "high"`.

Where the harness cannot switch a worker's model (opencode: `task` has no model parameter), skip the new-worker step: after the second failure the parent takes the cluster, or marks it blocked when the cause is an undecided contract. `ees-code-reviewer` in opencode keeps the same agent and the next cycle gets a sharper brief.

Committed tests are the contract. Later corrections require a concrete test defect, missing regression coverage or an agreed contract change, parent review and a separate test commit. Never weaken assertions to make faulty code pass. These rules apply to verify and review too.
