# backend/create_tables.py
from database import engine
from models import Base  # Ensure that your models.py defines Base = declarative_base()

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

if __name__ == "__main__":
    create_tables()
