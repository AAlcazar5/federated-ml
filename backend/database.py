# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings

# Create the engine. Ensure your DATABASE_URL in .env is correctly set.
engine = create_engine(settings.DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency to get a SQLAlchemy DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
