from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import Mock

from market_data_insights_api.ingestion import (
    MarketDataAsset,
    MarketDataPrice,
    YahooFinanceMarketData,
)
from market_data_insights_api.services import PriceIngestionService
from market_data_insights_api.ingestion import YahooFinanceClient

SAMPLE_ASSET_SYMBOL = "AAPL"
SAMPLE_ASSET_NAME = "Apple Inc."
SAMPLE_ASSET_CURRENCY = "USD"
SAMPLE_ASSET_EXCHANGE = "NMS"
SAMPLE_PRICE_TIMESTAMP = datetime(2026, 8, 8, tzinfo=UTC)
SAMPLE_PRICE_OPEN = Decimal("100.12")
SAMPLE_PRICE_HIGH = Decimal("110.34")
SAMPLE_PRICE_LOW = Decimal("99.56")
SAMPLE_PRICE_CLOSE = Decimal("105.78")
SAMPLE_PRICE_VOLUME = Decimal("1234567")
SAMPLE_PERIOD = "5d"
SAMPLE_INTERVAL = "1d"
SAMPLE_DEFAULT_PERIOD = "1mo"
SAMPLE_DEFAULT_INTERVAL = "1d"


def build_sample_market_data() -> YahooFinanceMarketData:
    return YahooFinanceMarketData(
        asset=MarketDataAsset(
            symbol=SAMPLE_ASSET_SYMBOL,
            name=SAMPLE_ASSET_NAME,
            currency=SAMPLE_ASSET_CURRENCY,
            exchange=SAMPLE_ASSET_EXCHANGE,
        ),
        prices=[
            MarketDataPrice(
                timestamp=SAMPLE_PRICE_TIMESTAMP,
                open_price=SAMPLE_PRICE_OPEN,
                high_price=SAMPLE_PRICE_HIGH,
                low_price=SAMPLE_PRICE_LOW,
                close_price=SAMPLE_PRICE_CLOSE,
                volume=SAMPLE_PRICE_VOLUME,
            )
        ],
    )


def test_fetch_market_data_receives_data_from_yahoo_finance_client() -> None:
    sample_market_data = build_sample_market_data()
    market_data_client = Mock()
    market_data_client.get_market_data.return_value = sample_market_data
    service = PriceIngestionService(market_data_client=market_data_client)

    result = service.fetch_market_data(
        " aapl ",
        period=SAMPLE_PERIOD,
        interval=SAMPLE_INTERVAL,
    )

    assert result is sample_market_data
    market_data_client.get_market_data.assert_called_once_with(
        SAMPLE_ASSET_SYMBOL,
        period=SAMPLE_PERIOD,
        interval=SAMPLE_INTERVAL,
    )


def test_fetch_market_data_uses_default_period_and_interval() -> None:
    sample_market_data = build_sample_market_data()
    market_data_client = Mock(spec=YahooFinanceClient)
    market_data_client.get_market_data.return_value = sample_market_data
    service = PriceIngestionService(market_data_client=market_data_client)

    service.fetch_market_data("MSFT")

    market_data_client.get_market_data.assert_called_once_with(
        "MSFT",
        period=SAMPLE_DEFAULT_PERIOD,
        interval=SAMPLE_DEFAULT_INTERVAL,
    )
