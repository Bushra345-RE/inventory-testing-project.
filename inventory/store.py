"""Storage layer: keeps products in memory with optional JSON persistence."""
import json
from typing import Dict, List, Optional

from .models import Product


class DuplicateSKUError(Exception):
    pass


class ProductNotFoundError(Exception):
    pass


class InventoryStore:
    def __init__(self):
        self._items: Dict[str, Product] = {}

    def add(self, product: Product) -> None:
        if product.sku in self._items:
            raise DuplicateSKUError(f"SKU {product.sku} already exists")
        self._items[product.sku] = product

    def get(self, sku: str) -> Product:
        key = sku.strip().upper()
        if key not in self._items:
            raise ProductNotFoundError(f"SKU {key} not found")
        return self._items[key]

    def remove(self, sku: str) -> None:
        key = sku.strip().upper()
        if key not in self._items:
            raise ProductNotFoundError(f"SKU {key} not found")
        del self._items[key]

    def all(self) -> List[Product]:
        return list(self._items.values())

    def save(self, path: str) -> None:
        data = [vars(p) for p in self._items.values()]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load(self, path: str) -> None:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self._items = {}
        for row in data:
            self.add(Product(**row))
