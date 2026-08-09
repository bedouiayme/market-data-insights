from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import Mock

from market_data_insights_api.ingestion import YahooFinanceClient

SAMPLE_ASSET_INFO = {
    "longName": "Apple Inc.",
    "quoteType": "EQUITY",
    "currency": "USD",
    "exchange": "NMS",
}
SAMPLE_PRICE_TIMESTAMP = datetime(2026, 8, 8)
SAMPLE_PRICE_ROW = {
    "Open": 100.12,
    "High": 110.34,
    "Low": 99.56,
    "Close": 105.78,
    "Volume": 1234567,
}
SAMPLE_PRICE_ROWS = [(SAMPLE_PRICE_TIMESTAMP, SAMPLE_PRICE_ROW)]


def build_ticker_mock(
    *,
    info: dict[str, object] | None = None,
    rows: list[tuple[datetime, dict[str, object]]] | None = None,
) -> Mock:
    history = Mock()
    history.empty = not rows
    history.iterrows.return_value = rows or []

    ticker = Mock()
    ticker.info = info or {}
    ticker.history.return_value = history

    return ticker


def test_get_asset_maps_yahoo_info_to_market_data_asset() -> None:
    ticker = build_ticker_mock(info=SAMPLE_ASSET_INFO)
    ticker_factory = Mock(return_value=ticker)
    client = YahooFinanceClient(ticker_factory=ticker_factory)

    asset = client.get_asset(" aapl ")

    assert asset.symbol == "AAPL"
    assert asset.name == "Apple Inc."
    assert asset.asset_type == "equity"
    assert asset.currency == "USD"
    assert asset.exchange == "NMS"
    ticker_factory.assert_called_once_with("AAPL")


def test_get_historical_prices_maps_yahoo_ohlcv_rows() -> None:
    ticker = build_ticker_mock(rows=SAMPLE_PRICE_ROWS)
    client = YahooFinanceClient(ticker_factory=Mock(return_value=ticker))

    prices = client.get_historical_prices("AAPL", period="5d", interval="1d")

    assert len(prices) == 1
    assert prices[0].timestamp == SAMPLE_PRICE_TIMESTAMP.replace(tzinfo=UTC)
    assert prices[0].open_price == Decimal("100.12")
    assert prices[0].high_price == Decimal("110.34")
    assert prices[0].low_price == Decimal("99.56")
    assert prices[0].close_price == Decimal("105.78")
    assert prices[0].volume == Decimal("1234567")
    ticker.history.assert_called_once_with(period="5d", interval="1d")


def test_get_historical_prices_skips_rows_with_missing_price_fields() -> None:
    row_with_missing_high = {
        **SAMPLE_PRICE_ROW,
        "High": None,
    }
    ticker = build_ticker_mock(rows=[(datetime(2026, 8, 8, tzinfo=UTC), row_with_missing_high)])
    client = YahooFinanceClient(ticker_factory=Mock(return_value=ticker))

    assert client.get_historical_prices("AAPL") == []


def test_get_market_data_returns_asset_and_prices() -> None:
    ticker = build_ticker_mock(
        info={"shortName": "Microsoft", "currency": "USD"},
        rows=[
            (
                datetime(2026, 8, 8, tzinfo=UTC),
                {
                    "Open": 200,
                    "High": 210,
                    "Low": 198,
                    "Close": 205,
                    "Volume": 987654,
                },
            )
        ],
    )
    client = YahooFinanceClient(ticker_factory=Mock(return_value=ticker))

    market_data = client.get_market_data("MSFT")

    assert market_data.asset.symbol == "MSFT"
    assert market_data.asset.name == "Microsoft"
    assert len(market_data.prices) == 1
