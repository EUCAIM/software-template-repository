cwlVersion: v1.2
class: FEMTask

id: federated-unbalance-runner
label: Federated Unbalance Runner
doc: A Python tool for federated dataset unbalance checking

requirements:
  - class: DockerRequirement
    dockerPull: harbor.eucaim.cancerimage.eu/processing-tools/federated-unbalance-runner:latest

inputs:
  dataset_dirs:
    type: Directory[]
    doc: List of input dataset directories containing clinical_mandatory_view.csv.
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
    doc: Directory where the JSON summary files for datasets will be written.
    required: true
    default: null
    hidden: false
    source: user
    inputBinding:
      position: 2
      prefix: -o
      separate: true
      valueFrom: $(runtime.outdir)

outputs:
  runner_json:
    type: File[]
    doc: JSON summary files generated for the input datasets.
    outputBinding:
      glob: "*.json"

baseCommand: [python, main.py]

expectedExitCode: 0  

metadata:                 
  author: Mona Ashtari, Carles Hernandez-FErrer
  version: "alpha2.0"
  orchestrator:
    network: overlay
    additional_metadata: {}
