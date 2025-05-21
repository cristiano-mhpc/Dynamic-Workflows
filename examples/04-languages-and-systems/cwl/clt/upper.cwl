cwlVersion: v1.2
class: CommandLineTool
requirements:
  InitialWorkDirRequirement:
    listing:
      - entry: cat $(inputs.chunk.path) | tr '[a-z]' '[A-Z]'
        entryname: script.sh
inputs:
  chunk:
    type: File
baseCommand: [sh, script.sh]
outputs:
  out: stdout
stdout: upper_$(inputs.chunk.basename)
