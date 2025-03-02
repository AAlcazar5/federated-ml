# backend/federated.py

import multiprocessing as mp
import subprocess
import time

def run_server():
    """
    Runs the FedML server.
    Assumes that 'utils/federated-server.py' accepts command-line arguments,
    for example: --num_rounds and --num_clients.
    """
    cmd = [
        "python",
        "utils/federated-server.py",
        "--num_rounds", "100",
        "--num_clients", "2"
    ]
    subprocess.run(cmd, check=True)

def run_client(client_id: int):
    """
    Runs a FedML client.
    Assumes that 'utils/federated-client.py' accepts command-line arguments,
    such as --client_id and --server_address.
    """
    cmd = [
        "python",
        "utils/federated-client.py",
        "--client_id", str(client_id),
        "--server_address", "127.0.0.1:5000"  # Adjust as needed; ensure it matches server settings.
    ]
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    processes = []

    # Start the server process.
    server_proc = mp.Process(target=run_server)
    server_proc.start()
    processes.append(server_proc)
    print("Server started...")

    # Allow some time for the server to start up.
    time.sleep(5)

    # Start client processes.
    num_clients = 2  # Adjust the number of clients as needed.
    for client_id in range(num_clients):
        p = mp.Process(target=run_client, args=(client_id,))
        p.start()
        processes.append(p)
        print(f"Client {client_id} started...")

    # Wait for all processes to complete.
    for p in processes:
        p.join()

    print("Federated learning simulation finished.")
