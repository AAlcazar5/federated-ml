import datetime
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import SimulationRecord
from sqlalchemy.exc import SQLAlchemyError

def create_tables():
    # Create tables if they do not exist yet.
    # Note: In production, use Alembic for migrations.
    from models import Base
    Base.metadata.create_all(bind=engine)

def seed_simulations(db: Session):
    # Create dummy simulation records.
    record1 = SimulationRecord(
        num_rounds=100,
        num_clients=2,
        fraction_fit=0.5,
        started_at=datetime.datetime.utcnow(),
        finished_at=None,
        status="Running"
    )
    record2 = SimulationRecord(
        num_rounds=200,
        num_clients=3,
        fraction_fit=0.6,
        started_at=datetime.datetime.utcnow() - datetime.timedelta(days=1),
        finished_at=datetime.datetime.utcnow(),
        status="Completed"
    )
    try:
        db.add(record1)
        db.add(record2)
        db.commit()
        print("Seeded simulation records successfully.")
    except SQLAlchemyError as e:
        db.rollback()
        print("Error seeding simulation records:", e)

if __name__ == "__main__":
    create_tables()
    db = SessionLocal()
    seed_simulations(db)
    db.close()
