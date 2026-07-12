import pytest
from market_data_insights_api.core.config import Settings


def test_settings_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ENVIRONMENT", "local")

    settings = Settings()

    assert settings.app_name == "Market Data Insights API"
    assert settings.app_version == "0.1.0"
    assert settings.environment == "local"
    assert "postgresql+psycopg://" in settings.database_url
