from datetime import UTC, datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from market_data_insights_api.ingestion import MarketDataAsset, MarketDataPrice


def test_market_data_asset_normalizes_text_fields() -> None:
    asset = MarketDataAsset(
        symbol=" aapl ",
        name=" Apple Inc. ",
        asset_type="equity",
        currency=" usd ",
        exchange=" nasdaq ",
    )

    assert asset.symbol == "AAPL"
    assert asset.name == "Apple Inc."
    assert asset.currency == "USD"
    assert asset.exchange == "NASDAQ"


def test_market_data_asset_rejects_blank_required_text() -> None:
    with pytest.raises(ValidationError):
        MarketDataAsset(symbol="AAPL", name=" ")


def test_market_data_price_requires_timezone_aware_timestamp() -> None:
    with pytest.raises(ValidationError):
        MarketDataPrice(
            timestamp=datetime(2026, 8, 8),
            open_price=Decimal("100.00"),
            high_price=Decimal("110.00"),
            low_price=Decimal("99.50"),
            close_price=Decimal("105.25"),
            volume=Decimal("1234567"),
        )


def test_market_data_price_rejects_negative_values() -> None:
    with pytest.raises(ValidationError):
        MarketDataPrice(
            timestamp=datetime(2026, 8, 8, tzinfo=UTC),
            open_price=Decimal("-1.00"),
            high_price=Decimal("110.00"),
            low_price=Decimal("99.50"),
            close_price=Decimal("105.25"),
            volume=Decimal("1234567"),
        )


def test_market_data_price_rejects_high_below_low() -> None:
    with pytest.raises(ValidationError):
        MarketDataPrice(
            timestamp=datetime(2026, 8, 8, tzinfo=UTC),
            open_price=Decimal("100.00"),
            high_price=Decimal("98.00"),
            low_price=Decimal("99.50"),
            close_price=Decimal("105.25"),
            volume=Decimal("1234567"),
        )
