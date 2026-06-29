cwlVersion: v1.2
class: FEMTask

id: runner
label: Federated Unbalance Runner
doc: A Python tool for federated dataset unbalance checking

requirements:
  - class: DockerRequirement
    dockerPull: harbor.eucaim.cancerimage.eu/processing-tools/federated-unbalance-runner:latest

inputs:
  dataset_dir:
    type: Directory
    doc: Input dataset directory containing clinical_mandatory_view.csv.
    inputBinding:
      position: 1
      prefix: -i
      separate: true
  
  output_name:
    type: string
    doc: Name of the JSON summary file to be produced.
    inputBinding:
      position: 2
      prefix: -o
      separate: true
      valueFrom: $(runtime.outdir)/$(self)
  
  log_stdout:
    type: string
    doc: Filename for standard output log.
    default: stdout.log  # Enforced default name
  
  log_stderr:
    type: string
    doc: Filename for standard error log.
    default: stderr.log  # Enforced default name

outputs:
  runner_json:
    type: File
    doc: JSON summary generated for the input dataset.
    outputBinding:
      glob: $(inputs.output_name)

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
