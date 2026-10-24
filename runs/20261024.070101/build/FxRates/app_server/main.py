"""FastAPI application factory for FxRates."""

from fastapi import FastAPI


def create_app() -> FastAPI:
    """Create the API application; routes are added by their feature blocks."""
    return FastAPI(title="FxRates")


app = create_app()
