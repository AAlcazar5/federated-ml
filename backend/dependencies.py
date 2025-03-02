from fastapi import Header, HTTPException, Depends
from typing import Optional
from config import settings

async def get_token_header(x_token: Optional[str] = Header(None)):
    """
    Dependency that validates the X-Token header against the secret key.
    Raises an HTTPException if the header is missing or invalid.
    """
    if x_token is None or x_token != settings.ACCESS_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid or missing X-Token header")
    return x_token

def get_simulation_params():
    """
    Dependency that returns simulation parameters from the configuration.
    """
    return {
        "num_rounds": settings.NUM_ROUNDS,
        "num_clients": settings.NUM_CLIENTS,
        "fraction_fit": settings.FRACTION_FIT,
    }
