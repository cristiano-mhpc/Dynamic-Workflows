import argparse
import json
import os
import pickle

import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import DBSCAN, KMeans
from sklearn.metrics import davies_bouldin_score, silhouette_score
from sklearn.neighbors import NearestNeighbors


def plot(X: np.ndarray, labels: np.ndarray, clustering_technique: str, outname: str):
    plt.scatter(X[:, 0], X[:, 1], c=labels, s=50, cmap="viridis")
    plt.title(f"{clustering_technique} Clustering Example")
    plt.savefig(f"plot_{outname}.png")
    # plt.show()


def k_distance(X: np.ndarray, k: int):
    neighbors = NearestNeighbors(n_neighbors=k)
    neighbors.fit(X)
    distances, _ = neighbors.kneighbors(X)
    # Take the farthest neighbor
    distances = np.sort(distances[:, -1], axis=0)
    # Find the elbow point where the increase begins
    diffs = np.diff(distances)
    second_diffs = np.diff(diffs)
    elbow_index = np.argmax(second_diffs) + 1
    return distances[elbow_index]


def get_score(score_metric: str, n_clusters: int, X: np.ndarray, labels: np.ndarray):
    if n_clusters > 1:
        if score_metric == "silhouette":
            score = silhouette_score(X, labels)
        elif score_metric == "davies_bouldin":
            score = davies_bouldin_score(X, labels)
        else:
            raise ValueError("Unknown score metric: {score_metric}")
    else:
        score = -1
    return score


def dbscan(X: np.ndarray, score_metric: str, seed: int):
    min_samples_values = [2, 3, 4, 5]
    best_score = None
    best_model = None

    for min_samples in min_samples_values:
        max_eps = k_distance(X, k=min_samples)
        min_eps = 1
        eps_values_len = 10
        eps_values = np.arange(min_eps, max_eps, (max_eps - min_eps) / eps_values_len)
        for eps in eps_values:
            model = DBSCAN(eps=eps, min_samples=min_samples)
            labels = model.fit_predict(X)

            n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
            score = get_score(score_metric, n_clusters, X, labels)
            if best_score is None or score > best_score:
                best_score = score
                best_model = model

    labels = best_model.fit_predict(X)
    return best_model, labels, len(set(labels)) - (1 if -1 in labels else 0), best_score


def kmeans(X: np.ndarray, score_metric: str, seed: int):
    best_score = None
    best_model = None
    for n_clusters in range(2, 11):
        model = KMeans(n_clusters=n_clusters, random_state=seed)
        model.fit(X)
        labels = model.fit_predict(X)

        score = get_score(score_metric, n_clusters, X, labels)
        if best_score is None or score > best_score:
            best_score = score
            best_model = model
    return best_model, best_model.fit_predict(X), best_model.n_clusters, best_score


def clustering(
    data: np.ndarray,
    clustering_technique: str,
    seed: int,
    outname: str,
    score_metric: str = "silhouette",
    create_plot: bool = False,
):
    if clustering_technique == "dbscan":
        model, labels, n_clusters, score = dbscan(data, score_metric, seed)
    elif clustering_technique == "kmeans":
        model, labels, n_clusters, score = kmeans(data, score_metric, seed)
    else:
        raise NotImplementedError(
            f"{clustering_technique} is not a valid clustering technique"
        )
    if create_plot:
        plot(data, labels, clustering_technique, outname)
    return model, outname, n_clusters, score, data


def main(args):
    if not os.path.exists(args.data):
        raise FileNotFoundError(f"{args.data} does not exist")
    np.random.seed(args.seed)

    data = np.load(args.data)
    model, outname, n_clusters, score, _ = clustering(
        data, args.clustering_technique, args.seed, args.outname
    )
    print(
        json.dumps(
            {"outname": outname, "n_clusters": n_clusters, "score": float(score)}
        )
    )
    with open(f"{args.outname}.pkl", "wb") as fd:
        pickle.dump(model, fd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", help="Dataset name", type=str)
    parser.add_argument(
        "--clustering_technique", help="Clustering technique to use", type=str
    )
    parser.add_argument("--outname", help="Output name", type=str)
    parser.add_argument("--seed", help="Seed", type=str)
    parser.add_argument("--plot", help="Create plots", action="store_true")
    main(parser.parse_args())
