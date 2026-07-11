from fastapi import FastAPI

from market_data_insights_api.api.routes.health import router as health_router
from market_data_insights_api.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="API for market data ingestion and financial insights.",
    )

    app.include_router(health_router)

    return app


app = create_app()
