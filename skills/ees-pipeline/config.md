# Pipeline configuration

The single description of pipeline settings. Nothing needs to exist in the project: with no files at all, detection and the conversation decide everything. Branches, pushing and PRs are not settings; they follow [delivery.md](./delivery.md).

## Settings

| Key | Values | Without a setting |
|-----|--------|-------------------|
| `language` | `en` \| `cs` | see language |
| `tracker` | `github` \| `local` | detected (see Tracker detection) |
| Monorepo | `## Monorepo` section | detected (see Monorepo detection) |

### language

`/ees-analyze` writes the analysis prose, and `/ees-idea` the idea prose, in this language — title and every section body. Section headings stay English, as do identifiers, paths and HTTP contracts. `/ees-implement` and `/ees-verify` comments on the **analysis** (never on the PR) use the same language, and so does the content of the PR `## Summary`; the PR title and commit messages stay English.

A language named in the session for one analysis ("write this one in English") wins for that analysis.

When `language` is not set at any level:

- `/ees-idea` and `/ees-analyze` use the language of the conversation (`/ees-analyze` on an existing analysis: the language of that analysis) and do not ask.
- `/ees-implement`, `/ees-verify` and `/ees-complete` use the language of the analysis.

## Resolution order

Resolve each key separately. The first level that sets the key wins; a level that does not set it is skipped.

1. **Session instructions.**
2. **Project file** `docs/agents/config/workflow.md`, if it exists.
3. **Global file** `~/.config/enterprise-engineering-skills/workflow.md`, if it exists. Only `language` is taken from it; `tracker` and `## Monorepo` are properties of a project and are ignored there.
4. **Conversation, analysis or detection** as described above.

Older files may still contain `branch-owner`, `push` or `ux-review`; those keys are ignored.

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

- language: en | cs
- tracker: github | local          (project only)

## Monorepo                        (project only, optional)
- container-root: .
  remote: org/monorepo
- delivery-roots:
  - path: backend
    remote: org/backend
```

Project files contain only deviations from the global file and detection.
