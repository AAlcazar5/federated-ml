# backend/config.py
from pydantic import BaseSettings, AnyUrl, Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "Federated Learning Simulation with Tokenized Incentives"
    DEBUG: bool = True

    # Simulation parameters
    NUM_ROUNDS: int = 100
    NUM_CLIENTS: int = 2
    FRACTION_FIT: float = 0.5

    # Token incentive configuration
    TOKEN_REWARD_SCALING_FACTOR: float = 10.0

    # Database configuration: must be provided via .env
    DATABASE_URL: AnyUrl = Field(..., env="DATABASE_URL")

    # Dummy secret keys for development
    ACCESS_SECRET_KEY: str = Field("dummy_access_secret", env="ACCESS_SECRET_KEY")
    RESET_PASSWORD_SECRET_KEY: str = Field("dummy_reset_secret", env="RESET_PASSWORD_SECRET_KEY")
    VERIFICATION_SECRET_KEY: str = Field("dummy_verification_secret", env="VERIFICATION_SECRET_KEY")

    # CORS configuration: list of allowed origins
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
