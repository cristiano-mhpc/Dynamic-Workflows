"""Simple FL script simulating FedAvg"""
# This script:
#     - Instantiates the server anf the client
#     - prepares the dataset with either IID 
#     or one-class-per client partitioning
#     based on the --one-class argument
#     - run local training and testing for each client
#     - run server model aggregation and upfating the model

import argparse
import sys
from typing import List
import torch

from common.models.simple_model import Net
from common.parser import parser
from common.utils import load_mnist, set_deterministic_execution

# Import client and server classes
from common.client.fed_avg_client import FedAvgClient
from common.server.fed_avg_server import FedAvgServer

def training(args: argparse.Namespace) -> None:
    """FedAvg training script

    :param args: Command-line arguments
    :type args: argparse.Namespace
    """

    # Select device
    device = torch.device("cuda" if args.gpu and torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Reporoducibility
    generator = None
    if args.seed is not None:
        generator = set_deterministic_execution(args.seed)

    print("Creating server...")

    # Instantiate server
    server = FedAvgServer(Net(), device=device)

    clients: List = []
    for i in range(args.clients):
        print(f"Creating client {i}...")
        # Instantiate clients
        train_loader, test_loader = load_mnist(
            batch_size=args.batch_size,
            one_class=args.one_class,
            id=i if args.one_class else None,
            generator=generator,
        )
        client_model = Net()
        client = FedAvgClient(
            client_id=i,
            model=server.get_model(),
            train_loader=train_loader,
            test_loader=test_loader,
            lr=args.learning_rate,
            device=device,
        )
        clients.append(client)    

    for i in range(args.rounds):
        print(f"Starting round {i}...")
        for id, client in enumerate(clients):
            print(f"Client {id} training...")
            # Client training
            train_loss = client.train(args.epochs)
            print(f"Client {id} finished training with loss: {train_loss:.4f}")

            print(f"Client {id} testing...")
            # Client testing
            test_loss = client.test()
            print(f"Client {id} finished testing with loss: {test_loss[0]:.4f}, accuracy: {test_loss[1]:.2f}%")
        print(f"Averaging clients' models...")
        # Clients' models averaging
        client_params = [client.get_parameters() for client in clients]
        server.average(client_params)
        for id, client in enumerate(clients):
            print(f"Sending model to client {id}...")
            # Setting aggregated model in clients
            client.set_model(server.get_model())
            
def main() -> None:
    """Argument parsing and training launch"""
    training(args=parser.parse_args(sys.argv[1:]))

if __name__ == "__main__":
    main()
