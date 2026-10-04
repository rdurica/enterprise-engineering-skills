---
name: tdd
description: >-
  Test-driven development with red-green-refactor vertical slices. Use when
  building features or fixes test-first, or when implement delegates testing.
  For PHP backend, HTTP goes to integration-tests; handler/domain decision
  logic always gets PHPUnit unit tests (HTTP does not replace them). Always
  run the failing test (Verify RED) before writing production code.
---

# Test-Driven Development

## Philosophy

Tests verify behaviour through **public interfaces**, not implementation details. Good tests survive refactors; bad tests break when you rename an internal function.

See [tests.md](tests.md), [mocking.md](mocking.md), [refactoring.md](refactoring.md). Full unit cycle: [examples.md](examples.md).

## Execution modes

For a **direct** invocation, use a vertical red-green-refactor loop:

```
RED test1 → Verify RED → GREEN impl1 → RED test2 → Verify RED → GREEN impl2 → …
```

Under `/implement`, follow its [Execution contract](../implement/SKILL.md#execution-contract): test-only workers first, reviewed test commits, then new implementation workers. Stay in your assigned phase and scope; return results to the parent without git/delivery operations.

## Workflow

### 1. Planning

Read `docs/adr/` if it exists.

When `/implement` invoked this skill, the published analysis is the plan: cover every assigned Acceptance item in your phase and permitted paths. Respect shared-resource constraints and return commands, results, coverage and blockers.

Otherwise, before writing code:

- Confirm interface changes and behaviours to test (prioritized)
- List behaviours, not implementation steps
- Obtain missing contract decisions when required; an already authorized, sufficiently defined task can proceed

### 2. Tracer bullet

```
RED:        One test for one behaviour
Verify RED: Run it — must fail for the expected reason
GREEN:      Minimal code to pass
```

### 3. Incremental loop

One test at a time. Only enough code to pass the current test. No speculative features.

Under `/implement`, test workers return contract coverage and RED evidence; implementation workers satisfy the committed tests through production code and return GREEN evidence. The parent controls phase changes and commits.

### Verify RED (mandatory)

Run tests before new production code. Command from `AGENTS.md` (typically `--filter` or a single file). Direct invocation: one test. Under `/implement`: the cluster's tests, with results mapped to behaviours. New or corrected behaviour needs an expected failure; regression tests for already correct behaviour may pass. Do not rewrite a correct regression assertion just to manufacture RED.

| PHPUnit result | Meaning | Action |
|----------------|---------|--------|
| **FAILURE** | Assertion failed — behaviour missing | GREEN |
| **ERROR** | Syntax, broken arrangement, autoload or environment | Fix the test/environment and re-run. A missing **new** class/method can establish initial RED, but does not yet validate all assertions; verify them once the symbol exists |
| **OK** | Existing behaviour passes | Keep valid regression coverage. If this was meant to reproduce a missing behaviour, investigate the input and contract; do not force a failure by weakening or distorting the test |

Never skip this step for missing or corrected behaviour. Report environment blockers honestly; do not describe an infrastructure failure as behavioural RED.

### Committed test baseline

Follow the Execution contract for later test corrections: justify and review the change, commit it separately, and recheck RED where applicable. Never weaken assertions or remove contract coverage to make implementation pass. In direct TDD, genuine contract or test defects may be corrected with the same reason recorded.

### 4. Refactor

After all tests pass, apply [refactoring.md](refactoring.md). **Never refactor while RED.**

## Choosing the test layer (PHP backend)

| Seam | Skill / approach |
|------|------------------|
| HTTP API endpoint | `integration-tests` — full-stack contract via KernelBrowser |
| Handler, domain service, or value object with **decision logic** (branches, invariant, calculation, policy) | PHPUnit **unit tests** on the public interface — **always**, even when an HTTP test already covers the endpoint. Read paths from target repo `AGENTS.md` |
| Pure wiring (handler forwards, no branches) | Skip unit — HTTP is enough |
| No HTTP | Unit only |
| Both seams on one Acceptance item | Highest seam first (HTTP), then unit for the **same** decision. Each test its own Verify RED. HTTP does not replace unit |

Run one test (`--filter` / one file) per red-green cycle, or the cluster's tests under `/implement`. Project-specific PHPUnit commands live in `AGENTS.md`.

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

Then the same `--filter` must pass. In direct TDD, proceed to the next behaviour. Under `/implement`, test-only and implementation workers complete their assigned cluster/phase and return to the orchestrator.

## Checklist per cycle

- [ ] Test describes behaviour, not implementation
- [ ] Test uses public interface only
- [ ] Recorded expected RED for new/corrected behaviour; identified passing regression coverage
- [ ] Code is minimal for this test
- [ ] No speculative features added
