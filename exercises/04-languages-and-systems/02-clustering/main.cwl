class: Workflow
cwlVersion: v1.2

inputs:
  download_script: File
  dataset_name: string

  reduction_script: File
  reduction_techniques: string[]
  number_dimensions: int

  normalization_script: File
  normalization_techniques: string[]

  clustering_script: File
  clustering_techniques: string[]

  seed: int

outputs:
  scores:
    type:
      type: array
      items:
        type: record
        fields:
          score:
            type: float
          label:
            type: string
    outputSource: cluster/score
  best_cluster:
    type: File
    outputSource: choose_higher_score/plot

steps:
  # Step: call the step in `clt/download.cwl`
  download:
    in:    # TODO: complete
    out:   # TODO: complete
    run:   # TODO: complete

  # Step: call the sub-workflow `clustering_pipeline` and execute the scatter on the normalization.
  cluster:
    in:        # TODO: complete
    out: [ plot, score ]
    scatter:   # TODO: complete
    scatterMethod: # TODO: complete
    run: clustering_pipeline.cwl

  choose_higher_score:
    in:
      scores: cluster/score
      plots: cluster/plot
    out: [ score, plot ]
    run: et/choose_higher_score.cwl