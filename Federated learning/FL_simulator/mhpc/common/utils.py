"""Utility methods class"""

import os
import random
from typing import Optional, Tuple

import numpy
import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms


def load_mnist(
    batch_size: int,
    one_class: bool = False,
    id: Optional[int] = None,
    generator: Optional[torch.Generator] = None,
) -> Tuple[DataLoader, DataLoader]:
    """Load the MNIST dataset

    :param batch_size: Batch size
    :type batch_size: int
    :return: Training and testing dataloaders
    :rtype: Tuple[DataLoader, DataLoader]
    """
    transform = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
    )
    trainset = datasets.MNIST("../data", train=True, download=True, transform=transform)
    testset = datasets.MNIST("../data", train=False, transform=transform)

    if one_class:
        trainset.data = trainset.data[trainset.targets == id]
        trainset.targets = trainset.targets[trainset.targets == id]
        testset.data = testset.data[testset.targets == id]
        testset.targets = testset.targets[testset.targets == id]

    train_loader = torch.utils.data.DataLoader(
        trainset,
        batch_size=batch_size,
        worker_init_fn=(
            seed_dataloader_worker if generator is not None else None
        ),  # Necessary for reproducibility
        generator=generator,
    )  # Necessary for reproducibility
    test_loader = torch.utils.data.DataLoader(
        testset,
        batch_size=batch_size,
        worker_init_fn=(
            seed_dataloader_worker if generator is not None else None
        ),  # Necessary for reproducibility
        generator=generator,
    )  # Necessary for reproducibility

    return train_loader, test_loader


def seed_dataloader_worker(worker_id: int) -> None:
    """Seeds PyTorch's data loader workers to guarantee reproducibility

    Since each data loader worker is a process, the underlying libraries have to be re-seeded in a reproducible way to guarantee reproducibility of the loaded data and that different workers do not have the same seed, thus loading the same data

    :param worker_id: Worker's id
    :type worker_id: int
    """
    worker_seed = (
        torch.initial_seed() % 2**32
    )  # Get PyTorch generated seed for the worker (base_seed + worker_id) and reduce it into a valid range
    random.seed(worker_seed)
    numpy.random.seed(worker_seed)


def set_deterministic_execution(seed: int) -> torch.Generator:
    """Set all the necessary RNGs to obtain reproducible executions

    This method sets random, numpy, torch and CUDA RNGs with the same seed.
    It also forces PyTorch's to use deterministic algorithms, reducing performance

    :param seed: Random seed
    :type seed: int
    :return: PyTorch RNG
    :rtype: torch.Generator
    """
    random.seed(seed)
    # numpy.random.seed(seed)
    generator = torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

    torch.utils.deterministic.fill_uninitialized_memory = (
        True  # This should be True by default
    )
    torch.use_deterministic_algorithms(mode=True)

    os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"  # Check cuBLAS version

    return generator
