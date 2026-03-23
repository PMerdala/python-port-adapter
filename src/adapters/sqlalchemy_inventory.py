"""Module contains the SQLAlchemy adapter for the InventoryPort.

allowing us to interact with a database using SQLAlchemy to manage inventory data.
"""

from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.engine import Connection  # noqa: TC002

from domain.ports import InventoryPort
from models import SKU, PositiveQuantity, Quantity


@dataclass
class SqlAlchemyInventoryAdapter(InventoryPort):
    """SQLAlchemy-based implementation of the InventoryPort interface."""

    conn: Connection

    def exists_sku(self, sku: SKU) -> bool:
        """Check if a SKU exists in the inventory."""
        row = self.conn.execute(
            text("SELECT 1 FROM inventory WHERE sku = :sku"),
            {"sku": sku},
        ).fetchone()
        return row is not None

    def get_stock(self, sku: SKU) -> Quantity:
        """Get the current stock level for a given SKU."""
        row = self.conn.execute(
            text("SELECT stock FROM inventory WHERE sku = :sku"),
            {"sku": sku},
        ).fetchone()
        return Quantity(int(row.stock))

    def reserve(self, sku: SKU, qty: PositiveQuantity) -> Quantity:
        """Reserve a specified quantity of a SKU, reducing available stock. Return new stock level."""
        with self.conn.begin():
            self.conn.execute(
                text("UPDATE inventory SET stock = stock - :qty WHERE sku=:sku"),
                {"sku": sku, "qty": qty},
            )
            remaining = self.conn.execute(
                text("SELECT stock FROM inventory WHERE sku=:sku"),
                {"sku": sku},
            ).scalar_one()

        return Quantity(int(remaining))
