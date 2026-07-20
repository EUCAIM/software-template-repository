# fembundle.schema.yaml
cwlVersion: v1.2
class: FEMBundle

id: dicom-seg-annotation-validation-bundle
label: DICOM-SEG Annotation Validation Bundle
doc: Single-node validation of DICOM-SEG annotations against a required-tags ruleset.

mode: standalone

tasks:
  - task_id: dicom-seg-annotation-validation
    role: worker
    multiplicity:
      type: single
      doc: One validation task runs against the provided DICOM directory.

shared_inputs:
  - id: dicom_dir
    type: Directory
    doc: Directory containing the DICOM (DICOM-SEG) files to validate.
    required: true
    default: null
    hidden: false
    constraints: {}
    targets:
      - task_id: dicom-seg-annotation-validation
        task_input_name: dicom_dir

  - id: requirements_file
    type: File
    doc: YAML file defining the required DICOM tags and validation rules.
    required: true
    default: null
    hidden: false
    constraints: {}
    targets:
      - task_id: dicom-seg-annotation-validation
        task_input_name: requirements_file

  - id: output_dir
    type: string
    doc: Directory where the exported CSV and JSON reports are written.
    required: false
    default: "."
    hidden: false
    constraints: {}
    targets:
      - task_id: dicom-seg-annotation-validation
        task_input_name: output_dir

  - id: verbose
    type: boolean
    doc: Enable verbose logging.
    required: false
    default: false
    hidden: false
    constraints: {}
    targets:
      - task_id: dicom-seg-annotation-validation
        task_input_name: verbose

shared_outputs:
  - id: annotation_report_csv
    type: File
    doc: Per-file annotation validity report (CSV).
    source:
      task_id: dicom-seg-annotation-validation
      task_output_name: annotation_report_csv

  - id: annotation_validity_report_json
    type: File
    doc: Aggregated annotation validity summary (JSON).
    source:
      task_id: dicom-seg-annotation-validation
      task_output_name: annotation_validity_report_json

dependencies: []

metadata:
  author: Ioannis Ladakis (iladakig@auth.gr)
  version: "1.0.0"
  orchestrator:
    additional_metadata: {}
