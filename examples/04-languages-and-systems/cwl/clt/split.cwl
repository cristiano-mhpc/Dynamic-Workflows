cwlVersion: v1.2
class: CommandLineTool
requirements:
  InitialWorkDirRequirement:
    listing:
      - entry: printf '$(inputs.str)' | split -b 6 - chunk_
        entryname: script.sh
baseCommand: [sh, script.sh]
inputs:
  str:
    type: string
outputs:
  out:
    type: File[]
    outputBinding:
      glob: 'chunk_*'
