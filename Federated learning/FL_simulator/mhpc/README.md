
# Parallelization Strategy in the Federated Learning Script using Dask


## Goals of Parallelization

The key goals of using parallelization in this script are to:
- Speed up local training and testing across multiple clients
- Utilize available CPU cores (or workers) efficiently
- Enable scalable simulation of federated learning rounds

## Why Dask?

Dask provides:
- Simple parallelization using Python syntax
- Dynamic task scheduling
- A dashboard (`localhost:8787`) for real-time monitoring
- Compatibility with `delayed` execution and `compute()`

## Components Parallelized

### 1. Client Training

```python
@delayed
def train_client(client, epochs):
    ...
    return train_loss, params
```

Each client's training is wrapped in a `@delayed` function, allowing Dask to build a task graph for concurrent execution.

### 2. Client Testing

```python
@delayed
def test_client(client):
    ...
    return client.test()
```

Testing is similarly delayed and executed in parallel.

### 3. Task Submission and Execution

```python
train_tasks = [train_client(client, args.epochs) for client in clients]
train_results = compute(*train_tasks)
```

- All client training tasks are submitted to the Dask scheduler.
- `compute(*train_tasks)` triggers execution and waits for all to complete.

The same pattern is used for testing with `test_tasks`.

### 4. Visualization of Task Graph

```python
dask.visualize(all_tasks, filename="train_test_graph", engine="graphviz", format="png")
```

This generates a visual representation of the parallel workflow, helping to analyze dependencies and performance.

## Control Over Sequential vs. Parallel

The script allows toggling between sequential and parallel execution via the `--sequential` argument:

- **Sequential Mode:** Executes client training/testing in a loop.
- **Parallel Mode:** Uses Dask to train/test clients concurrently.

## Summary of Benefits

- **Time Efficiency:** Speeds up FL rounds significantly for large numbers of clients.
- **Clarity:** Clear separation between task definition and execution.
- **Debuggability:** Dask dashboard aids in visual monitoring and debugging.

## Potential Improvements

- Use distributed Dask clusters for scaling beyond a single machine.
- Monitor memory and CPU usage with Dask diagnostics.
- Implement fault-tolerant client execution.

---

*Author: [Your Name]*  
*Date: 2025*
