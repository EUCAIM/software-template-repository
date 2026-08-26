# femworkflow.schema.yaml
cwlVersion: v1.2
class: FEMWorkflow

id: dicom-seg-annotation-validation-workflow
label: DICOM-SEG Annotation Validation Workflow
doc: Runs the DICOM-SEG annotation validation tool against a dataset on a single execution site.

execution_sites:
  - alias: execution_site
    kind: single
    selection: user
    value: null
    doc: Site where the annotation validation task is executed.

bundles:
  - bundle_id: dicom-seg-annotation-validation-bundle
    doc: Validates the DICOM-SEG dataset and produces the CSV/JSON reports.
    site_bindings:
      - role: worker
        site: execution_site

inputs:
  - id: dicom_dir
    type: Directory
    doc: Directory containing the DICOM (DICOM-SEG) files to validate.
    required: true
    default: null
    hidden: false
    scope: global
    constraints: {}
    targets:
      - bundle_id: dicom-seg-annotation-validation-bundle
        bundle_input_name: dicom_dir

  - id: requirements_file
    type: File
    doc: YAML file defining the required DICOM tags and validation rules.
    required: true
    default: null
    hidden: false
    scope: global
    constraints: {}
    targets:
      - bundle_id: dicom-seg-annotation-validation-bundle
        bundle_input_name: requirements_file

  - id: output_dir
    type: string
    doc: Directory where the exported CSV and JSON reports are written.
    required: false
    default: "."
    hidden: false
    scope: global
    constraints: {}
    targets:
      - bundle_id: dicom-seg-annotation-validation-bundle
        bundle_input_name: output_dir

  - id: verbose
    type: boolean
    doc: Enable verbose logging.
    required: false
    default: false
    hidden: false
    scope: global
    constraints: {}
    targets:
      - bundle_id: dicom-seg-annotation-validation-bundle
        bundle_input_name: verbose

outputs:
  - id: annotation_report_csv
    type: File
    doc: Per-file annotation validity report (CSV).
    source:
      bundle_id: dicom-seg-annotation-validation-bundle
      bundle_output_name: annotation_report_csv

  - id: annotation_validity_report_json
    type: File
    doc: Aggregated annotation validity summary (JSON).
    source:
      bundle_id: dicom-seg-annotation-validation-bundle
      bundle_output_name: annotation_validity_report_json

connections: []

metadata:
  author: Ioannis Ladakis (iladakig@auth.gr)
  version: "1.0.0"
  apps: {}
  version_control:
    repository: "https://github.com/EUCAIM/software-template-repository"
    branch: "main"
