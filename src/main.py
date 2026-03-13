"""Main application entry point for the Ports & Adapters example."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from api import router
from db import init_db


def on_startup() -> None:
    """Initialize the database on application startup."""
    init_db("sqlite:///./before.db")


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ANN201, ARG001
    """Application lifespan context manager."""
    # Load the ML model
    on_startup()
    yield
    # Clean up the ML models and release the resources


app = FastAPI(title="Ports & adapters", lifespan=lifespan)


app.include_router(router)
