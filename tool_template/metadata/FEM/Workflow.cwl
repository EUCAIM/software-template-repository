# femworkflow.schema.yaml
cwlVersion: v1.2
class: FEMWorkflow # Custom class, but structurally mirrors CWL Workflow

id: string                 # Machine-readable workflow ID
label: string              # Human-readable name of the workflow
doc: string                # Description of the workflow purpose

execution_nodes:
  - node_alias: runtime-param
    node_name: string

bundles:
  - bundle_id: string      # Reference to a bundle
    doc: string            # Human reference (e.g., "fed-training", "quality-control")
    execution_sites:
    - node_alias: string
      role: server | client | worker

inputs:
  - input_name: string
    type: string | int | File | Directory | string[]  # Inherited from the bundle it
                                                      # comes from
    doc: string
    required: boolean          # is this argument mandatory to be filled
    default: string | int | float | File | Directory # Optional
    targets:
      - bundle_id: string          # list of ids of bundles
        bundle_input_name: string  # with the input name in the selected bundle

outputs:
  - output_name: string
    type: File | Directory | string[] # Inherited from the task it comes from
    doc: string
    source:
      bundle_id: string           # bundles id that generates it
      bundle_input_name: string   # with the output’s name in the selected bundles
    aggregation: merge_nested | merge_flattened | pick_first

arguments:
  - arg_name: string               # Unique ID for this argument
    type: string | int | boolean | float
    doc: string
    default: string | int | boolean | float # Optional default value
    required: boolean
    targets:
      - bundle_id: string
        default: string | int | boolean | float # Optional: Override value per bundle

connections:
  - from:
      bundle_id: string # bundles id that generates it
      output: string    # name of the given output
    to:
      bundle_id: string # bundles id that needs it
      input: string     # name of the given input

metadata:
  author: string
  version: string
  apps: # Application-specific metadata (by BSC/UPV)
    app_name: # “OpenVRE”, “jobman”, "nextflow", "snakemake", "airflow" (by BSC/UPV)
      enabled: boolean
      config: # App-specific configuration
        - key: string
          value: any
  version_control: # Version control metadata
    repository: string
    branch: string
    commit: string
    tag: string   
  compliance: # Compliance and governance (by BSC)
    data_classification: public | private
    retention_policy:
      inputs_retention: string
      outputs_retention: string
      logs_retention: string
    security:
      access_control:
        - role: string
          permissions: string[]
