# When to Mock

Mock at **system boundaries** only: external APIs, time, file system (sometimes).

Do not mock your own modules or internal collaborators.

Prefer constructor injection at boundaries. Prefer a specific gateway over one generic HTTP client with conditional stubs.

```php
// Easy to stub — inject the boundary
final class ChargeOrder
{
    public function __construct(private PaymentGateway $gateway) {}

    public function handle(Order $order): ChargeResult
    {
        return $this->gateway->charge($order->total());
    }
}

$gateway = $this->createStub(PaymentGateway::class);
$gateway->method('charge')->willReturn(ChargeResult::ok());
$service = new ChargeOrder($gateway);
```

```php
// Hard to stub — constructed inside
final class ChargeOrder
{
    public function handle(Order $order): ChargeResult
    {
        $client = new StripeClient($_ENV['STRIPE_KEY']);

        return $client->charge($order->total());
    }
}
```
