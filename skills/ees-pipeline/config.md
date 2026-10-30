# Pipeline configuration

The single description of pipeline settings. Every skill that needs a setting resolves it as described here. Nothing needs to exist in the project: with no files at all, built-in defaults and detection apply.

## Settings

| Key | Values | Built-in default |
|-----|--------|------------------|
| `branch-owner` | `agent` \| `human` | `agent` |
| `push` | `finalize` \| `never` | `finalize` |
| `ux-review` | `enabled` \| `disabled` | `disabled` |
| `language` | `en` \| `cs` | none (see language) |
| `tracker` | `github` \| `local` | detected (see Tracker detection) |
| Monorepo | `## Monorepo` section | detected (see Monorepo detection) |

Built-in defaults, as they would be written in a file:

```
- branch-owner: agent
- push: finalize
- ux-review: disabled
```

### branch-owner

**agent** — prepare the Delivery branch from the remote default or reuse it, following `/ees-implement`. Preserve unfinished local work; branch switching and pull/rebase require a clean worktree.

**human** — the agent stays on the current branch and never checks out or creates one. The user creates the branch before `/ees-implement`.

Branch ownership controls checkout and PR management only. The analysis `## Delivery` names the branch; it does not carry `branch-owner` or `push`.

### push

**finalize** — the parent orchestrator may push during `/ees-verify` finalization and watch CI for the exact pushed SHA, for either branch owner. Only `branch-owner: agent` opens or updates a ready PR if green, or a draft PR if a gate fails. Human-owned PRs remain under user control.

**never** — retain verified local commits, regardless of branch ownership; skip push, CI watches and PR creation or state changes. Tracker updates on the analysis still happen unless the session restricts them too.

Push is independent of branch ownership: either owner can use either value. Working subagents never commit or push; the parent handles git operations.

### ux-review

**enabled** — `/ees-verify` Phase 3 runs after code review is green; hard gate on Critical/Major; after UX fixes re-run local tooling before Ship.

**disabled** — Ship right after code review is green.

Code review itself (Phase 2) has no switch; it always runs.

### language

`/ees-analyze` writes the analysis prose, and `/ees-idea` the idea prose, in this language — title and every section body. Section headings stay English, as do identifiers, paths and HTTP contracts. `/ees-implement` and `/ees-verify` comments on the **analysis** (never on the PR) use the same language, and so does the content of the PR `## Summary` that `/ees-verify` writes; the PR title and commit messages stay English.

When `language` is not set at any level:

- `/ees-idea`, `/ees-analyze` and `/ees-analyze-modify` use the language of the conversation (`/ees-analyze-modify`: the language of the analysis being modified) and do not ask.
- `/ees-implement`, `/ees-verify` and `/ees-complete` use the language of the analysis.

### Session override

Explicit instructions given in the session beat every file:

- `/ees-implement #N human` or `/ees-implement #N agent` sets `branch-owner` for that session only. It changes nothing else.
- "do not push" (or equivalent) sets `push: never` for the session only. It changes nothing else; tracker updates still happen.

## Resolution order

Resolve each key separately. The first level that sets the key wins; a level that does not set it is skipped.

1. **Session instructions** (see Session override).
2. **Project file** `docs/agents/config/workflow.md`, if it exists.
3. **Global file** `~/.config/enterprise-engineering-skills/workflow.md`, if it exists. Only `language`, `branch-owner`, `push` and `ux-review` are taken from it; `tracker` and `## Monorepo` are properties of a project and are ignored there.
4. **Built-in default or detection** (Settings table).

Example: a global `- language: cs` and a project file containing only `- ux-review: enabled` give `language: cs`, `ux-review: enabled`, `branch-owner: agent`, `push: finalize`.

## Tracker detection

Used when neither the session nor the project file sets `tracker` (a global `tracker` is ignored). In a monorepo, detect in the container root. First match wins:

1. `docs/agents/analysis/NNN-*.md`, `docs/agents/analysis/ideas/NNN-*.md` or `docs/agents/analysis/done/NNN-*.md` exists → `local`.
2. `git remote get-url origin` points to `github.com` → `github`.
3. Otherwise → `local`.

Only `github` and `local` exist; there is no combined mode. Tracker operations are in `{skills-root}/ees-pipeline/tracker-<tracker>.md`.

## Monorepo detection

Used when the project file has no `## Monorepo` section (a global one is ignored). Run `git submodule status` and look for nested `.git` entries (ignoring `.git/modules/`). If none are found, the repo is not a monorepo.

Otherwise:

- **Container root** is `.`, with `remote` from its `origin`. It holds GitHub issues and analyses and stays on its branch — no branch, commit, push or PR during `/ees-implement` or `/ees-verify`.
- **Delivery roots** are the found paths, in `git submodule status` order (otherwise alphabetical), each with `remote` from its own `origin`.

An explicit `## Monorepo` section in the project file replaces detection completely: only the delivery roots listed there are used. Submodule pointer bumps on the container root are not part of the pipeline.

## File format

The project file and the global file share one format. Skills read only:

- lines of the form `- <key>: <value>`, where an HTML comment after the value (`<!-- ... -->`) is stripped and surrounding whitespace trimmed;
- the `## Monorepo` section.

All other text is ignored, and so are lines with unknown keys. A file may contain any subset of keys; absent keys fall through to the next level.

```markdown
# Agent workflow

- branch-owner: agent | human
- push: finalize | never
- tracker: github | local          (project only)
- language: en | cs
- ux-review: enabled | disabled

## Monorepo                        (project only, optional)
- container-root: .
  remote: org/monorepo
- delivery-roots:
  - path: backend
    remote: org/backend
```

Project files contain only deviations from the global file and the built-in defaults.
