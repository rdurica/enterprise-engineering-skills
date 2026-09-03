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

2. Write the analysis from the template below, then publish it. On GitHub the only label is `analysis` — create it if it does not exist, and never add `ready-for-agent`. Locally the analysis is `.scratch/analysis/NNN-<slug>.md` with no Status line.

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

## Writing style

Facts for the implementers and for whoever has to explain the change later. Not a novel, and not a wall of backticks.

- Backticks are for paths, commands, HTTP routes and literal values. Class, command, DTO and event names in prose stay plain text.
- A data shape gets a fenced blueprint block instead of a sentence stuffed with backticked names:

```
ChangeSubscriptionPlanCommand
- string: $groupUuid
- string: $planCode
- bool: $prorate
```

- Frontend stays short when it is involved; it is not the focus.
- `## API Contracts` is omitted when there is no API.
- Summary always carries a mermaid, even a simple one.

### Architecture subsections

Each `###` is one real unit of the project: a package or repo in a monorepo, a module or bounded context in a monolith. Never a layer such as Controller, Service or Repository — layer subsections hand implementers horizontal slices. Never an invented name like `_backend`.

The heading is the unit name and nothing else. No parentheses, no path, no file name. The path goes on the first line below the heading.

example:

```markdown
### Frontend app

Path: frontend/src/views/groups/settings/
```

Units with disjoint paths can be implemented in parallel, so name any seam they share — otherwise `/implement` parallelizes blindly. Omit subsections only when the whole change sits in a single unit.

Every ADR the change rests on is linked from `## Architecture` by path (`docs/adr/NNNN-slug.md`), so a reader can reach the reasoning without the align session. A decision `/align` put in the analysis bucket has no ADR to link — it belongs in `## Further Notes` instead.

## Template

<analysis-template>

## Summary

- {what changes and **why**}
- {key changes - one to three bullets}
- {mermaid of the behaviour — always}

## Current State

{how it works today: modules, data, APIs, invariants few sentences readable}
{key parts - bullets}

## Change

{the delta — do not repeat Summary}

## Architecture

{layers, data flow, decisions carried over from align or ADRs.
One `###` per real unit, path on the line below the heading.
When the schema changes, state the delta — tables and columns added or
changed, nullability, defaults, indexes — plus the migration, written by
hand, with the backfill and the rollback whenever existing rows are touched.}

## API Contracts

{one block per endpoint; omit the whole section when there is no API.
Authorization is mandatory in every block — who may call it, and the status
and error code everyone else gets.}

```
POST /api/groups/{uuid}/plan

Authorization
- group owner only; any other member 403 insufficient_permissions

Request
- string: planCode
- bool: prorate

Response 200
- string: planCode
- string: effectiveFrom (ISO-8601)

Errors
- 409 plan_downgrade_blocked
- 404 group_not_found
```

## Acceptance

{`- [ ]` list — the testable contract for TDD and verify, not a WBS.
One observable behaviour per item: a concrete trigger or input plus the
concrete expected result (status code, payload shape, persisted state,
emitted event). Cover error and boundary paths, not only the happy path.
Every endpoint in `## API Contracts` gets its own item for the denied caller,
carrying the status and error code from that block's Authorization.
Point at the API contract instead of restating payloads. One item, one seam.
Keep items fine-grained — `/implement` clusters overlapping ones itself, and
verify needs them separate. Do not add checkboxes for unit tests.

good: - [ ] POST /orders with an out-of-stock item → 409, body `code: out_of_stock`, no order row
good: - [ ] Import of a CSV row with an unknown SKU skips that row and keeps the rest
good: - [ ] POST /orders as a caller outside the group → 403, body `code: insufficient_permissions`, no order row
bad:  - [ ] Order creation works and is covered by tests
bad:  - [ ] Add OrderController and its integration test}

## Further Notes

{one bullet for every decision `/align` put in the analysis bucket, naming the
alternative that was rejected — those are not optional. Beyond them, add a
bullet only when it carries impact, a risk, or a rollout or migration step.
Never state that something does not change, and never repeat what the sections
above already say. Durable decisions belong in ADRs, linked from
`## Architecture`. Omit the whole section when nothing qualifies.

good: Downgrade is blocked while an unpaid invoice exists; the queued-downgrade
      alternative needs the billing job and is out of scope.
bad:  No new endpoint and no change to the GET/PATCH data policy.}

## FAQ

{optional. Unresolved questions as bullets, each naming what it belongs to —
a section or a contract. Publishing with an open FAQ is fine. After answers:
fold each one into the right section and delete the item.}

</analysis-template>

**Bug:** Summary, Current State, Change, Acceptance. Architecture and API Contracts only when they apply; FAQ optional.

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
