class: Workflow
cwlVersion: v1.2

requirements:
  InlineJavascriptRequirement: {}
  MultipleInputFeatureRequirement: {}
  ScatterFeatureRequirement: {}
  StepInputExpressionRequirement: {}
  SubworkflowFeatureRequirement: {}

inputs:
  # TODO: complete

outputs:
   plot:
     type: File
     outputSource: clustering/plot
   score:
     type:
       type: record
       fields:
         score:
           type: float
         label:
           type: string
     outputSource: clustering/score

steps:
  normalizing:
    # TODO: complete

  reducing:
    # TODO: complete

  clustering:
    out: [ model, plot, score ]
    # TODO: complete