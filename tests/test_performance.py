"""Performance tests - guard against slow operations."""
import time
from inventory import InventoryStore, InventoryService


def test_bulk_add_and_search_10000_products_under_1s():
    svc = InventoryService(InventoryStore())
    start = time.perf_counter()
    for i in range(10_000):
        svc.add_product(f"SKU{i}", f"Item {i}", 1.0, i % 20)
    svc.search("item 9999")
    svc.total_inventory_value()
    svc.low_stock()
    elapsed = time.perf_counter() - start
    print(f"\nPERF_ELAPSED={elapsed:.3f}s")
    assert elapsed < 1.0
