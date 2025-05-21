class: CommandLineTool
cwlVersion: v1.2

requirements:
  InlineJavascriptRequirement: {}

baseCommand: [ "python" ]

arguments:
  - position: 6
    prefix: --outname
    valueFrom: "$(inputs.normalization_technique)_$(inputs.reduction_technique)_$(inputs.clustering_technique)"
  - position: 7
    valueFrom: --plot

inputs:
  script:
    type: File
    inputBinding:
      position: 1
  data:
    type: File
    inputBinding:
      position: 2
      prefix: --data
  clustering_technique:
    type: string
    inputBinding:
      position: 3
      prefix: --clustering_technique
  normalization_technique:
    type: string
  reduction_technique:
    type: string

stdout: "output.json"
stderr: "output.err"

outputs:
  model:
    type: File
    outputBinding:
      glob: "*.pkl"
  plot:
    type: File
    outputBinding:
      glob: "*.png"
  score:
    type:
      type: record
      fields:
        score:
          type: float
          outputBinding:
            loadContents: true
            glob: "output.json"
            outputEval: $(JSON.parse(self[0].contents).score)
        label:
          type: string
          outputBinding:
            loadContents: true
            glob: "output.json"
            outputEval: $(JSON.parse(self[0].contents).outname)