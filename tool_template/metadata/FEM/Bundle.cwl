# fembundle.schema.yaml
cwlVersion: v1.2
class: FEMBundle # Custom class for for FEM, abstraction for local, distributed, 
                 # and federated execution modes

id: string            # Machine-readable name of the bundle
label: string         # Human-readable name of the bundle
doc: string           # Description of the bundle

mode: 
  federated |         # Federated: multi-node with roles (client/server)
   distributed |      # Distributed: multi-mode (parallel tasks)
    standalone        # Standalone: intentional single-node execution

tasks:
  - task_id: string   # Reference to Task (CommandLineTool) IDs
    role: server |    # As when a single unit needs to be run together with
                      #   multiple clients
           client |   # As when multiple units need to be run together with
                      #   a single server
            worker    # As when no role is needed (for distributed mode)
    multiplicity: 
      type: single |  # As when a task needs to be executed once in a single node
             multiple # As when a task needs to be executed one in multiple nodes
      doc: string     # Free text for clarity (e.g., "1 server", "multiple clients")
    execution_site: string[]  # Assigned at execution time by FEM

inputs:
  - input_name: string
    type: string | int | File | Directory | string[]  # Inherited from the task it
                                                      # comes from
    doc: string
    required: boolean          # is this argument mandatory to be filled
    targets:
      - task_id: string          # list of id of the task
        task_input_name: string  # with the input name in the selected tasks

outputs:
  - output_name: string
    type: File | Directory | string[] # Inherited from the task it comes from
    doc: string
    source:
      task_id: string           # task id that generates it
      task_output_name: string  # with the output’s name in the selected task
    aggregation: merge | pick_first | keep_array

arguments:
  - arg_name: string # Unique ID for this argument
    type: string | int | boolean | float
    doc: string
    default: string | int | boolean | float # Optional default value
    required: boolean
    targets:
      - task_id: string
        position: int     # Specific to this task's
        prefix: string    # Specific to this task (e.g., "--verbose" vs "-v")
        separate: boolean # Specific to this task (--flag val vs --flag=val)
        valueFrom: string | expression # Optional transformation per task

metadata:
  author: string
  version: string
  orchestrator:
    additional_metadata: object  # Freeform metadata for node-level orchestration
