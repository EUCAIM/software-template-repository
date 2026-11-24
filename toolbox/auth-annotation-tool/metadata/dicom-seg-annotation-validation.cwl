# femtask.schema.yaml
cwlVersion: v1.2
class: FEMTask

id: dicom-seg-annotation-validation
label: DICOM-SEG Annotation Validation
doc: >
  Validates DICOM-SEG annotation files against a configurable set of required
  DICOM tags and exports a per-file validity CSV report plus a JSON summary
  report.

requirements:
  - class: DockerRequirement
    dockerPull: harbor.eucaim.cancerimage.eu/ingestion-tools/annotation_tool:latest
  - class: ResourceRequirement
    coresMin: 2
    ramMin: 2048

baseCommand: [python3, annotation_tool_v4_clean.py]

inputs:
  dicom_dir:
    type: Directory
    doc: Directory containing the DICOM (DICOM-SEG) files to validate.
    required: true
    default: null
    hidden: false
    source: user
    inputBinding:
      prefix: --dicom_dir
      separate: true

  requirements_file:
    type: File
    doc: YAML file defining the required DICOM tags and validation rules.
    required: true
    default: null
    hidden: false
    source: user
    inputBinding:
      prefix: --requirements
      separate: true

  output_dir:
    type: string
    doc: Directory where the exported CSV and JSON reports are written.
    required: false
    default: "."
    hidden: false
    source: user
    inputBinding:
      prefix: --output_dir
      separate: true
      valueFrom: $(runtime.outdir)

  verbose:
    type: boolean
    doc: Enable verbose logging.
    required: false
    default: false
    hidden: false
    source: user
    inputBinding:
      prefix: --verbose

outputs:
  annotation_report_csv:
    type: File
    doc: Per-file annotation validity report (CSV), named annotation_report_<run-date>.csv.
    outputBinding:
      glob: annotation_report_*.csv

  annotation_validity_report_json:
    type: File
    doc: Aggregated annotation validity summary (JSON), named annotation_validity_report_<run-date>.json.
    outputBinding:
      glob: annotation_validity_report_*.json

expectedExitCode: 0

metadata:
  author: Ioannis Ladakis (iladakig@auth.gr)
  version: "1.0.0"
  orchestrator:
    network: bridge
    additional_metadata: {}
