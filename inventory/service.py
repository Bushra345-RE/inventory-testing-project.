"""Business logic built on top of the store."""
from typing import List

from .models import Product
from .store import InventoryStore


class InsufficientStockError(Exception):
    pass


class InventoryService:
    LOW_STOCK_LIMIT = 5

    def __init__(self, store: InventoryStore):
        self.store = store

    def add_product(self, sku, name, price, quantity=0) -> Product:
        product = Product(sku, name, price, quantity)
        self.store.add(product)
        return product

    def restock(self, sku: str, amount: int) -> Product:
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("Restock amount must be a positive integer")
        product = self.store.get(sku)
        product.quantity += amount
        return product

    def sell(self, sku: str, amount: int) -> float:
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("Sale amount must be a positive integer")
        product = self.store.get(sku)
        if product.quantity < amount:
            raise InsufficientStockError(
                f"Only {product.quantity} of {product.sku} in stock"
            )
        product.quantity -= amount
        return round(product.price * amount, 2)

    def low_stock(self) -> List[Product]:
        return [p for p in self.store.all() if p.quantity <= self.LOW_STOCK_LIMIT]

    def total_inventory_value(self) -> float:
        return round(sum(p.total_value for p in self.store.all()), 2)

    def search(self, term: str) -> List[Product]:
        term = term.strip().lower()
        return [p for p in self.store.all()
                if term in p.name.lower() or term in p.sku.lower()]
