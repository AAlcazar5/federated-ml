from utils.data_partition import load_mnist_dataset, partition_dataset, create_data_loaders

def main():
    # Set the number of clients you want to simulate
    num_clients = 2

    # Load the full MNIST training dataset
    print("Loading MNIST training dataset...")
    dataset = load_mnist_dataset(train=True)
    total_size = len(dataset)
    print(f"Total dataset size: {total_size}")

    # Partition the dataset into subsets for each client (IID partitioning)
    print(f"Partitioning dataset into {num_clients} subsets...")
    subsets = partition_dataset(dataset, num_clients)
    for i, subset in enumerate(subsets):
        print(f"Client {i} partition size: {len(subset)}")

    # Create DataLoaders for each partition
    print("Creating DataLoaders for each partition...")
    data_loaders = create_data_loaders(subsets, batch_size=32)
    for i, loader in enumerate(data_loaders):
        num_batches = len(loader)
        print(f"Client {i} DataLoader has {num_batches} batches.")

if __name__ == "__main__":
    main()
