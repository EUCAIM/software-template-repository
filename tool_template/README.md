# Contributing a tool to EUCAIM

Tool providers contribute by submitting Pull Requests containing a new tool directory under

```text
toolbox/
```

This template helps tool providers to create the three parts that are compulsory to make available a new software tool in EUCAIM federated compute platform:
1) All container images registered in EUCAIM Harbor
2) Metadata describing how EUCAIM platform can run the new tool
3) Test dataset to validate the integration
4) Tool Documentation 
 

As explained in the [main README file](README.md), the easiest approach is to start forking the whole repository, copying `tool_template/` and renaming it to your own tool name `toolbox/<tool_name>`. 

### Template structure

```text
├── tool_template/
│   ├── README.md
│   ├── LICENSE
│   ├── task_containers/
│   │   ├── container_name_task-A
|   │   │   ├── dockerfile
|   │   │   ├── app/
|   │   │   └── entrypoint.sh
│   │   ├── another_task_cotainer
│   │   └── ...
│   ├── metadata/
│   │   ├── FEM/
|   │   │   ├── tool_bundle.cwl
│   │   │   └── ...
│   │   └── jobman/
│   ├── docs/
│   └── test/
│       └── example_input/
│       └── example_output/
```


# How to prepare task container images
A EUCAIM tools consists on a set of containers executed .... that corresponds to tasks

Tool providers are free to build images using their own CI/CD pipelines. Dockerfiles do not need to be shared. Images should however be built using the supplied `entrypoint.sh` mechanism so that execution inside EUCAIM infrastructures remains compatible.

*TODO: Merge in here the old README content*

# How to prepare test datasets

At minimum contributors shall provide

```text
test/
├── example_input/
└── example_output/
```

Input datasets shall correspond to the minimal dataset required by the tool and follow

* EUCAIM Common Data Model
* EUCAIM file-system conventions

Expected outputs shall be deterministic whenever possible.

If outputs are non deterministic,

```text
test/example_output/description.md
```

shall explain which properties should be checked during integration testing.

Providing expected execution logs is recommended.

# How to prepare Metadata

Metadata shall contain the information required for execution within EUCAIM compute infrastructures.

Particular focus is placed on execution through FEM.

Contributors shall provide

```text
metadata/FEM/
```

including

* CWL descriptions for each task
* a workflow CWL describing the complete tool execution
* `bundle.cwl` defining the overall workflow

Additional metadata formats may be added in the future.

# How to prepare the Tool documentation

