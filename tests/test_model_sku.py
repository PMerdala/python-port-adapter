"""Tests for the SKU model."""

import pytest

from domain.errors import InvalidSKUError
from domain.models import SKU


@pytest.mark.parametrize(
    ("input_value", "expected"),
    [
        ("ABC", "ABC"),
        ("ABC", SKU("ABC")),
        (" ABC", SKU("ABC")),
        ("ABC ", SKU("ABC")),
        (" ABC ", SKU("ABC")),
        ("abc", SKU("ABC")),
    ],
)
def test_sku_created_correctly(
    input_value: str | None,
    expected: str | SKU,
) -> None:
    """Test that creating a SKU with valid input returns the expected SKU."""
    result = SKU(input_value)
    assert result == expected


@pytest.mark.parametrize(
    ("input_value", "expected_exception"),
    [
        (None, InvalidSKUError),
        ("", InvalidSKUError),
        ("\t\t\t\t", InvalidSKUError),
        ("     ", InvalidSKUError),
        ("AB", InvalidSKUError),
        (" AB", InvalidSKUError),
        ("AB ", InvalidSKUError),
    ],
)
def test_sku_created_fail(
    input_value: str | None,
    expected_exception: type[Exception],
) -> None:
    """Test that creating a SKU with invalid input raises the expected exception."""
    with pytest.raises(expected_exception):
        SKU(input_value)
