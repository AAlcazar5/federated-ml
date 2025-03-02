# backend/utils/federated-server.py

import argparse
import fedml

def main():
    parser = argparse.ArgumentParser(description="Run FedML Federated Server")
    # Set role to server. In FedML, the same runner is used for both roles.
    parser.add_argument("--role", type=str, default="server", help="Role: server")
    parser.add_argument("--num_rounds", type=int, default=100, help="Number of federated learning rounds")
    parser.add_argument("--num_clients", type=int, default=2, help="Number of expected clients")
    # You can add more server-specific arguments as needed.
    args = parser.parse_args()

    # FedML uses the same run() function to launch both server and client.
    # When args.role is 'server', it will run in server mode.
    fedml.run(args)

if __name__ == "__main__":
    main()
