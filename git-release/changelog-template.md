# Changelog template (GitHub release body)

Fill placeholders, remove empty sections, keep **English**. Save as `/tmp/release-{VERSION}.md`.

```markdown
## {VERSION}

{One-sentence summary of the release since {PREVIOUS_TAG}. Mention scale: patch fixes, new features, breaking changes, etc.}

### Added

#### {DomainArea1}
- {User-facing addition}
- {Another item}

#### {DomainArea2}
- {Item}

### Changed

#### {DomainArea}
- {Non-breaking behavior or API change}

### Fixed

- {Bug fix with brief impact}
- {Another fix}

### Removed

- {Deprecated or removed feature — omit section if none}

### Upgrade notes

1. {Migration, dependency, or deploy step}
2. {Docker image, env var, client breaking change}
3. {Optional third note}

**Full Changelog**: https://github.com/{OWNER}/{REPO}/compare/{PREVIOUS_TAG}...{VERSION}
```

## Section guidelines

| Section | Use when |
|---------|----------|
| **Added** | New endpoints, features, settings, integrations |
| **Changed** | Behavior changes, refactors affecting operators, non-breaking API tweaks |
| **Fixed** | Bug fixes |
| **Removed** | Deleted routes, fields, pages, env vars |
| **Upgrade notes** | DB migrations, PHP/runtime bumps, breaking client changes, new required config |

## Style

- Bullet per logical change; merge related commits into one bullet
- Prefer domain subheadings (`#### Membership`, `#### Events`) for large releases
- For small patch releases, flat bullets under `### Fixed` are enough
- Name stable API fields and endpoints when breaking (`slug`, `IBAN`, route paths)
- Do not paste 50+ commit lines; synthesize for readers

## Compare link

Replace `{OWNER}`, `{REPO}`, `{PREVIOUS_TAG}`, `{VERSION}` from:

```bash
git remote get-url origin   # → github.com:OWNER/REPO.git
git tag -l --sort=-version:refname | head -1   # → PREVIOUS_TAG
```

Omit the **Full Changelog** line only if the user prefers a minimal note (default: include it).
