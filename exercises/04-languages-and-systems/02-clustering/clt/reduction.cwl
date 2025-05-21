class: CommandLineTool
cwlVersion: v1.2

requirements:
  InlineJavascriptRequirement: {}

baseCommand: [ "python" ]

inputs:
  script:
    type: File
    inputBinding:
      position: 1
  dataset:
    type: File
    inputBinding:
      position: 2
      prefix: --matrix
  technique:
    type: string
    inputBinding:
      position: 3
      prefix: --technique
  number_dimensions:
    type: int
    inputBinding:
      position: 4
      prefix: --num-dim
  seed:
    type: int
    inputBinding:
      position: 5
      prefix: --seed
  outname:
    type: string?
    inputBinding:
      position: 6
      prefix: --outname
    default: "reduced"

outputs:
  reduced:
    type: File
    outputBinding:
      glob: "$(inputs.outname).npy"