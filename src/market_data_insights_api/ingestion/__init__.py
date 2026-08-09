"""Market data ingestion package."""

from market_data_insights_api.ingestion.schemas import MarketDataAsset, MarketDataPrice
from market_data_insights_api.ingestion.yahoo_finance_client import (
    YahooFinanceClient,
    YahooFinanceMarketData,
)

__all__ = [
    "MarketDataAsset",
    "MarketDataPrice",
    "YahooFinanceClient",
    "YahooFinanceMarketData",
]
