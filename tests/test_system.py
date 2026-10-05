"""System test - full end-to-end workflow through the whole application."""
from inventory import InventoryStore, InventoryService


def test_full_shop_day_workflow(tmp_path):
    svc = InventoryService(InventoryStore())
    svc.add_product("PEN-1", "Blue Pen", 10, 20)
    svc.add_product("BK-1", "Notebook", 50, 8)
    svc.add_product("ER-1", "Eraser", 5, 3)

    revenue = svc.sell("PEN-1", 5) + svc.sell("BK-1", 4)
    assert revenue == 250.0

    assert {p.sku for p in svc.low_stock()} == {"ER-1", "BK-1"}
    svc.restock("ER-1", 30)
    assert {p.sku for p in svc.low_stock()} == {"BK-1"}

    path = tmp_path / "day.json"
    svc.store.save(str(path))
    restored = InventoryService(InventoryStore())
    restored.store.load(str(path))
    assert restored.total_inventory_value() == svc.total_inventory_value() == 15*10 + 4*50 + 33*5
