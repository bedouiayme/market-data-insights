from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

from market_data_insights_api.ingestion.schemas import MarketDataAsset, MarketDataPrice

TickerFactory = Callable[[str], Any]


@dataclass(frozen=True)
class YahooFinanceMarketData:
    asset: MarketDataAsset
    prices: list[MarketDataPrice]


class YahooFinanceClient:
    def __init__(self, ticker_factory: TickerFactory | None = None) -> None:
        self._ticker_factory = ticker_factory or self._default_ticker_factory

    def get_asset(self, symbol: str) -> MarketDataAsset:
        ticker = self._ticker_factory(symbol.strip().upper())
        info = getattr(ticker, "info", {}) or {}

        normalized_symbol = symbol.strip().upper()
        name = info.get("longName") or info.get("shortName") or normalized_symbol

        return MarketDataAsset(
            symbol=normalized_symbol,
            name=name,
            asset_type=self._normalize_asset_type(info.get("quoteType")),
            currency=info.get("currency") or "USD",
            exchange=info.get("exchange"),
        )

    def get_historical_prices(
        self,
        symbol: str,
        *,
        period: str = "1mo",
        interval: str = "1d",
    ) -> list[MarketDataPrice]:
        ticker = self._ticker_factory(symbol.strip().upper())
        history = ticker.history(period=period, interval=interval)

        if getattr(history, "empty", False):
            return []

        prices: list[MarketDataPrice] = []
        for timestamp, row in history.iterrows():
            if self._has_missing_price_fields(row):
                continue

            prices.append(
                MarketDataPrice(
                    timestamp=self._normalize_timestamp(timestamp),
                    open_price=self._to_decimal(row["Open"]),
                    high_price=self._to_decimal(row["High"]),
                    low_price=self._to_decimal(row["Low"]),
                    close_price=self._to_decimal(row["Close"]),
                    volume=self._to_decimal(row["Volume"]),
                )
            )

        return prices

    def get_market_data(
        self,
        symbol: str,
        *,
        period: str = "1mo",
        interval: str = "1d",
    ) -> YahooFinanceMarketData:
        return YahooFinanceMarketData(
            asset=self.get_asset(symbol),
            prices=self.get_historical_prices(symbol, period=period, interval=interval),
        )

    @staticmethod
    def _default_ticker_factory(symbol: str) -> Any:
        import yfinance as yf

        return yf.Ticker(symbol)

    @staticmethod
    def _normalize_asset_type(quote_type: str | None) -> str:
        if quote_type is None:
            return "equity"

        normalized_quote_type = quote_type.strip().lower()
        if normalized_quote_type == "etf":
            return "etf"
        if normalized_quote_type == "cryptocurrency":
            return "crypto"
        if normalized_quote_type == "index":
            return "index"

        return "equity"

    @staticmethod
    def _normalize_timestamp(value: Any) -> datetime:
        timestamp = value.to_pydatetime() if hasattr(value, "to_pydatetime") else value
        if not isinstance(timestamp, datetime):
            raise TypeError("timestamp must be a datetime-compatible value")

        if timestamp.tzinfo is None or timestamp.tzinfo.utcoffset(timestamp) is None:
            return timestamp.replace(tzinfo=UTC)

        return timestamp

    @staticmethod
    def _to_decimal(value: Any) -> Decimal:
        return Decimal(str(value))

    @classmethod
    def _has_missing_price_fields(cls, row: Any) -> bool:
        return any(
            cls._is_missing(row[column])
            for column in ("Open", "High", "Low", "Close", "Volume")
        )

    @staticmethod
    def _is_missing(value: Any) -> bool:
        return value is None or value != value
