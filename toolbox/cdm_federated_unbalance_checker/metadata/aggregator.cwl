cwlVersion: v1.2
class: FEMTask

id: aggregator
label: Federated Unbalance Aggregator
doc: A Python tool for federated dataset unbalance checking (aggregation component)

requirements:
  - class: DockerRequirement
    dockerPull: harbor.eucaim.cancerimage.eu/processing-tools/federated-unbalance-aggregator:latest

inputs:
  runner_jsons:
    type:
      type: array
      items: File
    doc: JSON summary files produced by the runner.
    inputBinding:
      position: 1
      prefix: -i
      separate: true
  output_dir:
    type: string
    doc: Directory where report.json will be written.
    default: .
    inputBinding:
      position: 2
      prefix: -o
      separate: true
      valueFrom: $(runtime.outdir)

  log_stdout:
    type: string
    doc: Filename for standard output log.
    default: stdout.log

  log_stderr:
    type: string
    doc: Filename for standard error log.
    default: stderr.log

outputs:
  report:
    type: File
    doc: Aggregated dataset balance report.
    outputBinding:
      glob: report.json

  task_stdout:
    type: File
    doc: Captured standard output.
    outputBinding:
      glob: $(inputs.log_stdout)

  task_stderr:
    type: File
    doc: Captured standard error.
    outputBinding:
      glob: $(inputs.log_stderr)

baseCommand: [python, main.py]

metadata:                 
  author: Mona Ashtari
  version: "alpha2.0"
  orchestrator:
    network: overlay
    additional_metadata: {}
