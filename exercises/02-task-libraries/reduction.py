import argparse
import os
from pathlib import Path

import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import MDS, TSNE, Isomap


def reduce(matrix: np.ndarray, num_dim: int, reduction_t: str, seed: int) -> np.ndarray:
    if reduction_t == "none":
        return matrix
    elif reduction_t == "pca":
        rd_model = PCA(n_components=num_dim)
    elif reduction_t == "tsne":
        rd_model = TSNE(n_components=num_dim, random_state=seed)
    elif reduction_t == "isomap":
        rd_model = Isomap(n_components=num_dim)
    elif reduction_t == "mds":
        rd_model = MDS(n_components=num_dim)
    else:
        raise NotImplementedError(f"{reduction_t} is not a valid reduction technique")
    reduced_embeddings = rd_model.fit_transform(matrix)
    return reduced_embeddings


def main(args: argparse.Namespace) -> None:
    if not os.path.exists(args.matrix):
        raise FileNotFoundError(f"{args.matrix} does not exist")

    data = np.load(args.matrix)
    reduced_data = reduce(data, args.num_dim, args.technique, args.seed)

    if args.outname:
        output_name = args.outname
    else:
        output_name = Path(args.matrix).stem
    np.save(output_name, reduced_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--matrix", help="Path to the matrix file (.csv)", type=str, required=True
    )
    parser.add_argument(
        "--num-dim", help="Technique of normalization to apply", type=str, required=True
    )
    parser.add_argument(
        "--technique",
        help="Technique of normalization to apply",
        type=str,
        required=True,
    )
    parser.add_argument("--outname", help="Output name", type=str, default=None)
    parser.add_argument("--seed", help="Seed", type=int, default=42)
    main(parser.parse_args())
