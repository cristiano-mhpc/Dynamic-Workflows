import argparse
import os

import kagglehub
import numpy as np
import pandas as pd


def download_data(dataset_name):
    path = kagglehub.dataset_download(dataset_name)
    csv_files = [f for f in os.listdir(path) if f.lower().endswith(".csv")]
    if not csv_files:
        raise FileNotFoundError("No CSV file found in the dataset directory.")
    csv_path = os.path.join(path, csv_files[0])
    df = pd.read_csv(csv_path)
    data = df.select_dtypes(include="number").values
    return np.array(data)


def main(args):
    data = download_data(args.dataset_name)
    np.save(args.outname, data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset_name", help="Dataset name", type=str)
    parser.add_argument("outname", help="Output name", type=str)
    main(parser.parse_args())
