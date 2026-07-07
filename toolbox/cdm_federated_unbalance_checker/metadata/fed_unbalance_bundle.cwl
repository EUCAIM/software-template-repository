cwlVersion: v1.2
class: FEMBundle

id: federated-unbalance-bundle
label: Federated Unbalance Bundle
doc: Summarizes datasets and aggregates their summaries to assess dataset balance.

mode: federated

tasks:
  - task_id: federated-unbalance-runner
    role: client
    multiplicity:
      type: multiple
      min: 1
      max: null
      doc: One runner is executed per dataset.

  - task_id: federated-unbalance-aggregator
    role: server
    multiplicity:
      type: single
      doc: One aggregator combines the runner outputs.
  
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
  - id: report
    type: File
    doc: Final aggregated dataset balance report.
    source:
      task_id: federated-unbalance-aggregator
      task_output_name: report

dependencies:
  - type: exit
    value: 0
    from: federated-unbalance-runner
    to: [federated-unbalance-aggregator]

metadata:
  author: Mona Ashtari, Carles Hernandez-Ferrer
  version: "alpha2.0"
  orchestrator:
    additional_metadata: {}
