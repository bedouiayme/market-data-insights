import httpx
import pytest
from market_data_insights_api.core.config import get_settings
from market_data_insights_api.main import create_app


@pytest.mark.anyio
async def test_health_check_returns_service_status(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ENVIRONMENT", "local")
    get_settings.cache_clear()

    transport = httpx.ASGITransport(app=create_app())

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "Market Data Insights API",
        "version": "0.1.0",
        "environment": "local",
    }

    get_settings.cache_clear()
