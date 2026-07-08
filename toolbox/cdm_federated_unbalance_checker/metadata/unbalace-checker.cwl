# femworkflow.schema.yaml
cwlVersion: v1.2
class: FEMWorkflow

id: federated-unbalance-workflow
label: Federated Unbalance Workflow
doc: Runs dataset-level summaries and aggregates them to assess dataset balance.

execution_sites:
  - alias: client_sites
    kind: group
    selection: user
    value: null
    min: 1
    max: null
    doc: Sites where runner tasks are executed.

  - alias: server_site
    kind: single
    selection: user
    value: null
    doc: Site where the aggregator task is executed.

bundles:
  - bundle_id: federated-unbalance-runner-bundle
    doc: Runs the runner on each selected dataset/site.
    site_bindings:
      - role: client
        site: client_sites

  - bundle_id: federated-unbalance-aggregator-bundle
    doc: Aggregates runner outputs into the final balance report.
    site_bindings:
      - role: server
        site: server_site

inputs:
  - id: dataset_dirs
    type: Directory
    doc: Dataset directory containing clinical_mandatory_view.csv for each client site.
    required: true
    default: null
    hidden: false
    scope: per_node
    constraints: {}
    targets:
      - bundle_id: federated-unbalance-runner-bundle
        bundle_input_name: dataset_dirs

outputs:
  - id: report
    type: File
    doc: Final aggregated dataset balance report.
    source:
      bundle_id: federated-unbalance-aggregator-bundle
      bundle_output_name: report

connections:
  - type: file
    policy: all
    delivery: gather
    from:
      bundle_id: federated-unbalance-runner-bundle
      output_name: runner_json
    to:
      bundle_id: federated-unbalance-aggregator-bundle
      input_name: runner_jsons

metadata:
  author: Mona Ashtari, Carles Hernandez-Ferrer
  version: "alpha2.0"
  apps: {}
  version_control:
    repository: "https://gitlab.bsc.es/fl/eucaim-cdm-federated-unbalance"
    branch: "CDM-adoption"

