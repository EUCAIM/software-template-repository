cwlVersion: v1.2
class: FEMBundle

id: federated-unbalance-aggregator-bundle
label: Federated Unbalance Aggregator Bundle
doc: Aggregates dataset summaries to assess dataset balance.

mode: federated

tasks:
  - task_id: federated-unbalance-aggregator
    role: server
    multiplicity:
      type: single
      doc: One aggregator combines the runner outputs.

shared_inputs:
  - id: runner_jsons
    type: File[]
    doc: JSON summary files produced by the runner.
    required: true
    default: null
    hidden: true
    constraints: {}
    targets:
      - task_id: federated-unbalance-aggregator
        task_input_name: runner_jsons

shared_outputs:
  - id: report
    type: File
    doc: Final aggregated dataset balance report.
    source:
      task_id: federated-unbalance-aggregator
      task_output_name: report

dependencies: []

metadata:
  author: Mona Ashtari, Carles Hernandez-Ferrer
  version: "alpha2.0"
  orchestrator:
    additional_metadata: {}
