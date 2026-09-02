# Good and Bad Tests

PHPUnit unit tests. Names: `test{Behavior}{Outcome}`. HTTP contracts belong in `integration-tests`, not here.

## Good Tests

Test observable behaviour through the public interface.

```php
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

- Observable behaviour callers care about
- Public API only
- Survives internal refactors
- Expected value is a known literal, not recomputed the way the code does

## Bad Tests

Implementation coupling: mock an internal collaborator and assert it was called.

```php
public function testApplyCallsPricingEngineCompute(): void
{
    $engine = $this->createMock(PricingEngine::class);
    $engine->expects(self::once())->method('compute')->with(1000, 200);

    (new DiscountCalculator($engine))->apply(subtotal: 1000, discount: 200);
}
```

Red flags: mocking internal collaborators, testing private methods, asserting call order, bypassing the interface to query the DB directly.
