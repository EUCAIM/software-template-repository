cwlVersion: v1.2
class: FEMBundle

id: federated-unbalance-runner-bundle
label: Federated Unbalance Bundle
doc: Runs dataset-level summaries for federated dataset balance analysis.

mode: federated

tasks:
  - task_id: federated-unbalance-runner
    role: client
    multiplicity:
      type: multiple
      min: 1       
      max: null 
      doc: One runner is executed per dataset.

shared_inputs:
  - id: dataset_dirs
    type: Directory
    doc: Dataset directories containing clinical_mandatory_view.csv.
    required: true
    default: null
    hidden: false
    constraints: {}
    targets:
      - task_id: federated-unbalance-runner
        task_input_name: dataset_dir

shared_outputs:
  - id: runner_json
    type: File
    doc: JSON summary produced by each runner instance.
    source:
      task_id: federated-unbalance-runner
      task_output_name: runner_json

dependencies: []

metadata:
  author: Mona Ashtari, Carles Hernandez-Ferrer
  version: "alpha2.0"
  orchestrator:
    additional_metadata: {}
