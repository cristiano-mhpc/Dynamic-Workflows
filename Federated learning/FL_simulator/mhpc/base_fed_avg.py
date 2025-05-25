"""Simple FL script simulating FedAvg"""
# This script:
#     - Instantiates the server and the client
#     - prepares the dataset with either IID 
#     or one-class-per client partitioning
#     based on the --one-class argument
#     - run local training and testing for each client
#     - run server model aggregation and upfating the model

import argparse
import sys
from typing import List
import torch

import dask
from dask import delayed, compute
from dask.distributed import Client

from common.models.simple_model import Net
from common.parser import parser
from common.utils import load_mnist, set_deterministic_execution

# Import client and server classes
from common.client.fed_avg_client import FedAvgClient
from common.server.fed_avg_server import FedAvgServer

@delayed
def train_client(client, epochs):
    """Parallel training of a clients"""
    print(f"Training client {client.client_id} for {epochs} epochs...")
    train_loss = client.train(epochs)
    params = client.get_parameters()
    return train_loss, params

@delayed
def test_client(client):
    """Parallel testing of a clients"""
    print(f"Testing client {client.client_id}...")
    return client.test() 

def training(args: argparse.Namespace) -> None:
    """FedAvg training script

    :param args: Command-line arguments
    :type args: argparse.Namespace
    """
    # Launch local Dask cluster (dashboard at localhost:8787)
    dask_client = Client()
    print(f"Dask dashboard available at: {dask_client.dashboard_link}")

    # Select device
    device = torch.device("cuda" if args.gpu and torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Reproducibility
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
        if args.sequential:
             # Sequential training
            print("Training and testing the models sequentially from one client to the next...")
            for id, client in enumerate(clients):
                print(f"Client {id} training...")
                # Client training
                train_loss = client.train(args.epochs)
                print(f"Client {id} finished training with loss: {train_loss:.4f}")

                print(f"Client {id} testing...")
                # Client testing
                test_loss = client.test()
                print(f"Client {id} finished testing with loss: {test_loss[0]:.4f}, accuracy: {test_loss[1]:.2f}%")
            
            # Clients' models averaging
            client_params = [client.get_parameters() for client in clients]
        else: 
            # Parallel training
            print("Training and testing the models in parallel...")
            train_tasks = [train_client(client, args.epochs) for client in clients]
            train_results = compute(*train_tasks) # execute in parallel

            # unpack training results
            train_losses, client_params = zip(*train_results)
            for i, loss in enumerate(train_losses):
                print(f"Client {i} training loss: {loss:.4f}")
            
            # Parallel testing
            test_tasks = [test_client(client) for client in clients]
            test_results = compute(*test_tasks)

            for i, (loss, acc) in enumerate(test_results):
                 print(f"Client {i} test loss: {loss:.4f}, accuracy: {acc:.2%}")

            all_tasks = train_tasks + test_tasks
            #Visualize the Dask task graph
            dask.visualize(all_tasks, filename="train_test_graph", engine="graphviz", format="png")

            print(f"Averaging clients' models...")

        # Average clients' models
        server.average(client_params)
        # Sending aggregated model to clients
        for id, client in enumerate(clients):
            print(f"Sending model to client {id}...")
            # Setting aggregated model in clients
            client.set_model(server.get_model())
            
def main() -> None:
    """Argument parsing and training launch"""
    training(args=parser.parse_args(sys.argv[1:]))

if __name__ == "__main__":
    main()
