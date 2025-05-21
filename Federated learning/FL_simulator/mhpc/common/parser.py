"""Command line argument parser for the xFFL-LLM example"""

from argparse import ArgumentParser

### Argument parser
parser = ArgumentParser(
    prog="Master in HPC - Federated Learning example",
    description="This example trains an ML model trough FL.",
)

parser.add_argument("-gpu", "--gpu", help="Use the available GPUs", action="store_true")

parser.add_argument(
    "-one",
    "--one-class",
    help="Load just one MNIST class per client",
    action="store_true",
)

parser.add_argument(
    "-c",
    "--clients",
    help="Number of clients in the federation.",
    type=int,
    default=0,
)

parser.add_argument(
    "-e",
    "--epochs",
    help="Number of training epochs",
    type=int,
    default=1,
)

parser.add_argument(
    "-r",
    "--rounds",
    help="Number of federated rounds to run",
    type=int,
    default=1,
)

parser.add_argument(
    "-bs",
    "--batch-size",
    help="Training batch size",
    type=int,
    default=4,
)

parser.add_argument(
    "-name",
    "--wandb-name",
    help="WandB group name",
    type=str,
    default="LLaMA-3.1 8B",
)

parser.add_argument(
    "-mode",
    "--wandb-mode",
    help="WandB mode",
    type=str,
    default="disabled",
    choices=["online", "offline", "disabled"],
)

parser.add_argument(
    "-s",
    "--seed",
    help="Random execution seed (for reproducibility purposes)",
    type=int,
    default=None,
)

parser.add_argument(
    "-lr",
    "--learning-rate",
    help="Learning rate",
    type=float,
    default=1.0,
)

parser.add_argument(
    "-g",
    "--gamma",
    help="Learning rate scheduler gamma",
    type=float,
    default=0.7,
)
