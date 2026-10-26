"""FastAPI application factory and HTTP route ownership boundary."""

from fastapi import FastAPI


def create_app() -> FastAPI:
    """Create the HTTP application; API routes delegate to services."""
    return FastAPI(title="FxRates")


app = create_app()
