"""Data model for a product in the inventory."""
from dataclasses import dataclass


@dataclass
class Product:
    sku: str
    name: str
    price: float
    quantity: int = 0

    def __post_init__(self):
        if not isinstance(self.sku, str) or not self.sku.strip():
            raise ValueError("SKU must be a non-empty string")
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Name must be a non-empty string")
        if isinstance(self.price, bool) or not isinstance(self.price, (int, float)):
            raise TypeError("Price must be a number")
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if not isinstance(self.quantity, int) or isinstance(self.quantity, bool):
            raise TypeError("Quantity must be an integer")
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative")
        self.sku = self.sku.strip().upper()
        self.name = self.name.strip()

    @property
    def total_value(self) -> float:
        return round(self.price * self.quantity, 2)
