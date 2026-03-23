"""Inventory management port definitions."""

from typing import Protocol

from domain.models import SKU, PositiveQuantity, Quantity


class InventoryPort(Protocol):
    """Port interface for inventory management."""

    def exists_sku(self, sku: SKU) -> bool:
        """Check if a SKU exists in the inventory."""
        ...

    def get_stock(self, sku: SKU) -> Quantity:
        """Get the current stock level for a given SKU."""
        ...

    def reserve(self, sku: SKU, qty: PositiveQuantity) -> Quantity:
        """Reserve a specified quantity of a SKU.

        reducing available stock. return new stock level.
        """
        ...
