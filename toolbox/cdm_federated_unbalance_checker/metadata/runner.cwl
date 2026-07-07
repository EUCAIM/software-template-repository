cwlVersion: v1.2
class: FEMTask

id: federated-unbalance-runner
label: Federated Unbalance Runner
doc: A Python tool for federated dataset unbalance checking

requirements:
  - class: DockerRequirement
    dockerPull: harbor.eucaim.cancerimage.eu/processing-tools/federated-unbalance-runner:latest

inputs:
  dataset_dir:
    type: Directory
    doc: Input dataset directory containing clinical_mandatory_view.csv.
    required: true
    default: null
    hidden: false
    source: user
    inputBinding:
      position: 1
      prefix: -i
      separate: true
  
  json_file:
    type: string
    doc: Name of the JSON summary file to be produced.
    required: true
    default: null
    hidden: false
    source: user
    inputBinding:
      position: 2
      prefix: -o
      separate: true
      valueFrom: $(runtime.outdir)/$(self)

outputs:
  runner_json:
    type: File
    doc: JSON summary generated for the input dataset.
    outputBinding:
      glob: $(inputs.json_file)

baseCommand: [python, main.py]

expectedExitCode: 0  

metadata:                 
  author: Mona Ashtari, Carles Hernandez-FErrer
  version: "alpha2.0"
  orchestrator:
    network: overlay
    additional_metadata: {}
