---
name: git-release
description: >-
  Creates semver git tags and GitHub releases with English changelogs.
  Proposes a semver bump (patch/minor/major) and always asks the user to
  approve or change the tag version before tagging. Use when the user asks
  for a release, tag, version bump, or GitHub release notes.
---

# Git release

Playbook for **semver tag + GitHub release** with an English changelog. Works across any git repo with `gh` CLI access.

Repo-specific notes: [examples.md](examples.md). Changelog skeleton: [changelog-template.md](changelog-template.md).

## When to use

- User asks for a release, tag, version bump, or changelog for GitHub
- After a feature batch is merged to `main` and ready to ship

## Workflow overview

1. Preflight checks
2. Resolve latest semver tag and analyze commits since it
3. Propose version bump (patch / minor / major) with one-line rationale
4. **`AskQuestion` (mandatory):** user approves proposed tag or picks another — **stop here until confirmed**
5. Write English changelog → `/tmp/release-{VERSION}.md` (use the **confirmed** version)
6. Annotated tag, push, `gh release create`
7. Watch release-triggered CI if present; report URLs to user

Respond to the user in their language; **release notes body is always English**.

## Step 1: Preflight

Run from the **correct repo root** (workspace or path the user named):

```bash
git status -sb
git branch --show-current
git rev-parse HEAD
git remote get-url origin
```

Requirements:

- Clean working tree (no uncommitted changes)
- On default branch (`main` or `master`), synced with `origin` (no unpushed commits ahead)
- `gh` authenticated for the remote owner/repo
- Proposed tag does not exist: `git tag -l {VERSION}`

If preflight fails, stop and tell the user what to fix. Do not tag on a dirty or diverged branch.

## Step 2: Version bump

```bash
git tag -l --sort=-version:refname | head -1
git log {LAST_TAG}..HEAD --oneline
git log {LAST_TAG}..HEAD --pretty=format:"%s"
```

### Bump rules (when user does not specify a version)

Parse commit subjects since `{LAST_TAG}`:

| Signals | Bump | Example `0.3.0` → |
|---------|------|-------------------|
| Only `fix`, `chore`, `docs`, `test`, `style`, `refactor` (no breaking, no new user-facing features) | **patch** | `0.3.1` |
| Any `feat` or clear new capability / API extension without breaking | **minor** | `0.4.0` |
| Breaking: `BREAKING CHANGE` footer, `type!:` (`feat!:`, `fix!:`), removed public API/fields, breaking migrations | **major** | `1.0.0` |

Tie-breakers:

- Both `feat` and `fix` since last tag → **minor** (features dominate)
- Large `refactor` / architecture-only batch with no `feat` but high operator impact → **state in rationale**; default semver rule may still be patch — user decides in Step 3
- Ambiguous → pick best-guess bump, explain assumption in Step 3 prompt

### User-specified version in the request

If the user already names a version (e.g. `/git-release 0.5.0`), treat that as the **proposal** — still run **Step 3** (`AskQuestion`) so they can confirm or change it. Do not skip confirmation because the version was stated upfront.

## Step 3: Version confirmation (mandatory — all releases)

**Always** use `AskQuestion` after Step 2 and **before** changelog, tag, or `gh release create`. Never tag autonomously.

Present in the prompt (user's language is fine for the question text):

- Latest tag: `{LAST_TAG}`
- Proposed tag: `{VERSION}` (bump type: patch / minor / major)
- One-line rationale (commit signals + any scale notes, e.g. large refactor)

**Options** (adapt labels to context; include at least):

1. **Approve** proposed `{VERSION}`
2. **Use a different version** — if the tool cannot collect free text, list sensible alternatives (e.g. patch vs minor when ambiguous) plus cancel
3. **Cancel** — abort release

If the user picks a different version, re-run `git tag -l {VERSION}` and use that value for Steps 4–7.

**Never** create any tag or GitHub release without explicit user approval of the final version string.

## Step 4: Changelog (English)

1. Read [changelog-template.md](changelog-template.md)
2. Group changes **by domain** (not a raw commit dump)
3. Use sections: `### Added`, `### Changed`, `### Fixed`, `### Removed` (optional), `### Upgrade notes` (migrations, runtime, breaking clients)
4. Opening line: scope since `{PREVIOUS_TAG}` and nature of the release
5. Save to `/tmp/release-{VERSION}.md` — do not commit this file unless the user asks

See [examples.md](examples.md) for large-minor vs small-release styles.

## Step 5: Tag and GitHub release

```bash
git tag -a {VERSION} -m "Release {VERSION}"
git push origin {VERSION}
gh release create {VERSION} --title "{VERSION}" --notes-file /tmp/release-{VERSION}.md
```

- Use `--draft` or `--prerelease` only if the user explicitly requests it
- Do not `git push --force`, amend tags, or commit unless asked
- Do not add `CHANGELOG.md` to the repo unless the user asks

## Step 6: Verify CI

```bash
gh run list --limit 5
gh run watch {RUN_ID} --exit-status
```

If `.github/workflows/*` has `on: release`, wait for the build (e.g. Docker push to GHCR). Report:

- Release URL: `https://github.com/{owner}/{repo}/releases/tag/{VERSION}`
- CI run URL and conclusion
- Repo-specific deploy hints from [examples.md](examples.md) when relevant

## Forbidden

- Tag/release on dirty or unpushed `main`
- Tag/release **without** `AskQuestion` version confirmation (any bump: patch, minor, major)
- Czech (or non-English) text in GitHub release notes
- Force-push tags or rewrite published tags without explicit user request

## Checklist

Copy and track progress:

```
- [ ] Preflight: clean tree, main synced, origin verified
- [ ] Last tag identified; commits analyzed
- [ ] Version proposed (patch/minor/major) with rationale
- [ ] User confirmed final tag via AskQuestion (approve / different / cancel)
- [ ] English changelog written to /tmp/release-{VERSION}.md
- [ ] Tag pushed; gh release published
- [ ] Release CI watched (if applicable); URLs reported
```
