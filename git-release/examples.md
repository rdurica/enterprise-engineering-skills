# Release examples

Reference patterns for [SKILL.md](SKILL.md). Do not copy verbatim; adapt to commits since the last tag.

**Placeholders:** `{owner}`, `{repository}`, `{registry}` (e.g. `ghcr.io/{owner}/{repository}`).  
**Remote:** `git@github.com:{owner}/{repository}.git` — resolve `{owner}` and `{repository}` from `git remote get-url origin`.

## Version bump decisions

### Patch (`0.3.0` → `0.3.1`)

Commits since `0.3.0`:

```
fix(api): stabilize CSV export ordering
fix: align PHP timezone to UTC across dev, test, and prod
chore: bump dev dependencies
```

→ **patch** — only fixes and chores, no `feat`, no breaking.

### Minor (`0.3.0` → `0.4.0`)

```
feat(api): add bulk export endpoint
fix(auth): correct token expiry edge case
```

→ **minor** — at least one `feat`, fixes do not downgrade to patch when features ship together.

### Major (`0.3.0` → `1.0.0`)

```
feat!: remove legacy slug field from API
refactor!: drop legacy /api/v0 routes
```

Or commit body contains `BREAKING CHANGE: clients must use UUID instead of slug`.

→ propose **major** in Step 3; user must approve (or pick patch/minor if they disagree).

### Large refactor, semver-ambiguous (`0.3.0` → patch or minor?)

```
refactor: migrate modules to layered layout (13 commits, 900+ files)
```

→ semver rules suggest **patch** (only `refactor`); agent may note scale in rationale. User picks `0.3.1` vs `0.4.0` in **Step 3 AskQuestion** — do not tag until they choose.

## Large minor — example-api `0.3.0`

**Repo:** `git@github.com:{owner}/example-api.git`  
**Previous tag:** `0.2.2`  
**Style:** domain subheadings under Added/Changed; Upgrade notes for migrations and runtime bumps

Structure sketch:

```markdown
## 0.3.0

Large feature release since 0.2.2: billing, events, reporting, dashboard, ...

### Added

#### Billing
- Customer tags and search caching
- Invitation workflow
...

#### Architecture (developer-facing)
- (in ### Changed)
- Module layout refactor; reference module pattern; HTTP integration tests

### Upgrade notes

1. Run all database migrations added since `0.2.2`.
2. Runtime **8.x+**; image `{registry}/{owner}/example-api:0.3.0`.
```

**After release:** if a Docker workflow runs on `release`, it publishes `{registry}/{owner}/example-api:{VERSION}` and `latest`. Remind deployers to run migrations if applicable.

## Small release — example-web `1.1.0`

**Repo:** `git@github.com:{owner}/example-web.git`  
**Previous tag:** `1.0.6`  
**Style:** shorter bullets, `### Changed` / `### Removed` / `### Fixed`, compare link at bottom

```markdown
### Changed
- Redesigned pricing section with simplified tier structure
...

### Removed
- Removed standalone /pricing page (redirects to /#pricing)

### Fixed
- Updated navigation links to use anchor /#pricing

**Full Changelog**: https://github.com/{owner}/{repository}/compare/1.0.6...1.1.0
```

## Example repo patterns

| Pattern | Remote | Typical semver | Post-release |
|---------|--------|----------------|--------------|
| Backend API | `{owner}/example-api` | `0.x.y` | Container registry `{registry}/{owner}/{repository}:{VERSION}`; run DB migrations |
| Web app | `{owner}/example-web` | `1.x.y` | Docker workflow on `release` event |
| Frontend SPA | `{owner}/example-app` | varies | Same skill; first tag defines baseline |

## Commands used (0.3.0 reference)

```bash
cd /path/to/repo
git status -sb
git tag -l --sort=-version:refname | head -1
git log 0.2.2..HEAD --pretty=format:"%s"
git tag -a 0.3.0 -m "Release 0.3.0"
git push origin 0.3.0
gh release create 0.3.0 --title "0.3.0" --notes-file /tmp/release-0.3.0.md
gh run watch {RUN_ID} --exit-status
```
