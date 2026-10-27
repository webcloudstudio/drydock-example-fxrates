"""Application factory. Building the app opens no store and initializes no schema."""

from __future__ import annotations

import importlib
import pkgutil

from fastapi import APIRouter, FastAPI

from app_server import routers as routers_package


def create_app() -> FastAPI:
    """Build the application and include every router found in app_server/routers."""
    app = FastAPI()
    for module_info in pkgutil.iter_modules(routers_package.__path__):
        module = importlib.import_module(f"{routers_package.__name__}.{module_info.name}")
        router = getattr(module, "router", None)
        if isinstance(router, APIRouter):
            app.include_router(router)
    return app


app = create_app()
