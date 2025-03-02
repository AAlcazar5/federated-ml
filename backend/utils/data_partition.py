import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, random_split

def load_mnist_dataset(train: bool = True, download: bool = True):
    """
    Load the MNIST dataset with standard normalization.
    
    Args:
        train (bool): If True, loads the training dataset; otherwise, loads the test dataset.
        download (bool): If True, downloads the dataset if not present.
    
    Returns:
        torch.utils.data.Dataset: The MNIST dataset.
    """
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))  # Using MNIST mean and std
    ])
    dataset = datasets.MNIST(root="./data", train=train, download=download, transform=transform)
    return dataset

def partition_dataset(dataset, num_clients: int):
    """
    Partition a dataset into `num_clients` subsets using IID random splitting.
    
    Args:
        dataset (torch.utils.data.Dataset): The dataset to partition.
        num_clients (int): Number of subsets/clients.
        
    Returns:
        List[torch.utils.data.Subset]: A list of dataset subsets.
    """
    total_size = len(dataset)
    partition_size = total_size // num_clients
    # Distribute any remainder evenly among the first few partitions
    lengths = [partition_size] * num_clients
    remainder = total_size - partition_size * num_clients
    for i in range(remainder):
        lengths[i] += 1
    
    subsets = random_split(dataset, lengths)
    return subsets

def create_data_loaders(subsets, batch_size: int = 32, shuffle: bool = True):
    """
    Given a list of dataset subsets, create a DataLoader for each subset.
    
    Args:
        subsets (List[torch.utils.data.Subset]): List of dataset partitions.
        batch_size (int): Batch size for the DataLoaders.
        shuffle (bool): Whether to shuffle the data.
        
    Returns:
        List[torch.utils.data.DataLoader]: A list of DataLoaders.
    """
    data_loaders = [DataLoader(subset, batch_size=batch_size, shuffle=shuffle) for subset in subsets]
    return data_loaders

if __name__ == "__main__":
    # Example: Partition the training MNIST dataset for 2 simulated clients.
    dataset = load_mnist_dataset(train=True)
    subsets = partition_dataset(dataset, num_clients=2)
    loaders = create_data_loaders(subsets, batch_size=32)
    
    print(f"Total dataset size: {len(dataset)}")
    for idx, subset in enumerate(subsets):
        print(f"Client {idx} dataset size: {len(subset)}")
