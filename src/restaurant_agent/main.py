from fastapi import FastAPI

from restaurant_agent.api.routes.health import router as health_router
from restaurant_agent.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(
        title=settings.name,
        version="0.1.0",
        description="Restaurant AI agent backend scaffold",
    )
    application.include_router(health_router)
    return application


app = create_app()
