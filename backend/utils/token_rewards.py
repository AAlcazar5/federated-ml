# backend/utils/token_rewards.py

import datetime
from typing import List, Dict, Any

def calculate_reward(previous_metric: float, current_metric: float, scaling_factor: float = 10.0) -> float:
    """
    Calculate a token reward based on the improvement in a performance metric.
    For example, if the metric is loss (where lower is better):
       reward = (previous_loss - current_loss) * scaling_factor
    """
    improvement = previous_metric - current_metric
    if improvement > 0:
        return improvement * scaling_factor
    return 0.0

class TokenLedger:
    def __init__(self) -> None:
        # Ledger is a dictionary mapping user IDs to a list of transaction records.
        self.ledger: Dict[int, List[Dict[str, Any]]] = {}

    def record_transaction(self, user_id: int, amount: float, description: str = "") -> None:
        transaction = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "amount": amount,
            "description": description,
        }
        if user_id not in self.ledger:
            self.ledger[user_id] = []
        self.ledger[user_id].append(transaction)

    def get_balance(self, user_id: int) -> float:
        if user_id not in self.ledger:
            return 0.0
        return sum(tx["amount"] for tx in self.ledger[user_id])

    def transfer_tokens(self, sender_id: int, receiver_id: int, amount: float, description: str = "") -> None:
        if self.get_balance(sender_id) < amount:
            raise ValueError("Insufficient funds for transfer")
        self.record_transaction(sender_id, -amount, f"Transfer to user {receiver_id}: {description}")
        self.record_transaction(receiver_id, amount, f"Transfer from user {sender_id}: {description}")

# Global ledger instance to be used across the app
global_ledger = TokenLedger()
