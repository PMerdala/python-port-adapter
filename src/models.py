"""Module defines the data models used in the application."""

from dataclasses import dataclass
from typing import Self

from domain.errors import InvalidQuantityError, InvalidSKUError

MIN_SKU_LENGTH = 3


class SKU(str):
    """A SKU (Stock Keeping Unit) is a unique identifier for a product in inventory."""

    __slots__ = ()

    def __new__(cls: type[SKU], value: str | SKU) -> Self:
        """Create a new SKU instance, ensuring the value is a non-empty string."""
        if (
            value is None
            or not isinstance(value, str)
            or len(value.strip()) < MIN_SKU_LENGTH
        ):
            raise InvalidSKUError(value)
        return super().__new__(cls, value.strip().upper())


class Quantity(int):
    """A Quantity represents the amount of stock for a SKU."""

    __slots__ = ()

    def __new__(cls: type[Quantity], value: int) -> Self:
        """Create a new Quantity instance, ensuring the value is a positive integer."""
        if value < 0:
            raise InvalidQuantityError(value)
        return super().__new__(cls, value)


class PositiveQuantity(Quantity):
    """A Quantity represents the amount of stock for a SKU."""

    __slots__ = ()

    def __new__(cls: type[Quantity], value: int) -> Self:
        """Create a new PositiveQuantity instance, ensuring the value is a positive integer."""
        if value <= 0:
            raise InvalidQuantityError(value)
        return super().__new__(cls, value)


@dataclass(frozen=True)
class OrderRequest:
    """Represents a request to place an order for a specific SKU and quantity."""

    sku: SKU
    qty: PositiveQuantity


@dataclass(frozen=True)
class OrderPlaced:
    """Represents the response after placing an order, including the SKU, quantity, and remaining stock."""

    sku: SKU
    qty: PositiveQuantity
    remaining_stock: Quantity
