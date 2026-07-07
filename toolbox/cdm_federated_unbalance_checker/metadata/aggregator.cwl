cwlVersion: v1.2
class: FEMTask

id: federated-unbalance-aggregator
label: Federated Unbalance Aggregator
doc: A Python tool for federated dataset unbalance checking (aggregation component)

requirements:
  - class: DockerRequirement
    dockerPull: harbor.eucaim.cancerimage.eu/processing-tools/federated-unbalance-aggregator:latest

inputs:
  runner_jsons:
    type: File[]
    doc: JSON summary files produced by the runner.
    required: true
    default: null
    hidden: false
    source: user
    inputBinding:
      position: 1
      prefix: -i
      separate: true

  output_dir:
    type: string
    doc: Directory where report.json and .html will be written.
    default: .
    required: true
    hidden: false
    source: user
    inputBinding:
      position: 2
      prefix: -o
      separate: true
      valueFrom: $(runtime.outdir)

outputs:
  report:
    type: File
    doc: Aggregated dataset balance report.
    outputBinding:
      glob: report.json

baseCommand: [python, main.py]

expectedExitCode: 0  

metadata:                 
  author: Mona Ashtari, Carles Hernandez-Ferrer
  version: "alpha2.0"
  orchestrator:
    network: overlay
    additional_metadata: {}
