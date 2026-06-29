cwlVersion: v1.2
class: FEMBundle

id: federated-unbalance-bundle
label: Federated Unbalance Bundle
doc: A Python tool for federated dataset unbalance checking

mode: federated

tasks:
  - task_id: runner
    role: client
    multiplicity:
      type: multiple
      doc: One runner is executed per dataset.
    execution_site: []

  - task_id: aggregator
    role: server
    multiplicity:
      type: single
      doc: One aggregator combines the runner outputs.
    execution_site: []

inputs:
  - dataset_dirs:
      type: Directory[]
      doc: Dataset directories to be summarized by the runner.
      required: true
      targets:
        - task_id: runner
          task_input_name: dataset_dir

  - output_names:
      type: string[]
      doc: Output JSON filenames for the runner summaries.
      required: true
      targets:
        - task_id: runner
          task_input_name: output_name

outputs:
  - report:
      type: File
      doc: Final aggregated dataset balance report.
      source:
        task_id: aggregator
        task_output_name: report
      aggregation: pick_first

arguments: []

metadata:
  author: Mona Ashtari
  version: "alpha2.0"
  orchestrator:
    additional_metadata: {}
