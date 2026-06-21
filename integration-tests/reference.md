# HTTP integration tests — reference

## Directory layout

| Path | Purpose |
|------|---------|
| `tests/Integration/Support/` | Shared abstract test case, auth trait, fluent HTTP client |
| `tests/Integration/{Module}/Support/{Module}ApiTestCase.php` | Module base extending shared abstract |
| `tests/Integration/{Module}/Support/{Module}ApiTestHelperTrait.php` | Optional: module URI builders and test-only helpers |
| `tests/Integration/{Module}/{Area}/*Test.php` | One `final` test class per controller action area |

Group tests by **API area** (resource or controller group), not by PHP namespace of handlers.

## Module base template

```php
<?php

declare(strict_types=1);

namespace App\Tests\Integration\YourModule\Support;

use App\Tests\Integration\Support\AbstractHttpApiTestCase;

abstract class YourModuleApiTestCase extends AbstractHttpApiTestCase
{
    // use YourModuleApiTestHelperTrait; // if present
}
```

Module traits should contain **URI helpers and test data builders only** — not shared multi-test scenarios.

## Fluent client API

Typical class name: `HttpActingAsClient`. Obtained via `actingAs($user)` or `withoutAuth()` on the test case.

### Expectation methods (immutable clones)

| Method | Sets |
|--------|------|
| `expectStatus(int $status)` | Exact HTTP status; default 200 when omitted on success paths |
| `expectProblem(int $status, string $code)` | Status + JSON `code` field in problem body |
| `expectValidationErrors(int $status, array $fields)` | Status + presence of each field in `errors` payload |

Call expectation methods **before** the HTTP verb method.

### HTTP verb methods

| Method | Notes |
|--------|-------|
| `get(string $uri): ?array` | JSON decode; `null` if empty body |
| `getText(string $uri): string` | Raw body; uses `expectStatus` only |
| `post(string $uri, ?array $body): ?array` | `Content-Type: application/json` |
| `put(string $uri, ?array $body): ?array` | |
| `patch(string $uri, ?array $body): ?array` | |
| `delete(string $uri, ?array $body): ?array` | |
| `postFile(string $uri, string $field, UploadedFile $file): ?array` | Multipart upload |

Return type is usually `array<string, mixed>|list<mixed>|null` after JSON decode.

## Assertion matrix

| Scenario | Typical call | Body assertion |
|----------|--------------|----------------|
| Success | `expectStatus(201)->post(...)` or omit expect for 200 | Assert keys/count on returned array |
| Domain forbidden | `expectProblem(403, 'insufficient_permissions')` | Client asserts `code` |
| Not found | `expectProblem(404, 'resource_not_found')` | Stable code from API mapper |
| Conflict | `expectProblem(409, 'already_exists')` | |
| Validation | `expectValidationErrors(400, ['email', 'name'])` | Each field present in `errors` |
| Missing auth (framework) | `withoutAuth()->expectStatus(401)->get(...)` | Do not require `code` unless API documents it |
| Empty success body | `expectStatus(204)->delete(...)` | Return may be `null` |

### Choosing `expectProblem` vs `expectStatus`

- **`expectProblem`:** application or presentation layer returns RFC 7807 / problem JSON with a stable machine-readable `code` (e.g. `insufficient_permissions`).
- **`expectStatus` only:** Symfony firewall or entrypoint rejects before application problem mapper runs; body may be empty or HTML.

## Auth and database

- **Database:** dedicated test database; schema migrated; tables truncated or reset **before each test** so tests stay isolated.
- **Auth:** issue real JWT/session tokens using test keys and the same `TokenIssuer` (or equivalent) as production wiring — `actingAs($user)` sets `Authorization: Bearer …`.
- **External services:** stub interfaces in `services_test.yaml` (e.g. OAuth verifiers); never call real third-party APIs from integration tests.

## Naming reference

| Artifact | Pattern | Example |
|----------|---------|---------|
| Test class | `{Action}{Resource}Test` or `{Resource}{Action}Test` | `GetMembersTest`, `CreateEventTest` |
| Happy method | `test{Action}{Resource}Returns{Status}` | `testGetMembersReturnsAllMembers` |
| Denied method | `test{Action}{Resource}DeniedFor{Actor}` | `testGetMembersDeniedForOutsider` |
| Validation method | `test{Action}RejectsInvalid{Field}` | `testCreateUserRejectsInvalidEmail` |

## Docblock enforcement pattern

Projects may ship a PHP script that scans `tests/Integration/**/*Test.php` and requires on every `public function test*()`:

- A docblock containing `* Verifies that `
- A line `* Input:`
- A line `* Reason:`

Regex sketch (illustrative):

```php
preg_match_all(
    '/\/\*\*(.*?)\*\/\s*public\s+function\s+(test\w+)\s*\(/s',
    $contents,
    $matches,
);
// then assert Verifies / Input: / Reason: in $docblock
```

Wire into Composer as `check-integration-docblocks` and CI `all-checks` when present.

## PHPUnit execution

Commands vary by project. Common patterns:

```bash
# full integration suite
composer phpunit -- --testsuite Integration

# single file
./vendor/bin/phpunit tests/Integration/Module/Area/SomeTest.php

# filter method
./vendor/bin/phpunit --filter testMethodName
```

Run inside the project's PHP container or local env as documented in `AGENTS.md`. Prefer `XDEBUG_MODE=off` for speed when documented.

## Extending coverage on a new module

1. Add `{Module}ApiTestCase` extending shared abstract.
2. Add URI trait if routes share a prefix (`/api/groups/{id}/…`).
3. For each controller action group, add `final *Test` with happy + unhappy + validation.
4. Run integration suite + docblock check.
5. Do not add facade/handler integration tests if the project standard is HTTP-only.
