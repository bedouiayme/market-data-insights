from sqlalchemy import select
from sqlalchemy.orm import Session

from market_data_insights_api.ingestion import (
    MarketDataAsset,
    YahooFinanceClient,
    YahooFinanceMarketData,
)
from market_data_insights_api.models import Asset


class PriceIngestionService:
    def __init__(
        self,
        market_data_client: YahooFinanceClient | None = None,
        db_session: Session | None = None,
    ) -> None:
        self._market_data_client = market_data_client or YahooFinanceClient()
        self._db_session = db_session

    def fetch_market_data(
        self,
        symbol: str,
        *,
        period: str = "1mo",
        interval: str = "1d",
    ) -> YahooFinanceMarketData:
        normalized_symbol = symbol.strip().upper()
        return self._market_data_client.get_market_data(
            normalized_symbol,
            period=period,
            interval=interval,
        )

    def _get_asset_by_symbol(self, symbol: str) -> Asset | None:
        if self._db_session is None:
            raise RuntimeError("database session is required to query assets")

        normalized_symbol = symbol.strip().upper()
        statement = select(Asset).where(Asset.symbol == normalized_symbol)

        return self._db_session.execute(statement).scalar_one_or_none()

    def _get_or_create_asset(self, market_data_asset: MarketDataAsset) -> Asset:
        if self._db_session is None:
            raise RuntimeError("database session is required to persist assets")

        existing_asset = self._get_asset_by_symbol(market_data_asset.symbol)
        if existing_asset is not None:
            return existing_asset

        asset = Asset(
            symbol=market_data_asset.symbol,
            name=market_data_asset.name,
            asset_type=market_data_asset.asset_type,
            currency=market_data_asset.currency,
            exchange=market_data_asset.exchange,
        )
        self._db_session.add(asset)
        self._db_session.flush()

        return asset
