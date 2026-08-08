from datetime import datetime
from decimal import Decimal
from typing import Self

from pydantic import BaseModel, ConfigDict, field_validator, model_validator


class MarketDataAsset(BaseModel):
    model_config = ConfigDict(frozen=True)

    symbol: str
    name: str
    asset_type: str = "equity"
    currency: str = "USD"
    exchange: str | None = None

    @field_validator("symbol", "currency")
    @classmethod
    def normalize_uppercase(cls, value: str) -> str:
        return value.strip().upper()

    @field_validator("name", "asset_type")
    @classmethod
    def reject_blank_text(cls, value: str) -> str:
        normalized_value = value.strip()
        if not normalized_value:
            raise ValueError("value must not be blank")
        return normalized_value

    @field_validator("exchange")
    @classmethod
    def normalize_optional_exchange(cls, value: str | None) -> str | None:
        if value is None:
            return None

        normalized_value = value.strip().upper()
        return normalized_value or None


class MarketDataPrice(BaseModel):
    model_config = ConfigDict(frozen=True)

    timestamp: datetime
    open_price: Decimal
    high_price: Decimal
    low_price: Decimal
    close_price: Decimal
    volume: Decimal

    @field_validator("timestamp")
    @classmethod
    def require_timezone_aware_timestamp(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            raise ValueError("timestamp must be timezone-aware")
        return value

    @field_validator("open_price", "high_price", "low_price", "close_price", "volume")
    @classmethod
    def reject_negative_values(cls, value: Decimal) -> Decimal:
        if value < 0:
            raise ValueError("value must be non-negative")
        return value

    @model_validator(mode="after")
    def validate_price_range(self) -> Self:
        if self.high_price < self.low_price:
            raise ValueError("high_price must be greater than or equal to low_price")
        return self
