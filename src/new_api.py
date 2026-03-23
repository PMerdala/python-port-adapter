"""fastapi api use sqlalchemy.

Will be removed in the future, please use new api instead
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.engine import Connection  # noqa: TC002

from adapters.sqlalchemy_inventory import SqlAlchemyInventoryAdapter
from db import get_db
from domain.errors import (
    InvalidQuantityError,
    InvalidSKUError,
    OutOfStockError,
    UnknownSKUError,
)
from domain.use_cases import place_order
from models import OrderRequest

router = APIRouter()


class PlaceOrderIn(BaseModel):
    """API input model for placing an order."""

    sku: str
    qty: int = Field(..., ge=0)


class PlaceOrderOut(BaseModel):
    """API output model for placing an order."""

    sku: str
    qty: int
    remaining_stock: int


@router.post("/orders", response_model=PlaceOrderOut)
def place_order_endpoint(
    payload: PlaceOrderIn,
    connection: Annotated[Connection, Depends(get_db)],
) -> PlaceOrderOut:
    """API endpoint for placing an order."""  # noqa: D401
    try:
        adapter = SqlAlchemyInventoryAdapter(connection)
        result = place_order(OrderRequest(sku=payload.sku, qty=payload.qty), adapter)
    except InvalidQuantityError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except InvalidSKUError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except UnknownSKUError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except OutOfStockError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e)) from e
    return PlaceOrderOut(
        sku=result.sku,
        qty=result.qty,
        remaining_stock=result.remaining_stock,
    )
