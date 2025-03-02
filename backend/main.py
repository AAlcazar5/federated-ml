# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routes import simulations, incentives  # Make sure your routes are imported correctly
from database import engine
from models import Base

# Create tables (for development)
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG)

# Add CORS middleware to allow requests from your frontend (e.g., http://localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can also use ["*"] for development (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(simulations.router, prefix="/api/simulations", tags=["Simulations"])
app.include_router(incentives.router, prefix="/api/incentives", tags=["Incentives"])

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
