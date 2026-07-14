from sqlalchemy import ForeignKeyConstraint, UniqueConstraint

from market_data_insights_api.db import Base
from market_data_insights_api.models import Asset, Price


def test_asset_and_price_tables_are_registered() -> None:
    assert Base.metadata.tables["assets"] is Asset.__table__
    assert Base.metadata.tables["prices"] is Price.__table__


def test_asset_model_columns() -> None:
    columns = Asset.__table__.columns

    assert columns["symbol"].unique is True
    assert columns["symbol"].index is True
    assert columns["symbol"].nullable is False
    assert columns["currency"].type.length == 3


def test_price_model_links_to_asset_and_prevents_duplicate_timestamps() -> None:
    constraints = Price.__table__.constraints

    assert any(
        isinstance(constraint, ForeignKeyConstraint)
        and constraint.elements[0].target_fullname == "assets.id"
        for constraint in constraints
    )
    assert any(
        isinstance(constraint, UniqueConstraint)
        and constraint.name == "uq_prices_asset_timestamp"
        for constraint in constraints
    )
