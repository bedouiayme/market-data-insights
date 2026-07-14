from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from market_data_insights_api.db import Base

if TYPE_CHECKING:
    from market_data_insights_api.models.asset import Asset


class Price(Base):
    __tablename__ = "prices"
    __table_args__ = (
        UniqueConstraint("asset_id", "timestamp", name="uq_prices_asset_timestamp"),
        CheckConstraint("open >= 0", name="ck_prices_open_non_negative"),
        CheckConstraint("high >= 0", name="ck_prices_high_non_negative"),
        CheckConstraint("low >= 0", name="ck_prices_low_non_negative"),
        CheckConstraint("close >= 0", name="ck_prices_close_non_negative"),
        CheckConstraint("volume >= 0", name="ck_prices_volume_non_negative"),
        CheckConstraint("high >= low", name="ck_prices_high_gte_low"),
        Index("ix_prices_asset_timestamp", "asset_id", "timestamp"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"),
        nullable=False,
    )
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    open_price: Mapped[Decimal] = mapped_column("open", Numeric(18, 6), nullable=False)
    high_price: Mapped[Decimal] = mapped_column("high", Numeric(18, 6), nullable=False)
    low_price: Mapped[Decimal] = mapped_column("low", Numeric(18, 6), nullable=False)
    close_price: Mapped[Decimal] = mapped_column("close", Numeric(18, 6), nullable=False)
    volume: Mapped[Decimal] = mapped_column(Numeric(24, 4), nullable=False)

    asset: Mapped["Asset"] = relationship(back_populates="prices")
