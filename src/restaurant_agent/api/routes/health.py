from typing import Annotated, Literal

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from restaurant_agent.core.config import Settings, get_settings

router = APIRouter(prefix="/health", tags=["health"])


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    service: str
    environment: str


@router.get("/live", response_model=HealthResponse)
async def liveness(
    settings: Annotated[Settings, Depends(get_settings)],
) -> HealthResponse:
    return HealthResponse(
        service=settings.app_name,
        environment=settings.environment,
    )


@router.get("/ready", response_model=HealthResponse)
async def readiness(
    settings: Annotated[Settings, Depends(get_settings)],
) -> HealthResponse:
    return HealthResponse(
        service=settings.app_name,
        environment=settings.environment,
    )
