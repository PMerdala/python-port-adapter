"""Tests for the Quantity model."""

import sys

import pytest

from domain.errors import InvalidQuantityError
from domain.models import PositiveQuantity, Quantity


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (0, 0),
        (1, 1),
        (5, 5),
        (10, 10),
        (sys.maxsize, sys.maxsize),
    ],
)
def test_create_quantity(value: int, expected: int) -> None:
    """Test creating a Quantity with valid values."""
    qty = Quantity(value)
    assert qty == expected


@pytest.mark.parametrize(
    ("value", "expected_exception"),
    [
        (-1, InvalidQuantityError),
        (-5, InvalidQuantityError),
        (-10, InvalidQuantityError),
    ],
)
def test_create_quantity_fail(value: int, expected_exception: type[Exception]) -> None:
    """Test creating a Quantity with invalid values."""
    with pytest.raises(expected_exception):
        Quantity(value)


def test_create_quantity_with_non_integer() -> None:
    """Test creating a Quantity with a non-integer value."""
    with pytest.raises(TypeError):
        Quantity("not an integer")  # type: ignore


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (1.4, Quantity(1)),
        (1.44, Quantity(1)),
        (1.45, Quantity(1)),
        (1.46, Quantity(1)),
        (1.49, Quantity(1)),
        (1.5, Quantity(1)),
        (1.9, Quantity(1)),
    ],
)
def test_create_quantity_with_float(value: float, expected: int) -> None:
    """Test creating a Quantity with a float value."""
    qty = Quantity(value)
    assert qty == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (1, 1),
        (5, 5),
        (10, 10),
        (sys.maxsize, sys.maxsize),
    ],
)
def test_create_positive_quantity(value: int, expected: int) -> None:
    """Test creating a PositiveQuantity with valid values."""
    qty = PositiveQuantity(value)
    assert qty == expected


@pytest.mark.parametrize(
    ("value", "expected_exception"),
    [
        (0, InvalidQuantityError),
        (-1, InvalidQuantityError),
        (-5, InvalidQuantityError),
        (-10, InvalidQuantityError),
    ],
)
def test_create_positive_quantity_fail(
    value: int,
    expected_exception: type[Exception],
) -> None:
    """Test creating a PositiveQuantity with invalid values."""
    with pytest.raises(expected_exception):
        PositiveQuantity(value)
