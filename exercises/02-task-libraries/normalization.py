import argparse
import os
from pathlib import Path

import numpy as np
from sklearn import preprocessing


def normalize(matrix: np.ndarray, normalize_t: str) -> np.ndarray:
    if normalize_t == "none":
        return matrix
    elif normalize_t == "ln_p1":
        # In-place normalization
        np.log1p(matrix, out=matrix)
        return matrix
    elif normalize_t == "tanh":
        # In-place normalization
        np.tanh(matrix, out=matrix)
        return matrix
    elif normalize_t == "ln_pe":
        pseudo_count = 1e-6
        normalized = np.log(matrix + pseudo_count)
        return normalized
    elif normalize_t == "minmax":
        min_max_scaler = preprocessing.MinMaxScaler()
        return min_max_scaler.fit_transform(matrix)
    else:
        raise NotImplementedError(
            f"{normalize_t} is not a valid normalization technique"
        )


def main(args: argparse.Namespace) -> None:
    if not os.path.exists(args.matrix):
        raise FileNotFoundError(f"{args.matrix} does not exist")

    data = np.load(args.matrix)
    normalized_data = normalize(data, args.technique)

    if args.outname:
        output_name = args.outname
    else:
        output_name = Path(args.matrix).stem
    np.save(output_name, normalized_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("matrix", help="Path to the matrix file (.csv)", type=str)
    parser.add_argument(
        "technique", help="Technique of normalization to apply", type=str
    )
    parser.add_argument("outname", help="Output name", type=str)
    main(parser.parse_args())
