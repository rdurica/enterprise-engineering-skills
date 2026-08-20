---
name: integration-tests
description: >-
  Writes and extends Symfony PHPUnit HTTP integration tests (KernelBrowser,
  contract assertions, mandatory Verifies/Input/Reason docblocks). Use when
  adding or changing tests in tests/Integration, HTTP API test cases, actingAs
  clients, expectProblem, or integration test docblocks.
---

# PHP HTTP integration tests

Playbook for **HTTP contract** integration tests in Symfony + PHPUnit. Project-specific paths, base classes, and run commands live in the repo's `AGENTS.md` — read that section first.

## When to use this skill

| Layer | Scope |
|-------|--------|
| **HTTP integration** | Full stack: routing, security, serialization, persistence — via `KernelBrowser` |
| **Unit (handlers)** | Command/Query logic without HTTP — use project unit-test conventions instead |

Do **not** test handlers by calling them directly from integration tests when the project standard is HTTP contract tests.

## Architecture

```
tests/Integration/
├── Support/                    # shared: abstract base, auth trait, fluent HTTP client
└── {Module}/
    ├── Support/
    │   ├── {Module}ApiTestCase.php      # extends shared abstract
    │   └── {Module}ApiTestHelperTrait.php   # optional: URI/helpers only
    └── {Area}/
        └── *Test.php           # final class per endpoint area
```

Flow: `*Test` → `{Module}ApiTestCase` → `AbstractHttpApiTestCase` → `HttpActingAsClient` → real app (router, security, controller, DB).

Details: [reference.md](reference.md). Examples: [examples.md](examples.md).

## File and method conventions

- **Class:** `final class CreateFooTest extends FooApiTestCase`
- **Method:** `test{Behavior}{Outcome}` — e.g. `testCreateFooReturns201`, `testCreateFooDeniedForOutsider`
- **Arrange:** inline in each test (`createTestUser`, entity factories) — no shared scenario fixtures across tests
- **Assert:** decoded JSON from the fluent client; after writes, assert repository/DB state when the contract implies persistence
- **Auth:** real tokens in test env (`actingAs($user)` / `withoutAuth()`) — do not disable security globally

## Fluent HTTP client

Obtain client from base test case: `$this->actingAs($user)` or `$this->withoutAuth()`.

```php
// Happy (default status 200 if expectStatus omitted)
$body = $this->actingAs($owner)->expectStatus(201)->post($uri, $payload);

// Business / domain error — body must expose stable `code`
$this->actingAs($outsider)->expectProblem(403, 'insufficient_permissions')->get($uri);

// Request validation — field keys in API error payload
$this->actingAs($user)->expectValidationErrors(400, ['email'])->post($uri, []);

// Framework security without JWT — often status only, no problem `code`
$this->withoutAuth()->expectStatus(401)->get($uri);
```

**Rule:** use `expectProblem` only when the API returns a documented `code` in the JSON body. For Symfony Security 401 without a body code, use `expectStatus(401)`.

## Mandatory docblock (English)

Every `public function test*()` needs these three lines (CI-friendly exact prefixes):

```php
/**
 * Verifies that GET /api/resources returns the list for an authorized caller.
 *
 * Input: authenticated user with two related records in the database.
 * Reason: authorized users must see their resources via the public API contract.
 *
 * @throws JsonException
 */
public function testListResourcesReturnsAll(): void
```

| Line | Content |
|------|---------|
| `Verifies that` | HTTP method + route + outcome (status, error `code`, side effect) |
| `Input:` | Arrange: actors/roles, DB state, payload highlights, auth |
| `Reason:` | Why the contract matters — not "asserts 200" |
| `@throws` | Keep existing PHPUnit/Doctrine `@throws` tags |

Docblocks are **English** even when user-facing API messages are localized.

## Agent workflow

1. Locate controller, route attributes, and security rules in source.
2. Find existing `tests/Integration/{Module}/` layout and `{Module}ApiTestCase`.
3. Add **happy** path plus **unhappy** paths (403/404/409 per domain) and **validation** where a Request DTO exists.
4. Add docblock to every new `test*` method before finishing.
5. Run the project's Integration PHPUnit suite (command from `AGENTS.md`).
6. If the project has a docblock check script, run it (e.g. `composer check-integration-docblocks`).

## Coverage checklist per endpoint

- [ ] Happy path with expected status and response shape
- [ ] Authorization failure (`expectProblem` or `expectStatus` per project rules)
- [ ] Not found / conflict when applicable
- [ ] Validation errors for invalid payload
- [ ] Unauthenticated access where security applies
- [ ] Docblock on every `test*` method

## Out of scope for this skill

- Project-specific DB names, Docker/`make` commands, module URI traits
- Full catalog of error `code` values — read module ErrorMap or exception mappers
- Unit tests for application handlers

## Additional resources

- Assertion matrix and folder layout: [reference.md](reference.md)
- Copy-paste patterns: [examples.md](examples.md)
