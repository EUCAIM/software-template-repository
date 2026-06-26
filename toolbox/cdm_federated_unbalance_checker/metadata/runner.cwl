cwlVersion: v1.0
class: CommandLineTool

requirements:
  DockerRequirement:
    dockerPull: federated-unbalance-runner
  InlineJavascriptRequirement: {}

baseCommand: [python, main.py]

inputs:
  dataset_dir:
    type: Directory
    inputBinding:
      prefix: -i

  output_name:
    type: string

  output_path:
    type: string
    inputBinding:
      prefix: -o
      valueFrom: $(runtime.outdir)/$(inputs.output_name)

outputs:
  runner_json:
    type: File
    outputBinding:
      glob: $(inputs.output_name)