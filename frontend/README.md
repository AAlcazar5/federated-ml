# Federated Learning Simulation with Tokenized Incentives

This project is a simulation environment for federated learning that integrates a token-based incentive system. Multiple simulated nodes (clients) collaboratively train a shared model using federated learning. The system calculates rewards based on improvements in model performance and logs these rewards into a ledger. The rewards and simulation logs are displayed on a Next.js frontend.

## Project Purpose

- **Federated Learning Simulation:**  
  Simulate a federated learning environment where multiple clients train a shared model.
  
- **Token-Based Incentives:**  
  Incentivize client contributions by calculating rewards based on performance improvements and record these rewards in a ledger.

- **Real-Time Feedback:**  
  Provide real-time training logs and simulation results on the frontend using Server-Sent Events (SSE).

## Features

- **Backend:**  
  - FastAPI backend with endpoints for triggering simulations and retrieving simulation records.
  - Uses a real training loop with PyTorch on MNIST data.
  - Calculates rewards based on loss improvements.
  - Uses PostgreSQL to store simulation records.
  - Provides Server-Sent Events (SSE) to stream simulation logs in real time.
  - Implements a token ledger using in-memory storage (with a note to consider persistent storage for production).

- **Frontend:**  
  - Next.js application displaying simulation logs and training results in real time.
  - A "Start Simulation" button to trigger simulations.
  - Automatic scrolling behavior for log output and summary display.

## Requirements

- **Backend:**  
  - Python 3.9+
  - FastAPI, Uvicorn
  - SQLAlchemy
  - psycopg2-binary (for PostgreSQL connectivity)
  - PyTorch
  - torchvision
  - Additional Python packages as listed in `requirements.txt`

- **Frontend:**  
  - Node.js (v14 or later)
  - Next.js
  - Tailwind CSS (for styling)

- **Database:**  
  - PostgreSQL (locally installed or running in a container)

## Setup and Installation

### Backend Setup

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd federated-learning-simulation/backend
