from market_data_insights_api.ingestion import YahooFinanceClient, YahooFinanceMarketData


class PriceIngestionService:
    def __init__(self, market_data_client: YahooFinanceClient | None = None) -> None:
        self._market_data_client = market_data_client or YahooFinanceClient()

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
