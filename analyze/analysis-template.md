# Analysis template

Writing rules and section template for `/analyze`. Delivery and publishing follow [SKILL.md](SKILL.md).

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
