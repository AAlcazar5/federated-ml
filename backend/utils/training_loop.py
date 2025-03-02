# backend/utils/training_loop.py

import copy
import numpy as np
import torch
from torch import nn
from torch.optim import Optimizer
from torch.utils.data import DataLoader
from typing import List, Callable, Generator

def aggregate_updates(client_updates: List[dict]) -> dict:
    """
    Aggregate client updates by computing the element-wise average of the updates.
    """
    aggregated_update = {}
    keys = client_updates[0].keys()
    for key in keys:
        total_update = sum(client_update[key] for client_update in client_updates)
        aggregated_update[key] = total_update / len(client_updates)
    return aggregated_update

def training_loop_stream(
    global_model: nn.Module,
    num_rounds: int,
    client_dataloader: DataLoader,
    criterion: nn.Module,
    optimizer_fn: Callable[[List[torch.nn.parameter.Parameter]], Optimizer],
    num_clients: int = 1,
    device: str = "cpu"
) -> Generator[str, None, None]:
    """
    A generator version of the federated training loop that yields log messages as each round is processed.
    
    Yields:
        Log messages as strings.
    """
    yield f"Initial global_model type: {type(global_model)}\n"
    global_model.to(device)
    global_weights = copy.deepcopy(global_model.state_dict())

    for round_num in range(num_rounds):
        yield f"=== Round {round_num + 1} ===\n"
        client_updates = []
        client_losses = []

        for client in range(num_clients):
            # Create a fresh client model and load global weights
            client_model = copy.deepcopy(global_model)
            client_model.load_state_dict(global_weights)
            client_model.to(device)
            client_model.train()

            optimizer = optimizer_fn(client_model.parameters())
            running_loss = 0.0
            total_batches = 0

            # One epoch of training for the client
            for batch in client_dataloader:
                inputs, targets = batch
                inputs, targets = inputs.to(device), targets.to(device)
                optimizer.zero_grad()
                outputs = client_model(inputs)
                loss = criterion(outputs, targets)
                loss.backward()
                optimizer.step()

                running_loss += loss.item()
                total_batches += 1

            avg_client_loss = running_loss / total_batches if total_batches > 0 else 0.0
            client_losses.append(avg_client_loss)
            yield f"Client {client} average loss: {avg_client_loss:.4f}\n"

            # Calculate update: difference between client model and global weights
            client_state = client_model.state_dict()
            update = {key: client_state[key] - global_weights[key] for key in global_weights.keys()}
            client_updates.append(update)

        # Aggregate client updates and update global weights
        aggregated_update = aggregate_updates(client_updates)
        for key in global_weights.keys():
            global_weights[key] += aggregated_update[key]

        round_avg_loss = sum(client_losses) / num_clients
        yield f"Average loss for round {round_num + 1}: {round_avg_loss:.4f}\n"

    global_model.load_state_dict(global_weights)
    yield "Training loop completed.\n"
