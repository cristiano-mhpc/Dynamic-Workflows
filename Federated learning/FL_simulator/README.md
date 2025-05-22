### Federated Learning (FL) Simulator Skeleton

This repository provides a minimal sequential Python framework for building a Federated Learning (FL) simulator for the exam of the "Hybrid workflows for Federated AI" course.

**Exam instructions**

Students are expected to implement:
* The abstract classes found in `base_client.py` (a working FL client) **[max 7 pt.]**
  * The training can be implemented with any model or data desired; a draft model and dataset (MNIST) are already present in the repo.
  * Additional model, data, or data splitting support will be evaluated with higher grades.   
* The abstract classes found in `base_server.py` (a working FL server with correct aggregation) **[max 7 pt.]**
  * Please double check that the aggregation function returns correct models; non-correctly working aggregation methods will be evaluated with less points.
  * More complex aggregation strategies will be evaluated more; the bare minimum requirement is a simple average.
* The `base_fed_avg.py` script (draft script implementing the FedAvg algorithm) **[max 5 pt.]**
* Optimnize the FL simulator using a task-based programming approach **[max 7 pt.]**
  * You can use any task-based programming library you prefer;
  * A more efficient parallelization strategy will be evaluated more.
  * Please provide a pictorial representation of the resulting task graph along with a step by step description of the design process. You can either generate it from the library (``dask.visualize``) or draw it manually (e.g., using [draw.io](https://draw.io))
* Decompose the application into sub-programs that communicate through a file-based data transport strategy and orchestrate the execution through a high-level workflow system (Nextflow or CWL). **[max 9 pt.]**
  * To save a DNN model to a file and load it in PyTorch you can use ``torch.save()`` and ``torch.load()``, respectively.

Please provide a README file justifying your implementation choices.

Students can work in groups of 2 people at maximum. Group projects will be evaluated more severely than single-person projects.
The maximum score achievable is 35 pt., while the lowest is 0. Scores higher than 30 will be considered as 30L.
