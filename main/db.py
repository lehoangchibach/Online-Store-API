from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


def _init_db_session():
    from main._config import config

    engine = create_engine(
        url=config.SQLALCHEMY_DATABASE_URI,
        **config.SQLALCHEMY_ENGINE_OPTIONS,
    )
    session_maker = sessionmaker(
        autocommit=False,
        autoflush=False,
        expire_on_commit=True,
        bind=engine,
    )
    return scoped_session(session_maker)


session = _init_db_session()
