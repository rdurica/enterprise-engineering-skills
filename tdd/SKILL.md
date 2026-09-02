---
name: tdd
description: >-
  Test-driven development with red-green-refactor vertical slices. Use when
  building features or fixes test-first, or when implement delegates testing.
  For PHP backend, routes HTTP work to integration-tests and handler/domain
  work to PHPUnit unit tests. Always run the failing test (Verify RED) before
  writing production code.
---

# Test-Driven Development

## Philosophy

Tests verify behaviour through **public interfaces**, not implementation details. Good tests survive refactors; bad tests break when you rename an internal function.

See [tests.md](tests.md), [mocking.md](mocking.md), [refactoring.md](refactoring.md). Full unit cycle: [examples.md](examples.md).

## Anti-pattern: horizontal slices

Do NOT write all tests first, then all code.

```
WRONG:  RED test1..5  →  GREEN impl1..5
RIGHT:  RED test1 → Verify RED → GREEN impl1 → RED test2 → GREEN impl2 → …
```

## Workflow

### 1. Planning

Read `docs/adr/` if it exists.

Before writing code:

- Confirm interface changes and behaviours to test (prioritized)
- List behaviours, not implementation steps
- Get user approval on the plan

### 2. Tracer bullet

```
RED:        One test for one behaviour
Verify RED: Run it — must fail for the expected reason
GREEN:      Minimal code to pass
```

### 3. Incremental loop

One test at a time. Only enough code to pass the current test. No speculative features.

### Verify RED (mandatory)

Run **one** test before any production code. Command from `AGENTS.md` (typically `--filter` or a single file).

| PHPUnit result | Meaning | Action |
|----------------|---------|--------|
| **FAILURE** | Assertion failed — behaviour missing | GREEN |
| **ERROR** | Syntax, broken arrange, autoload | Fix the test and re-run. Exception: first cycle of a **new class** may ERROR with class/method not found — that is valid RED |
| **OK** | Test already passes | You are testing existing behaviour. Change the test. Do not write production code |

Never skip this step. If you did not watch it fail, you do not know the test can catch the bug.

### 4. Refactor

After all tests pass, apply [refactoring.md](refactoring.md). **Never refactor while RED.**

## Choosing the test layer (PHP backend)

| Seam | Skill / approach |
|------|------------------|
| HTTP API endpoint | `integration-tests` — full-stack contract via KernelBrowser |
| Command/Query handler, domain service, value object | PHPUnit **unit tests** — read paths and conventions from target repo `AGENTS.md` |
| Both in one slice | TDD cycle at the highest seam first (usually HTTP); unit tests only where HTTP cannot reach the logic cleanly |

Run one test (`--filter` / one file) per red-green cycle. Project-specific PHPUnit commands live in `AGENTS.md`.

## One cycle (unit)

RED — one behaviour, public method, literal expected value:

```php
public function testApplyDiscountDoesNotGoBelowZero(): void
{
    $total = (new DiscountCalculator())->apply(subtotal: 1000, discount: 1500);

    self::assertSame(0, $total);
}
```

Verify RED — must FAIL (or class-not-found ERROR on a brand-new type):

```
./vendor/bin/phpunit --filter testApplyDiscountDoesNotGoBelowZero
```

GREEN — only enough code to pass:

```php
public function apply(int $subtotal, int $discount): int
{
    return max(0, $subtotal - $discount);
}
```

Then the same `--filter` must pass. Next behaviour = next test, not a batch.

## Checklist per cycle

- [ ] Test describes behaviour, not implementation
- [ ] Test uses public interface only
- [ ] Watched FAIL for the expected reason before implementing
- [ ] Code is minimal for this test
- [ ] No speculative features added
