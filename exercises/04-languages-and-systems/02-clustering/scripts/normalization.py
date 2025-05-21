import argparse
import os
from pathlib import Path

import numpy as np
from sklearn import preprocessing


def normalize(matrix: np.ndarray, normalize_t: str) -> np.ndarray:
    if normalize_t == "none":
        normalized = matrix
    elif normalize_t == "ln_p1":
        normalized = np.log1p(matrix)
    elif normalize_t == "tanh":
        normalized = np.tanh(matrix)
    elif normalize_t == "ln_pe":
        pseudo_count = 1e-6
        normalized = np.log(matrix + pseudo_count)
    elif normalize_t == "minmax":
        min_max_scaler = preprocessing.MinMaxScaler()
        normalized = min_max_scaler.fit_transform(matrix)
    else:
        raise NotImplementedError(
            f"{normalize_t} is not a valid normalization technique"
        )
    return normalized


def main(args: argparse.Namespace) -> None:
    if not os.path.exists(args.matrix):
        raise FileNotFoundError(f"{args.matrix} does not exist")

    # Set seed for reproducibility
    np.random.seed(args.seed)

    data = np.load(args.matrix)
    normalized_data = normalize(data, args.technique)
    np.save(args.outname, normalized_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("matrix", help="Path to the matrix file (.csv)", type=str)
    parser.add_argument(
        "technique", help="Technique of normalization to apply", type=str
    )
    parser.add_argument(
        "--outname", help="Output name", type=str, default="normalized.npy"
    )
    parser.add_argument("--seed", help="Random seed", type=int, default=42)
    main(parser.parse_args())
