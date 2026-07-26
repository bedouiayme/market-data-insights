"""create assets and prices tables

Revision ID: 20260726_0001
Revises:
Create Date: 2026-07-26

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260726_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "assets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("symbol", sa.String(length=20), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("asset_type", sa.String(length=50), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("exchange", sa.String(length=100), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_assets_symbol"), "assets", ["symbol"], unique=True)

    op.create_table(
        "prices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("asset_id", sa.Integer(), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("open", sa.Numeric(precision=18, scale=6), nullable=False),
        sa.Column("high", sa.Numeric(precision=18, scale=6), nullable=False),
        sa.Column("low", sa.Numeric(precision=18, scale=6), nullable=False),
        sa.Column("close", sa.Numeric(precision=18, scale=6), nullable=False),
        sa.Column("volume", sa.Numeric(precision=24, scale=4), nullable=False),
        sa.CheckConstraint("close >= 0", name="ck_prices_close_non_negative"),
        sa.CheckConstraint("high >= 0", name="ck_prices_high_non_negative"),
        sa.CheckConstraint("high >= low", name="ck_prices_high_gte_low"),
        sa.CheckConstraint("low >= 0", name="ck_prices_low_non_negative"),
        sa.CheckConstraint("open >= 0", name="ck_prices_open_non_negative"),
        sa.CheckConstraint("volume >= 0", name="ck_prices_volume_non_negative"),
        sa.ForeignKeyConstraint(["asset_id"], ["assets.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("asset_id", "timestamp", name="uq_prices_asset_timestamp"),
    )
    op.create_index("ix_prices_asset_timestamp", "prices", ["asset_id", "timestamp"])


def downgrade() -> None:
    op.drop_index("ix_prices_asset_timestamp", table_name="prices")
    op.drop_table("prices")
    op.drop_index(op.f("ix_assets_symbol"), table_name="assets")
    op.drop_table("assets")
