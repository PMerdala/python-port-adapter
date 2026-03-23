"""Module for custom exceptions used in the application."""


class DomainError(Exception):
    """Base class for domain errors."""


class InvalidSKUError(DomainError):
    """Raised when an attempt is made to create a SKU with an empty value."""

    def __init__(self, value: str | None = None) -> None:
        """Initialize the InvalidSKUError with a default message."""
        self.value = value
        if value is None:
            message = "SKU cannot be empty"
        elif isinstance(value, str) and len(value.strip()) < 3:
            message = f"Wrong SKU code: received '{value}'"
        super().__init__(message)


class OutOfStockError(DomainError):
    """Raised when an order cannot be fulfilled due to insufficient stock."""

    def __init__(self, sku: str, requested: int, available: int) -> None:
        """Initialize the OutOfStockError with SKU, requested quantity, and available stock."""
        self.sku = sku
        self.requested = requested
        self.available = available
        super().__init__(
            f"Out of stock for SKU '{sku}': requested {requested}, available {available}",
        )


class InvalidQuantityError(DomainError):
    """Raised when an invalid quantity is provided for an order."""

    def __init__(self, qty: int) -> None:
        """Initialize the InvalidQuantityError with the invalid quantity."""
        self.qty = qty
        super().__init__(f"Invalid quantity: {qty}")


class UnknownSKUError(DomainError):
    """Raised when an unknown SKU is requested."""

    def __init__(self, sku: str) -> None:
        """Initialize the UnknownSKUError with the unknown SKU."""
        self.sku = sku
        super().__init__(f"Unknown SKU: '{sku}' not found in inventory.")
