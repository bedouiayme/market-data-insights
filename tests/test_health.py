import httpx
import pytest

from app.main import create_app


@pytest.mark.anyio
async def test_health_check_returns_service_status() -> None:
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
