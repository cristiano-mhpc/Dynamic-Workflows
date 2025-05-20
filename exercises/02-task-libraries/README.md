# Dask exercise

In this exercise, the students will apply various clustering techniques to a dataset, experimenting with different combinations of normalization and dimensionality reduction (including the option to skip either or both). The overall workflow consists of four main steps:

- Download the dataset
- Normalization (or no normalization)
- Dimensionality Reduction (or no reduction)
- Clustering

## Material
Python scripts are provided for each of these steps:

The `download.py` script contains the `download_data` function, which downloads a dataset by name from the [KaggleHub](https://www.kaggle.com/datasets) repositories.

The `normalization.py` script contains the `normalize` function, which allows the application of one of the following normalization techniques:

- `none`: No normalization is applied.
- `ln_p1`: Natural logarithm of one plus the input array.
- `ln_pe`: Natural logarithm of an epsilon plus the input array.
- `tanh`: Hyperbolic tangent applied element-wise.
- `minmax`: Rescaling the values in the range 0-1.

The `reduction.py` script contains the `reduce` function, which takes as input the target number of dimensions for reduction and supports the following dimensionality reduction techniques:

- `none`: No reduction is applied.
- `pca`: Principal Component Analysis.
- `tsne`: t-SNE (t-distributed Stochastic Neighbor Embedding).
- `isomap`: Isomap.
- `mds`: Multidimensional Scaling.

The `clusterization.py` script contains the `clustering` function, which computes the desired clustering based on the provided input. The quality of the resulting clusters is then evaluated by calculating a corresponding score (default: silhouette). The available clustering techniques are:

- `dbscan`: DBSCAN (Density-Based Spatial Clustering of Applications with Noise).
- `k-means`: K-means clustering.

Finally, `dask_application.py` is the main script. It uses Dask to execute the workflow by leveraging the functions defined in the other files.

## Execute the script

A virtual environment must be created and activated to execute the code:

```bash
python -m venv venv
source venv/bin/activate
```

Required packages can be installed with the following command:

```bash
pip install -r requirements.txt
```

Finally, execute the main script with the appropriate inputs

```bash
python dask_application.py config.yml
```

The script returns a plot of the cluster with the highest silhouette score.

Execution can be customized by modifying the `config.yml` file. It must include the following inputs:
- `dataset_name`: Name of the dataset repository to download from KaggleHub.
- `clustering_techniques`: A list of clustering techniques to be used.
- `normalization_techniques`: A list of normalization techniques to be applied.
- `reduction_techniques`: A list of dimensionality reduction techniques to be applied.
- `number_dimensions`: The target number of dimensions after reduction.
- `seed`: The random seed to ensure reproducibility of the experiments.

## Exercise

The current code contains several errors and inefficiencies. The student's goal is to produce an execution that uses the values provided in the config file and matches the expected output, while also improving the performance of the workflow.

Proper use of Dask is required, following [best practices](https://docs.dask.org/en/stable/delayed-best-practices.html). This includes designing parallel tasks with a balanced workload and minimizing redundant computation, specifically, avoiding repeated execution of the same code.

There are two known issues in the code: one affects the reproducibility of the experiments, and the other alters the input data. It is also recommended to review other scripts (e.g., normalization.py) to help identify and resolve these problems.

Run the following commands to verify the correctness of the output:

```bash
./check_output.sh
```
