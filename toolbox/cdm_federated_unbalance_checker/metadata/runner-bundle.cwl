cwlVersion: v1.2
class: FEMBundle

id: federated-unbalance-runner-bundle
label: Federated Unbalance Bundle
doc: A Python tool for federated dataset unbalance checking

mode: federated

tasks:
  - task_id: federated-unbalance-runner
    role: client
    multiplicity:
      type: multiple
      doc: One runner is executed per dataset.

inputs:
  - dataset_dirs:
      type: Directory[]
      doc: Dataset directories to be summarized by the runner.
      required: true
      targets:
        - task_id: federated-unbalance-runner
          task_input_name: dataset_dir

outputs:
  runner_json:
    type: File[]
    doc: Name of the JSON file to be produced.
    source:
      task_id: federated-unbalance-runner
      task_output_name: runner_json
    aggregation: keep_array

arguments: []

metadata:
  author: Mona Ashtari, Carles Hernandez-Ferrer
  version: "alpha2.0"
  orchestrator:
    additional_metadata: {}
