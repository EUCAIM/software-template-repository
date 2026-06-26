cwlVersion: v1.0
class: CommandLineTool

requirements:
  DockerRequirement:
    dockerPull: federated-unbalance-aggregator

baseCommand: []

inputs:
  runner_jsons:
    type:
      type: array
      items: File
    inputBinding:
      prefix: -i

  output_dir:
    type: string
    default: .
    inputBinding:
      prefix: -o
      valueFrom: $(runtime.outdir)

outputs:
  report:
    type: File
    outputBinding:
      glob: report.json