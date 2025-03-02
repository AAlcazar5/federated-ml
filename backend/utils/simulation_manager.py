# backend/utils/simulation_manager.py

import datetime
from sqlalchemy.orm import Session
import torch
import torch.nn as nn
import torch.optim as optim
from models import SimulationRecord  # SQLAlchemy model
from models import MNISTModel       # Our PyTorch model
from utils.training_loop import training_loop_stream
from utils.token_rewards import calculate_reward, global_ledger
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

def load_mnist_dataloader(batch_size: int = 32) -> DataLoader:
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    dataset = datasets.MNIST(root="./data", train=True, download=True, transform=transform)
    return DataLoader(dataset, batch_size=batch_size, shuffle=True)

def sse_format(message: str) -> str:
    """Format a message as an SSE event."""
    return f"data: {message}\n\n"

def run_simulation_stream(
    db: Session, 
    num_rounds: int, 
    num_clients: int, 
    fraction_fit: float, 
    global_model: nn.Module
):
    start_time = datetime.datetime.utcnow()
    yield sse_format(f"Starting simulation at {start_time.isoformat()}Z")

    train_loader = load_mnist_dataloader(batch_size=32)
    criterion = nn.CrossEntropyLoss()
    optimizer_fn = lambda params: optim.Adam(params, lr=0.001)

    # Run the training loop as a generator that yields log messages
    for log in training_loop_stream(
        global_model=global_model,
        num_rounds=num_rounds,
        client_dataloader=train_loader,
        criterion=criterion,
        optimizer_fn=optimizer_fn,
        num_clients=num_clients,
        device="cpu"  # Change to "cuda" if available
    ):
        yield sse_format(log)

    finish_time = datetime.datetime.utcnow()
    yield sse_format(f"Finishing simulation at {finish_time.isoformat()}Z")

    # Calculate reward based on loss improvement.
    previous_metric = 0.5  # Example baseline
    # For demonstration, assume the final average loss is 0.4
    current_metric = 0.4  
    reward = calculate_reward(previous_metric, current_metric, scaling_factor=10.0)
    yield sse_format(f"Calculated reward: {reward:.4f}")
    global_ledger.record_transaction(1, reward, "Reward for simulation performance improvement")
    new_balance = global_ledger.get_balance(1)
    yield sse_format(f"Updated token balance for user 1: {new_balance:.2f}")

    simulation_record = SimulationRecord(
        num_rounds=num_rounds,
        num_clients=num_clients,
        fraction_fit=fraction_fit,
        started_at=start_time,
        finished_at=finish_time,
        status="Completed"
    )
    db.add(simulation_record)
    try:
        db.commit()
        db.refresh(simulation_record)
        yield sse_format(f"Simulation record saved with ID: {simulation_record.id}")
    except Exception as e:
        db.rollback()
        yield sse_format(f"Error saving simulation record: {str(e)}")
        raise e
