from sqlalchemy import select
from sqlalchemy.orm import Session

from market_data_insights_api.ingestion import YahooFinanceClient, YahooFinanceMarketData
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
