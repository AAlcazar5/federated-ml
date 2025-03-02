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

    Create a Python virtual environment and activate it:

python3 -m venv fmlenv
source fmlenv/bin/activate

Install the backend dependencies:

pip install -r requirements.txt

Configure Environment Variables:

Create a .env file in the backend folder with the following content (adjust the values as needed):

DATABASE_URL=postgresql://myuser:mypassword@localhost:5432/mydb
ACCESS_SECRET_KEY=dummy_access_secret
RESET_PASSWORD_SECRET_KEY=dummy_reset_secret
VERIFICATION_SECRET_KEY=dummy_verification_secret

Set Up PostgreSQL:

Make sure PostgreSQL is installed and running. You can use Homebrew on macOS:

brew install postgresql
brew services start postgresql

Then create a database and user:

psql postgres
CREATE USER myuser WITH PASSWORD 'mypassword';
CREATE DATABASE mydb OWNER myuser;
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
\q

Create Database Tables:

Run the table creation script:

    python create_tables.py

Frontend Setup

    Navigate to the frontend folder:

cd ../frontend

Install Node.js dependencies:

    npm install

    Configure Tailwind CSS:
    Follow Tailwind’s installation guide if not already configured.

Running the Application
Start the Backend

In the backend directory (with the virtual environment activated):

uvicorn main:app --host 0.0.0.0 --port 8000 --reload

This will start the FastAPI backend on http://localhost:8000.
Start the Frontend

In the frontend directory:

npm run dev

This will start the Next.js app on http://localhost:3000.
Usage Instructions
Trigger a Simulation

    On the Home Page:
    The home page displays a green "Start Simulation" button. Click this button to trigger a new simulation. The simulation is run on the backend using federated training on MNIST data. Simulation logs (including training results and rewards) are streamed in real time and displayed on the page.

    Real-Time Logs:
        Training Results: A summary of key results (such as calculated rewards and simulation record IDs) is displayed immediately below the button.
        Simulation Logs: Detailed logs from each training round are streamed and appear in a scrollable container below the training results.
        Auto-Scroll Behavior: The logs container automatically scrolls to the bottom as new log messages are added. Once the simulation completes and the summary is available, the page scrolls back to the top.

Viewing Simulation Records and Rewards

    Simulation Records:
    You can navigate to /simulations (or use the appropriate link) to view all simulation records stored in the database.

    Rewards Ledger:
    The rewards ledger is accessible via the /api/incentives/ledger endpoint and is displayed on the home page if integrated with the rewards component.

Testing & Iteration

    Iterate on the Training Loop:
    The training loop logs average losses per round and updates model weights based on real computed loss values from client training. Review the logs to see performance trends.

    Refine the Incentive Mechanism:
    Adjust the scaling factor or reward calculation in utils/token_rewards.py as needed based on observed node performance.

    Real-Time Log Streaming:
    The system uses Server-Sent Events (SSE) to stream logs to the frontend. For real-time feedback during training, ensure the SSE connection is stable and that your backend is sending properly formatted events.

Additional Notes

    CORS Configuration:
    The FastAPI backend includes CORS middleware configured to allow requests from the Next.js frontend (http://localhost:3000). Adjust this configuration as needed for production.

    Persistent Ledger Storage:
    The token ledger currently uses an in-memory global variable (global_ledger). For production, consider persisting this data in a database or a distributed cache to handle multiple backend instances.

License

This project is licensed under the MIT License.