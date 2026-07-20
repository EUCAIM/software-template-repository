# fembundle.schema.yaml
cwlVersion: v1.2
class: FEMBundle

id: dicom-deduplication-bundle
label: DICOM Deduplication Bundle
doc: Single-node deduplication scan of a local DICOM dataset directory.

mode: standalone

tasks:
  - task_id: dicom-deduplication
    role: worker
    multiplicity:
      type: single
      doc: One deduplication task runs against the provided dataset directory.

shared_inputs:
  - id: dataset_dir
    type: Directory
    doc: Root directory containing the DICOM dataset to scan.
    required: true
    default: null
    hidden: false
    constraints: {}
    targets:
      - task_id: dicom-deduplication
        task_input_name: dataset_dir

  - id: workers
    type: int
    doc: Number of parallel worker processes used for scanning, hashing, and pixel comparison.
    required: false
    default: 8
    hidden: false
    constraints:
      min: 1
    targets:
      - task_id: dicom-deduplication
        task_input_name: workers

  - id: exclude_modalities
    type: string[]
    doc: Modalities to exclude from deduplication analysis.
    required: false
    default: ["SEG", "RTSTRUCT"]
    hidden: false
    constraints: {}
    targets:
      - task_id: dicom-deduplication
        task_input_name: exclude_modalities

  - id: sample_step
    type: int
    doc: Stride used when sampling pixel frames for series hashing.
    required: false
    default: 5
    hidden: false
    constraints:
      min: 1
    targets:
      - task_id: dicom-deduplication
        task_input_name: sample_step

  - id: keep_nonimage
    type: boolean
    doc: If set, keep non-image instances instead of filtering them out before comparison.
    required: false
    default: false
    hidden: false
    constraints: {}
    targets:
      - task_id: dicom-deduplication
        task_input_name: keep_nonimage

  - id: output_json
    type: string
    doc: Name of the JSON deduplication report file to be produced.
    required: true
    default: dedup_report.json
    hidden: false
    constraints: {}
    targets:
      - task_id: dicom-deduplication
        task_input_name: output_json

shared_outputs:
  - id: dedup_report
    type: File
    doc: JSON report listing duplicate and near-duplicate findings for the input dataset.
    source:
      task_id: dicom-deduplication
      task_output_name: dedup_report

dependencies: []

metadata:
  author: Ioannis Ladakis (iladakig@auth.gr)
  version: "0.9.0"
  orchestrator:
    additional_metadata: {}
