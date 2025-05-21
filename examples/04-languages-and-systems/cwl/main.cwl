cwlVersion: v1.2
class: Workflow
requirements:
 ScatterFeatureRequirement: {}
inputs:
  str:
    type: string
    default: 'Hello World!'
outputs:
  split:
    type: File[]
    outputSource: split/out
  upper:
    type: File[]
    outputSource: upper/out
steps:
  split:
    run: clt/split.cwl
    in:
      str: str
    out: [out]
  upper:
    run: clt/upper.cwl
    in:
      chunk: split/out
    scatter: chunk
    out: [out]
