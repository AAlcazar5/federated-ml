import argparse
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import fedml

from .data_partition import load_mnist_dataset, partition_dataset, create_data_loaders

# Define a simple PyTorch model for MNIST classification
class MNISTModel(nn.Module):
    def __init__(self):
        super(MNISTModel, self).__init__()
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(28 * 28, 128)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(128, 10)
    
    def forward(self, x):
        x = self.flatten(x)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

def main():
    parser = argparse.ArgumentParser(description="FedML Client for MNIST Simulation")
    parser.add_argument("--client_id", type=int, default=0, help="ID of the client")
    parser.add_argument("--num_clients", type=int, default=2, help="Total number of clients")
    parser.add_argument("--server_address", type=str, default="127.0.0.1:5000", help="Address of the FedML server")
    parser.add_argument("--num_epochs", type=int, default=1, help="Number of local training epochs")
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Create the model and move it to the appropriate device
    model = MNISTModel().to(device)
    
    # Define optimizer and loss function
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()

    # Load and partition the MNIST training dataset
    full_train_dataset = load_mnist_dataset(train=True)
    partitions = partition_dataset(full_train_dataset, num_clients=args.num_clients)
    
    # Validate client_id
    if args.client_id < 0 or args.client_id >= len(partitions):
        raise ValueError(f"Invalid client_id {args.client_id}. Must be between 0 and {len(partitions)-1}.")
    
    # Create DataLoader for this client's partition
    train_loader = create_data_loaders([partitions[args.client_id]], batch_size=32, shuffle=True)[0]

    # For testing, we load the full test dataset (or you can partition it similarly)
    test_dataset = load_mnist_dataset(train=False)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
    
    # Set up FedML Runner (using FedML's unified API)
    fedml_runner = fedml.FedMLRunner()
    fedml_runner.setup_training_args(args)
    
    # Run the FedML client: this function should handle the communication with the server,
    # local training, and evaluation using the provided DataLoaders.
    fedml_runner.run(
        model=model,
        train_dataloader=train_loader,
        test_dataloader=test_loader,
        optimizer=optimizer,
        loss_func=criterion,
        device=device,
        num_epochs=args.num_epochs,
    )

if __name__ == "__main__":
    main()
