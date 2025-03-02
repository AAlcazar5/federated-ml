# backend/routes/simulations.py

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from schemas import SimulationRecord as SimulationRecordSchema, SimulationStartRequest, SimulationStartResponse
from database import get_db
from utils.simulation_manager import run_simulation_stream
from models import MNISTModel, SimulationRecord as SimulationRecordModel

router = APIRouter()

@router.get("/", response_model=List[SimulationRecordSchema], tags=["Simulations"])
def get_simulations(db: Session = Depends(get_db)):
    try:
        simulations = db.query(SimulationRecordModel).all()
        print(f"Retrieved {len(simulations)} simulation records from the database.")
        return simulations
    except Exception as e:
        print("Error retrieving simulations:", e)
        raise HTTPException(status_code=500, detail=str(e))

# SSE endpoint for streaming simulation logs
@router.get("/stream", tags=["Simulations"])
def start_simulation_stream(
    num_rounds: int = Query(..., description="Number of rounds"),
    num_clients: int = Query(..., description="Number of clients"),
    fraction_fit: float = Query(..., description="Fraction of clients to train"),
    db: Session = Depends(get_db)
):
    # Instantiate a proper PyTorch model for simulation
    global_model = MNISTModel()
    try:
        log_generator = run_simulation_stream(
            db=db,
            num_rounds=num_rounds,
            num_clients=num_clients,
            fraction_fit=fraction_fit,
            global_model=global_model
        )
    except Exception as e:
        print("Error during simulation execution:", e)
        raise HTTPException(status_code=500, detail=str(e))
    
    return StreamingResponse(log_generator, media_type="text/event-stream")
