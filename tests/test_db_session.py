from sqlalchemy.orm import Session

from market_data_insights_api.db.session import SessionLocal, engine, get_db


def test_engine_uses_configured_database_url() -> None:
    assert engine.url.drivername == "postgresql+psycopg"
    assert engine.url.database == "market_data"


def test_session_factory_creates_sqlalchemy_session() -> None:
    session = SessionLocal()
    try:
        assert isinstance(session, Session)
    finally:
        session.close()


def test_get_db_yields_session() -> None:
    db_generator = get_db()
    session = next(db_generator)

    try:
        assert isinstance(session, Session)
    finally:
        db_generator.close()
