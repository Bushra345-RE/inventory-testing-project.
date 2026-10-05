"""Integration tests - service + store + model working together."""
import pytest
from inventory import InventoryStore, InventoryService
from inventory.service import InsufficientStockError


@pytest.fixture
def svc():
    return InventoryService(InventoryStore())


def test_add_then_sell_updates_stock(svc):
    svc.add_product("A1", "Pen", 2.0, 10)
    assert svc.sell("A1", 4) == 8.0
    assert svc.store.get("A1").quantity == 6


def test_restock_then_total_value(svc):
    svc.add_product("A1", "Pen", 2.0, 1)
    svc.restock("A1", 4)
    assert svc.total_inventory_value() == 10.0


def test_low_stock_report(svc):
    svc.add_product("A1", "Pen", 2.0, 2)
    svc.add_product("B1", "Book", 9.0, 50)
    assert [p.sku for p in svc.low_stock()] == ["A1"]


def test_search_by_name_and_sku(svc):
    svc.add_product("PEN-1", "Blue Pen", 2.0, 5)
    svc.add_product("BK-1", "Notebook", 5.0, 5)
    assert len(svc.search("pen")) == 1
    assert svc.search("bk")[0].name == "Notebook"


def test_persistence_round_trip(svc, tmp_path):
    svc.add_product("A1", "Pen", 2.0, 3)
    f = tmp_path / "inv.json"
    svc.store.save(str(f))
    fresh = InventoryService(InventoryStore())
    fresh.store.load(str(f))
    assert fresh.store.get("A1").quantity == 3


def test_oversell_does_not_change_stock(svc):
    svc.add_product("A1", "Pen", 2.0, 3)
    with pytest.raises(InsufficientStockError):
        svc.sell("A1", 10)
    assert svc.store.get("A1").quantity == 3
