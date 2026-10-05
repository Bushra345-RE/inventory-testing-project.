"""User acceptance tests - written as real-world shopkeeper scenarios."""
import pytest
from inventory import InventoryStore, InventoryService
from inventory.service import InsufficientStockError


@pytest.fixture
def shop():
    s = InventoryService(InventoryStore())
    s.add_product("MILK", "Milk 1L", 30, 12)
    return s


def test_uat1_shopkeeper_can_sell_item_and_get_bill(shop):
    assert shop.sell("milk", 3) == 90.0


def test_uat2_shopkeeper_warned_when_stock_is_low(shop):
    shop.sell("MILK", 8)
    assert "MILK" in [p.sku for p in shop.low_stock()]


def test_uat3_cannot_sell_more_than_available(shop):
    with pytest.raises(InsufficientStockError) as e:
        shop.sell("MILK", 99)
    assert "Only 12" in str(e.value)


def test_uat4_shopkeeper_can_find_product_by_partial_name(shop):
    assert shop.search("mil")[0].sku == "MILK"
