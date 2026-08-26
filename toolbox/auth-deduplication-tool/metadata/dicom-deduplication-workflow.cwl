# femworkflow.schema.yaml
cwlVersion: v1.2
class: FEMWorkflow

id: dicom-deduplication-workflow
label: DICOM Deduplication Workflow
doc: Runs the DICOM deduplication tool against a dataset on a single execution site.

execution_sites:
  - alias: execution_site
    kind: single
    selection: user
    value: null
    doc: Site where the deduplication task is executed.

bundles:
  - bundle_id: dicom-deduplication-bundle
    doc: Scans the dataset directory and produces the deduplication report.
    site_bindings:
      - role: worker
        site: execution_site

inputs:
  - id: dataset_dir
    type: Directory
    doc: Root directory containing the DICOM dataset to scan.
    required: true
    default: null
    hidden: false
    scope: global
    constraints: {}
    targets:
      - bundle_id: dicom-deduplication-bundle
        bundle_input_name: dataset_dir

  - id: workers
    type: int
    doc: Number of parallel worker processes used for scanning, hashing, and pixel comparison.
    required: false
    default: 8
    hidden: false
    scope: global
    constraints:
      min: 1
    targets:
      - bundle_id: dicom-deduplication-bundle
        bundle_input_name: workers

  - id: exclude_modalities
    type: string[]
    doc: Modalities to exclude from deduplication analysis.
    required: false
    default: ["SEG", "RTSTRUCT"]
    hidden: false
    scope: global
    constraints: {}
    targets:
      - bundle_id: dicom-deduplication-bundle
        bundle_input_name: exclude_modalities

  - id: sample_step
    type: int
    doc: Stride used when sampling pixel frames for series hashing.
    required: false
    default: 5
    hidden: false
    scope: global
    constraints:
      min: 1
    targets:
      - bundle_id: dicom-deduplication-bundle
        bundle_input_name: sample_step

  - id: keep_nonimage
    type: boolean
    doc: If set, keep non-image instances instead of filtering them out before comparison.
    required: false
    default: false
    hidden: false
    scope: global
    constraints: {}
    targets:
      - bundle_id: dicom-deduplication-bundle
        bundle_input_name: keep_nonimage

  - id: output_json
    type: string
    doc: Name of the JSON deduplication report file to be produced.
    required: true
    default: dedup_report.json
    hidden: false
    scope: global
    constraints: {}
    targets:
      - bundle_id: dicom-deduplication-bundle
        bundle_input_name: output_json

outputs:
  - id: dedup_report
    type: File
    doc: JSON report listing duplicate and near-duplicate findings for the input dataset.
    source:
      bundle_id: dicom-deduplication-bundle
      bundle_output_name: dedup_report

connections: []

metadata:
  author: Ioannis Ladakis (iladakig@auth.gr)
  version: "0.9.0"
  apps: {}
  version_control:
    repository: "https://github.com/EUCAIM/software-template-repository"
    branch: "main"
