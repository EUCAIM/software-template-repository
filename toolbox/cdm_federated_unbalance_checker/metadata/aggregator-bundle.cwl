cwlVersion: v1.2
class: FEMBundle

id: federated-unbalance-aggregator-bundle
label: Federated Unbalance Bundle
doc: A Python tool for federated dataset unbalance checking

mode: federated

tasks:
  - task_id: federated-unbalance-aggregator
    role: server
    multiplicity:
      type: single
      doc: One aggregator combines the runner outputs.
    execution_site: []

inputs:
  - runner_jsons:
      type: File[]
      doc: Dataset directories to be summarized by the runner.
      required: true
      targets:
        - task_id: federated-unbalance-aggregator
          task_input_name: runner_jsons

  - output_dir:
      type: string
      doc: Output JSON filenames for the runner summaries.
      required: true
      targets:
        - task_id: federated-unbalance-aggregator
          task_input_name: output_dir

outputs:
  - report:
      type: File
      doc: Final aggregated dataset balance report.
      source:
        task_id: federated-unbalance-aggregator
        task_output_name: report
      aggregation: pick_first

arguments: []

metadata:
  author: Mona Ashtari, Carles Hernandez-Ferrer
  version: "alpha2.0"
  orchestrator:
    additional_metadata: {}
