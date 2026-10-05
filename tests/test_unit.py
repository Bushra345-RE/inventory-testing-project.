"""Unit tests - each component tested in isolation."""
import pytest
from inventory import Product, InventoryStore
from inventory.store import DuplicateSKUError, ProductNotFoundError


class TestProduct:
    def test_valid_product_normalises_sku_and_name(self):
        p = Product(" ab12 ", " Pen ", 10.5, 3)
        assert p.sku == "AB12" and p.name == "Pen"

    def test_total_value(self):
        assert Product("A1", "Pen", 2.5, 4).total_value == 10.0

    def test_default_quantity_is_zero(self):
        assert Product("A1", "Pen", 2).quantity == 0


class TestStore:
    def test_add_and_get(self):
        s = InventoryStore(); s.add(Product("A1", "Pen", 1))
        assert s.get("a1").name == "Pen"

    def test_duplicate_sku_rejected(self):
        s = InventoryStore(); s.add(Product("A1", "Pen", 1))
        with pytest.raises(DuplicateSKUError):
            s.add(Product("a1", "Other", 2))

    def test_get_missing_raises(self):
        with pytest.raises(ProductNotFoundError):
            InventoryStore().get("NOPE")

    def test_remove(self):
        s = InventoryStore(); s.add(Product("A1", "Pen", 1)); s.remove("A1")
        assert s.all() == []

    def test_remove_missing_raises(self):
        with pytest.raises(ProductNotFoundError):
            InventoryStore().remove("NOPE")
