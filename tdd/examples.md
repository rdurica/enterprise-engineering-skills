# One vertical slice (PHPUnit unit)

Generic domain service. Adapt namespaces and the PHPUnit command from `AGENTS.md`. Do not use this pattern for HTTP — that is `integration-tests`.

## Behaviour 1 — subtract discount

### RED

```php
// tests/Unit/DiscountCalculatorTest.php
final class DiscountCalculatorTest extends TestCase
{
    public function testApplySubtractsDiscountFromSubtotal(): void
    {
        $calculator = new DiscountCalculator();

        $total = $calculator->apply(subtotal: 1000, discount: 200);

        self::assertSame(800, $total);
    }
}
```

### Verify RED

```
./vendor/bin/phpunit --filter testApplySubtractsDiscountFromSubtotal
```

New class: **ERROR** `Class "DiscountCalculator" not found` is valid RED.

Class already exists with the wrong result: **FAILURE** is valid RED, for example:

```
Failed asserting that 1000 is identical to 800.
```

Syntax error or broken arrange in the test → fix the test, re-run. Do not implement yet.

### GREEN

Only enough to pass this test:

```php
final class DiscountCalculator
{
    public function apply(int $subtotal, int $discount): int
    {
        return $subtotal - $discount;
    }
}
```

### Verify GREEN

Same `--filter`. Must pass. Then stop — do not add clamping, types, or extra methods until the next test asks for them.

## Behaviour 2 — next cycle, same file

Do **not** write this test in the same RED as behaviour 1.

```php
public function testApplyDiscountDoesNotGoBelowZero(): void
{
    $calculator = new DiscountCalculator();

    $total = $calculator->apply(subtotal: 1000, discount: 1500);

    self::assertSame(0, $total);
}
```

Verify RED (`--filter testApplyDiscountDoesNotGoBelowZero`): **FAILURE** — `Failed asserting that -500 is identical to 0.`

GREEN — change only what this test requires:

```php
return max(0, $subtotal - $discount);
```

Verify GREEN with the same filter, then run the file so behaviour 1 still passes.
