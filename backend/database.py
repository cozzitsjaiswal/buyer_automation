from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./eu_buyer_automation.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Provide a SQLAlchemy Session for use by callers and ensure the session is closed after use.
    
    Returns:
        Session: A SQLAlchemy Session instance yielded to the caller; the generator guarantees the session is closed when the context is exited.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()