# backend/models.py

import datetime
import torch
import torch.nn as nn
from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SimulationRecord(Base):
    __tablename__ = "simulation_records"
    
    id = Column(Integer, primary_key=True, index=True)
    num_rounds = Column(Integer, nullable=False)
    num_clients = Column(Integer, nullable=False)
    fraction_fit = Column(Float, nullable=False)
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)
    status = Column(String, default="pending")

# A proper PyTorch model for MNIST classification
class MNISTModel(nn.Module):
    def __init__(self):
        super(MNISTModel, self).__init__()
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(784, 128)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(128, 10)
    
    def forward(self, x):
        x = self.flatten(x)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x
