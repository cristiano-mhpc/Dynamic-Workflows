"""Simple FL script simulating FedAvg"""

import argparse
import sys
from typing import List

from common.models.simple_model import Net
from common.parser import parser

# Import client and server classes


def training(args: argparse.Namespace) -> None:
    """FedAvg training script

    :param args: Command-line arguments
    :type args: argparse.Namespace
    """

    print("Creating server...")
    # Instantiate server

    clients: List = [None for _ in range(args.clients)]
    for i in range(args.clients):
        print(f"Creating client {i}...")
        # Instantiate clients

    for i in range(args.rounds):
        print(f"Starting round {i}...")

        for id, client in enumerate(clients):
            print(f"Client {id} training...")
            # Client training
            print(f"Client {id} testing...")
            # Client testing

        print(f"Averaging clients' models...")
        # Clients' models averaging

        for id, client in enumerate(clients):
            print(f"Sending model to client {id}...")
            # Setting aggregated model in clients


def main() -> None:
    """Argument parsing and training launch"""
    training(args=parser.parse_args(sys.argv[1:]))


if __name__ == "__main__":
    main()
