---
name: analyze
description: >-
  Turn the current conversation into a published analysis — current state,
  change, architecture, API contracts, acceptance. Use after /align or when
  the user wants to create, write, or publish an analysis.
disable-model-invocation: true
---

# Analyze

Synthesize the align session and the codebase into a published analysis. Do not interview here — that was `/align`. Do not implement — that is `/implement`.

Write for a human who was not in the align session. They should read the analysis once and be able to explain the change without opening the diff.

Read `docs/agents/issue-tracker.md` and `docs/agents/workflow.md`. Run `/setup` in the target repo if they are missing.

Read `language` from `workflow.md` (`en` | `cs`); ask if it is missing. Everything you write in prose goes in that language: the title, every section body, and the comments on the ticket. Section headings stay English, and so do identifiers, paths, HTTP contracts and commit messages. Branch slugs are always ASCII and hyphenated, transliterated when the title is not.

All publish operations follow `docs/agents/issue-tracker.md` — GitHub or local `.scratch/`, never hardcoded `gh`.

Publish **even when `## FAQ` still has open questions**. The analysis has to be stored so the work can continue later. Each FAQ item names what it belongs to, and once it is answered you fold the answer into that section and delete the item. The ideal end state is no FAQ section at all.

## Process

1. Explore the repo if you have not already. If `docs/adr/` exists, respect those decisions.

2. Before drafting, read [analysis-template.md](analysis-template.md) for writing rules, section structure, Acceptance examples and the shorter bug variant. Write the analysis from that template, then publish it. On GitHub the only label is `analysis` — create it if it does not exist, and never add `ready-for-agent`. Locally the analysis is `.scratch/analysis/NNN-<slug>.md` with no Status line.

3. After publishing, prepend `## Delivery` — edit the issue body on GitHub, update the file locally:

```markdown
## Delivery

- Ticket: [AB#4821](https://dev.azure.com/org/project/_workitems/edit/4821)
- Kind: feature | bug | chore
- Branch: `feature/4821-group-pricing`
```

**Ticket** is the number this work is tracked under, as a clickable link whenever you have a URL. An external tracker wins — Azure DevOps, Jira, Redmine, whatever the project uses. Take the ID or link from the align session, and ask for it when the work clearly came from a ticket but nobody named it. Without an external ticket, use the analysis's own number: on GitHub the issue itself, linked as `Ticket: [#<N>](<issue url>)`; locally the plain file number `NNN`.

**Branch** is `feature/<ticket>-<short-slug>` and reuses that same number, so branch and ticket never drift apart. The slug comes from the title: lowercase, hyphenated, ASCII, around 30 characters.

Commits and the PR keep referencing the GitHub analysis issue as `#N`, because that is the number GitHub autolinks. The external ticket travels in the `Ticket:` line.

For **bugs**, set `Kind: bug` and use the shorter bug sections.

## Publishing

### Local tracker publish

When the active backend is Local Markdown, follow the `/analyze` operations in `docs/agents/issue-tracker.md`:

1. Compute the next `NNN` as described there — scan `.scratch/analysis/` and `.scratch/analysis/done/`, never reuse an ID.
2. Take `<slug>` from the analysis title: lowercase, hyphenated, ASCII, transliterated if needed.
3. Create `.scratch/analysis/NNN-<slug>.md` with Kind, Delivery (branch `feature/<ticket>-<short-slug>`, where the ticket falls back to `NNN`) and the analysis body. No Status line.

Bug fast-path — a ticket with Acceptance rather than a full analysis — uses the same path and ID scan with `Kind: bug`.

### GitHub publish

When the backend is GitHub, follow the `/analyze` operations in `docs/agents/issue-tracker.md`.

**Monorepo:** if `workflow.md` has a `## Monorepo` section, or nested git repos exist, create the analysis issue on the **container-root** repo only — `gh … -R <owner/container-repo>` from that remote. Never publish an analysis into a delivery-root repository.

After publishing, tell the user the next step is `/implement` on this analysis, once they have reviewed it.
