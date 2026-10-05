"""Edge-case and error-handling tests."""
import pytest
from inventory import Product, InventoryStore, InventoryService


@pytest.mark.parametrize("sku", ["", "   ", None, 123])
def test_invalid_sku(sku):
    with pytest.raises(ValueError):
        Product(sku, "Pen", 1)


@pytest.mark.parametrize("name", ["", "  "])
def test_invalid_name(name):
    with pytest.raises(ValueError):
        Product("A1", name, 1)


def test_negative_price():
    with pytest.raises(ValueError):
        Product("A1", "Pen", -1)


@pytest.mark.parametrize("price", ["10", None, True])
def test_non_numeric_price(price):
    with pytest.raises(TypeError):
        Product("A1", "Pen", price)


def test_negative_quantity():
    with pytest.raises(ValueError):
        Product("A1", "Pen", 1, -5)


@pytest.mark.parametrize("qty", [1.5, "3", True])
def test_non_integer_quantity(qty):
    with pytest.raises(TypeError):
        Product("A1", "Pen", 1, qty)


@pytest.mark.parametrize("amount", [0, -1, 2.5, "3"])
def test_invalid_sale_and_restock_amounts(amount):
    svc = InventoryService(InventoryStore())
    svc.add_product("A1", "Pen", 1, 10)
    with pytest.raises(ValueError):
        svc.sell("A1", amount)
    with pytest.raises(ValueError):
        svc.restock("A1", amount)


def test_zero_price_allowed():
    assert Product("FREE", "Sample", 0, 5).total_value == 0


def test_sell_exact_stock_leaves_zero():
    svc = InventoryService(InventoryStore())
    svc.add_product("A1", "Pen", 1.5, 4)
    assert svc.sell("A1", 4) == 6.0
    assert svc.store.get("A1").quantity == 0


def test_floating_point_rounding():
    assert Product("A1", "X", 0.1, 3).total_value == 0.3


def test_load_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        InventoryStore().load(str(tmp_path / "missing.json"))


def test_load_corrupt_json_raises(tmp_path):
    f = tmp_path / "bad.json"; f.write_text("{not json")
    with pytest.raises(ValueError):
        InventoryStore().load(str(f))
