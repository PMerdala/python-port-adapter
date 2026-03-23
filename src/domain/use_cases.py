"""Use case implementations for the inventory management system."""

from .errors import OutOfStockError, UnknownSKUError
from .models import OrderPlaced, OrderRequest
from .ports import InventoryPort  # noqa: TC001


def place_order(req: OrderRequest, inventory: InventoryPort) -> OrderPlaced:
    """Place an order for a specific SKU and quantity."""
    if not inventory.exists_sku(req.sku):
        raise UnknownSKUError(req.sku)

    available = inventory.get_stock(req.sku)

    if available < req.qty:
        raise OutOfStockError(req.sku, req.qty, available)

    remaining = inventory.reserve(req.sku, req.qty)

    # API response shaping in the domain-y function
    return OrderPlaced(
        sku=req.sku,
        qty=req.qty,
        remaining_stock=remaining,
    )
