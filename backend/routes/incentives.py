# backend/routes/incentives.py

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from utils.token_rewards import calculate_reward, global_ledger

router = APIRouter()

# Request schema for calculating a reward
class RewardRequest(BaseModel):
    user_id: int
    previous_metric: float
    current_metric: float
    scaling_factor: Optional[float] = 10.0

# Response schema for the reward endpoint
class RewardResponse(BaseModel):
    user_id: int
    reward: float
    new_balance: float

@router.post("/reward", response_model=RewardResponse, tags=["Incentives"])
def add_reward(reward_req: RewardRequest):
    try:
        reward = calculate_reward(
            reward_req.previous_metric,
            reward_req.current_metric,
            reward_req.scaling_factor,
        )
        global_ledger.record_transaction(
            reward_req.user_id,
            reward,
            description="Reward for performance improvement"
        )
        # Round balance to 2 decimal places for a cleaner display.
        new_balance = round(global_ledger.get_balance(reward_req.user_id), 2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return RewardResponse(
        user_id=reward_req.user_id,
        reward=reward,
        new_balance=new_balance,
    )

# Response schema for returning the ledger
class LedgerResponse(BaseModel):
    user_id: int
    balance: float
    transactions: List[Dict[str, Any]]

@router.get("/ledger", response_model=LedgerResponse, tags=["Incentives"])
def get_ledger(user_id: int = Query(..., description="User ID to query ledger for")):
    try:
        balance = round(global_ledger.get_balance(user_id), 2)
        transactions = global_ledger.ledger.get(user_id, [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return LedgerResponse(
        user_id=user_id,
        balance=balance,
        transactions=transactions,
    )
