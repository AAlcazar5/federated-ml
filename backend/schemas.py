# backend/schemas.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SimulationRecord(BaseModel):
    id: int
    num_rounds: int
    num_clients: int
    fraction_fit: float
    started_at: datetime
    finished_at: Optional[datetime] = None
    status: str

    class Config:
        orm_mode = True

class SimulationStartRequest(BaseModel):
    num_rounds: int
    num_clients: int
    fraction_fit: float

class SimulationStartResponse(BaseModel):
    message: str
    parameters: dict
    logs: List[str]
