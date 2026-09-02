---
name: analyze
description: >-
  Turn the current conversation into a published analysis — current state,
  change, architecture, API contracts, acceptance. Use after /align or when
  the user wants to create, write, or publish an analysis.
disable-model-invocation: true
---

# Analyze

Synthesize the align session and codebase into a published analysis. Do NOT interview (no seam checks). Do NOT implement — that is `/implement`.

Read `docs/agents/issue-tracker.md` and `docs/agents/workflow.md` — run `/setup` in the target repo if missing.

Read `language` from `workflow.md` (`en` | `cs`). If missing, ask. Write analysis **prose** (title, summary, notes, acceptance text, comments) in that language. Keep **section headings in English**. Branch slug: ASCII, hyphenated; transliterate if the title is not English.

All publish operations follow `docs/agents/issue-tracker.md` (GitHub or local `.scratch/` — do not hardcode `gh` only).

Publish **even if `## FAQ` has open questions** — the analysis must be stored when work continues later. Each FAQ item names what it belongs to (section / contract). After answers, fold them into the right section and remove the FAQ item. Ideal end state: no FAQ section.

## Process

1. Explore the repo if you have not already. If `docs/adr/` exists, respect those decisions.

2. Write the analysis using the template below, then publish (GitHub: label `analysis` only; local: `.scratch/analysis/NNN-<slug>.md`, no Status). Do not add `ready-for-agent`. Create the `analysis` label if it is missing.

3. After publish, prepend `## Delivery` (GitHub: edit issue body; local: update the file):

```markdown
## Delivery

- Kind: feature | bug | chore
- Branch: `feature/analysis-<number>-<short-slug>` (local: `NNN` from next ID, three digits; GitHub: issue number. Slug from title, lowercase, max ~30 chars)
- Branch owner: agent | human   # from docs/agents/workflow.md unless user overrides
- Push: finalize | never
```

For **bugs**, set `Kind: bug` and use the shorter bug sections where appropriate.

## Template

Facts for implementers, not a novel. Frontend (when present) is brief in Architecture — not the focus. **Omit `## API Contracts`** when there is no API. **Always include a mermaid in Summary**, even a simple one.

Architecture `###` subsections are named after real units of the project — a package or repo in a monorepo, a module / bounded context / namespace in a monolith. Never a prescribed `_backend`, and never a layer (`Controller`, `Service`, `Repository`): layer subsections hand implementers horizontal slices. Say where each unit lives (path or namespace). Omit subsections only when the whole change sits in one unit.

<analysis-template>

## Summary

- Ticket: {GitHub / Azure DevOps / Jira URL — omit if none}
- {what changes and **why**}
- {short mermaid of the behaviour — always}

## Current State

{how it works today: modules, data, APIs, invariants}

## Change

{delta — do not repeat Summary}

## Architecture

{layers, data flow, DB/schema, decisions from align/ADRs.
One `###` subsection per real unit of the project, with its path or
namespace: package/repo in a monorepo, module / bounded context in a
monolith. State what changes in each one. Never a prescribed `_backend`,
never a layer (`Controller`, `Service`, `Repository`) — that splits the
work horizontally. Omit subsections only when the whole change sits in
one unit.}

## API Contracts

{request/response, concrete objects and properties. Omit this section when there is no API.}

## Acceptance

{short `- [ ]` list — the testable contract for TDD and verify, not a WBS.
One observable behaviour per item: concrete trigger/input plus the concrete
expected result (status code, payload shape, persisted state, emitted event).
Cover error and boundary paths, not only the happy path.
Reference `## API Contracts` instead of restating payloads.
Never: vague outcomes ("works", "is correct", "is tested") or task items
("add entity", "write test").

good: - [ ] POST /orders with an out-of-stock item → 409, body `code: out_of_stock`, no order row
good: - [ ] Import of a CSV row with an unknown SKU skips that row and keeps the rest
bad:  - [ ] Order creation works and is covered by tests
bad:  - [ ] Add OrderController and its integration test}

## Further Notes

{bullets; durable decisions belong in ADRs}

## FAQ

{optional. Unresolved questions as bullets; each names what it belongs to
(section / contract). Publish with FAQ is OK — persist for later work.
After answers: fold into the right section and remove the FAQ item.
Ideal end state: section omitted.}

</analysis-template>

**Bug:** Summary / Current State / Change / Acceptance; Architecture and API Contracts only when they apply. FAQ optional.

### Local tracker publish

When `docs/agents/issue-tracker.md` is Local Markdown, follow `issue-tracker-local.md`:

1. Compute next `NNN` per issue-tracker-local.md (scan `.scratch/analysis/` and `.scratch/analysis/done/`; never reuse).
2. Choose `<slug>` from the analysis title (lowercase, hyphenated, ASCII; transliterate if needed).
3. Create `.scratch/analysis/NNN-<slug>.md` with Kind, Delivery (`feature/analysis-NNN-<short-slug>`), and analysis body. No Status line.

Bug fast-path (ticket with Acceptance, not a full analysis): same path and ID scan, `Kind: bug`.

### GitHub publish

When backend is GitHub, follow issue-tracker-github.md `/analyze` operations.

**Monorepo:** if `workflow.md` has `## Monorepo` (or nested git repos exist), create the analysis issue on the **container-root** GitHub repo only — use `gh … -R <owner/container-repo>` from that remote. Never publish the analysis into a delivery-root repository.

After publish, tell the user the next step is `/implement` on this analysis (after they have reviewed it).
