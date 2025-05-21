class: ExpressionTool
cwlVersion: v1.2

requirements:
  InlineJavascriptRequirement: {}

inputs:
  plots:
    type: File[]
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

outputs:
  plot:
    type: File
  score:
    type:
      type: record
      fields:
        score:
          type: float
        label:
          type: string

expression: >
  ${
    if (inputs.scores.length === 0 || inputs.scores.length != inputs.plots.length) {
      return null;
    }

    var maxIndex = 0;
    for (var i = 1; i < inputs.scores.length; i++) {
      if (inputs.scores[i].score > inputs.scores[maxIndex].score) {
        maxIndex = i;
      }
    }
    return {
      "plot": inputs.plots[maxIndex],
      "score": inputs.scores[maxIndex]
    };
  }
