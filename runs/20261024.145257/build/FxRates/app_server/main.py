"""FastAPI application factory."""


def create_app():
    """Create the HTTP application; routes are added in the API build block."""
    from fastapi import FastAPI

    return FastAPI(title="FxRates")
