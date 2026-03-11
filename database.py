from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Létrehozunk egy SQLite adatbázis fájlt a projekt mappájában "books.db" néven
SQLALCHEMY_DATABASE_URL = "sqlite:///./books.db"

# Az 'engine' felel a tényleges kapcsolatért az adatbázissal
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# A SessionLocal osztályból fogunk példányokat (session-öket) létrehozni,
# amiken keresztül adatokat írunk/olvasunk
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Ebből az alaposztályból fognak örökölni a mi adatbázis modelljeink
Base = declarative_base()