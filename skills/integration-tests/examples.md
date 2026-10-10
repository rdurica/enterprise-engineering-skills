# HTTP integration tests — examples

Generic patterns. Adapt class names, factories, and URI helpers to the project.

## 1. Happy GET — list resources

```php
final class ListItemsTest extends CatalogApiTestCase
{
    /**
     * Verifies that GET /api/items returns all items visible to the owner.
     *
     * Input: owner with two items persisted; authenticated GET request.
     * Reason: owners must retrieve their full item list through the API contract.
     *
     * @throws JsonException
     */
    public function testListItemsReturnsAllForOwner(): void
    {
        $owner = $this->createTestUser('owner@example.com');
        $this->createTestItem($owner, 'First');
        $this->createTestItem($owner, 'Second');

        $body = $this->actingAs($owner)->get('/api/items');

        self::assertIsArray($body);
        self::assertCount(2, $body);
    }
}
```

## 2. Business error — forbidden

```php
    /**
     * Verifies that GET /api/items/{id} returns 403 for a user without access.
     *
     * Input: item owned by another user; authenticated GET as outsider.
     * Reason: only users with view permission may read another user's private item.
     *
     * @throws JsonException
     */
    public function testGetItemDeniedForOutsider(): void
    {
        $owner = $this->createTestUser('owner@example.com');
        $outsider = $this->createTestUser('outsider@example.com');
        $item = $this->createTestItem($owner, 'Private');

        $this->actingAs($outsider)->expectProblem(403, 'insufficient_permissions')->get(
            '/api/items/' . $item->id(),
        );
    }
```

## 3. Validation errors

```php
    /**
     * Verifies that POST /api/items rejects a missing required email field.
     *
     * Input: authenticated user; POST with empty body.
     * Reason: the create-item contract requires a valid email in the payload.
     *
     * @throws JsonException
     */
    public function testCreateItemRejectsMissingEmail(): void
    {
        $user = $this->createTestUser('user@example.com');

        $this->actingAs($user)->expectValidationErrors(400, ['email'])->post('/api/items', [
            'name' => 'No email',
        ]);
    }
```

## 4. Unauthenticated — framework 401

```php
    /**
     * Verifies that GET /api/items returns 401 without authentication.
     *
     * Input: no Authorization header; GET items collection.
     * Reason: the items endpoint requires an authenticated principal.
     *
     * @throws JsonException
     */
    public function testListItemsRequiresAuthentication(): void
    {
        $this->withoutAuth()->expectStatus(401)->get('/api/items');
    }
```

## 5. Happy POST — create + DB assert

```php
    /**
     * Verifies that POST /api/items creates an item and returns 201.
     *
     * Input: authenticated owner; valid name and email in JSON body.
     * Reason: owners must be able to create items through the public create endpoint.
     *
     * @throws JsonException
     */
    public function testCreateItemReturns201(): void
    {
        $owner = $this->createTestUser('owner@example.com');

        $body = $this->actingAs($owner)->expectStatus(201)->post('/api/items', [
            'name' => 'New item',
            'email' => 'item@example.com',
        ]);

        self::assertIsArray($body);
        self::assertArrayHasKey('id', $body);

        $stored = $this->itemRepository->find($body['id']);
        self::assertNotNull($stored);
        self::assertSame('New item', $stored->name());
    }
```

## 6. Scoped URI helper (module trait)

```php
// In YourModuleApiTestHelperTrait:
protected function itemUri(string $itemId, string $suffix = ''): string
{
    return '/api/items/' . $itemId . $suffix;
}

// In test:
$this->actingAs($owner)->get($this->itemUri($item->id()));
```

## Anti-patterns

```php
// BAD: shared fixture builds a whole scenario used by many tests
$this->loadScenario('premium_group_at_capacity');

// GOOD: arrange only what this test needs
$owner = $this->createTestUser('owner@example.com');
$group = $this->createTestGroup($owner);

// BAD: call application handler directly in Integration suite
($this->getContainer()->get(CreateItemHandler::class))($command);

// GOOD: HTTP contract
$this->actingAs($owner)->expectStatus(201)->post('/api/items', $payload);

// BAD: docblock without required lines
/** @test */
public function testFoo(): void

// GOOD: Verifies / Input / Reason (see SKILL.md)
```
