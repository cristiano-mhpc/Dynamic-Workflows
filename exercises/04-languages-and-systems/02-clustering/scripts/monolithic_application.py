import argparse

import yaml
from clusterization import clustering
from download import download_data
from normalization import normalize
from reduction import reduce


def read_yaml_file(file_path):
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    return data


def main(args):
    arguments = read_yaml_file(args.config_file)
    dataset_name = arguments["dataset_name"]
    norm_techniques = arguments["normalization_techniques"]
    reduction_techniques = arguments["reduction_techniques"]
    num_dimensions = arguments["number_dimensions"]
    clustering_techniques = arguments["clustering_techniques"]
    seed = arguments["seed"]

    # Download the dataset
    data = download_data(dataset_name)

    for norm_technique in norm_techniques:
        # Normalize values
        normalized = normalize(data, norm_technique)

        for red_technique in reduction_techniques:
            # Reduce the dimensions
            reduced = reduce(normalized, num_dimensions, red_technique, seed)

            for clustering_technique in clustering_techniques:
                # Clustering the data
                clustering(
                    reduced,
                    clustering_technique,
                    seed,
                    f"{norm_technique}_{red_technique}_{clustering_technique}",
                )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file", help="Path of config name", type=str)
    main(parser.parse_args())
