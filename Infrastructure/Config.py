from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.event import listens_for

DATABASE_URL = "sqlite+aiosqlite:///online_school.db?mode=wal"

engine = create_async_engine(DATABASE_URL, echo=True)

@listens_for(engine.sync_engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA case_sensitive_like = OFF")
    cursor.close()

async_session_factory = async_sessionmaker(
    engine,
    expire_on_commit=False
)

Base = declarative_base()