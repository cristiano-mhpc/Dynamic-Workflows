import argparse
import json
import time
from typing import MutableSequence

import dask
import numpy as np
import yaml

from clusterization import clustering, plot
from download import download_data
from normalization import normalize
from reduction import reduce


def read_yaml_file(file_path):
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    return data


def pipeline(
    dataset_name: str,
    norm_techniques: MutableSequence[str],
    reduction_techniques: MutableSequence[str],
    clustering_techniques: MutableSequence[str],
    num_dimensions: int,
    seed: int,
):
    results = []
    # Download the dataset
    data = download_data(dataset_name)
    for norm_technique in norm_techniques:
        for red_technique in reduction_techniques:
            for clustering_technique in clustering_techniques:
                # Normalize values
                normalized = normalize(data, norm_technique)
                # Reduce the dimensions
                reduced = reduce(normalized, num_dimensions, red_technique, seed)
                # Clustering the data
                result = clustering(
                    reduced,
                    clustering_technique,
                    seed,
                    f"{norm_technique}_{red_technique}_{clustering_technique}",
                )
                results.append(result)
    return results


def main(args):
    arguments = read_yaml_file(args.config_file)
    dataset_name = arguments["dataset_name"]
    norm_techniques = arguments["normalization_techniques"]
    reduction_techniques = arguments["reduction_techniques"]
    num_dimensions = arguments["number_dimensions"]
    clustering_techniques = arguments["clustering_techniques"]
    #seed = int(time.time()) # MARK changed
    seed = arguments["seed"]

    # Set seed for reproducibility
    np.random.seed(seed)

    # Execute the workflow.
    # Currently, the pipeline is not parallelized.
    task = dask.delayed(pipeline)(
        dataset_name=dataset_name,
        norm_techniques=norm_techniques,
        reduction_techniques=reduction_techniques,
        clustering_techniques=clustering_techniques,
        num_dimensions=num_dimensions,
        seed=seed,
    )

    task.visualize(bad.svg)
    # Execute dask tasks
    results = task.compute()
    # Print values
    results = sorted(results, key=lambda x: x[3])
    for _, outname, n_clusters, score, _ in results:
        print(
            json.dumps(
                {"outname": outname, "n_clusters": n_clusters, "score": float(score)}
            )
        )
    # Plot best cluster
    model, outname, n_clusters, score, data = results[-1]
    plot(data, model.fit_predict(data), outname.split("_")[-1], outname)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file", help="Path of config name", type=str)
    main(parser.parse_args())
