"""FastAPI application factory and the module-level app for `uvicorn app_server.main:app`."""

from fastapi import FastAPI

from app_server import routes


def create_app() -> FastAPI:
    """Build a new FastAPI application that includes the shared router."""
    application = FastAPI()
    application.include_router(routes.router)
    return application


app = create_app()
