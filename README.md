# EUCAIM Toolbox Repository

This repository contains software tools contributed by EUCAIM tool providers and integrated into the EUCAIM compute platform.

The objective of this repository is to provide:

* a **live repository of approved tools** in the process eventually available to EUCAIM users;
* a **template and guidelines** for new tool providers wishing to contribute their tools;
* all metadata and test assets required by EUCAIM platform operators to validate and integrate tools into the platform.



# Contents

The repository is strucutred like folows:

```text
.
├── README.md
├── CONTRIBUTING.md
└── toolbox/
    ├── cdm_federatedunbalance_checker/
    ├── another_tool/
    └── ...
└──  tool_template/
```

- `toolbox/`: it contains the supportive information of on-boarded approved tools to successfully test and register them in EUCAIM platform. Each subdirectory corresponds to a single tool. The tool [cdm_federatedunbalance_checker](https://urldefense.com/v3/__https://github.com/EUCAIM/software-template-repository/tree/main/toolbox/cdm_federated_unbalance_checker__;!!D9dNQwwGXtA!XiyUWjEHlqm1Cwb0f1zn2dyB9JQ7bC_kbd4ZTBQYA-yvAZGaXOVCdiM_Hx0aIFcF_XxxQp3FLuEgoPOacZwPa14y$) is provided as an example implementation and may be used as a reference by future contributors.
- `tool_template`:  it contains the template that tool providers shall use to prepare a new submission. Tool providers should not modify the template directly. Instead, they should copy it into the `toolbox/` directory using their tool name. Example:

```text
toolbox/
└── my_amazing_tool/
```
# Requirements

The repository aims at keeping the contribution barrier as low as possible. However, some components are mandatory.

A tool submission **must contain**

* references to task container images already available at [EUCAIM Harbor registry](https://urldefense.com/v3/__https://harbor.eucaim.cancerimage.eu/__;!!D9dNQwwGXtA!XiyUWjEHlqm1Cwb0f1zn2dyB9JQ7bC_kbd4ZTBQYA-yvAZGaXOVCdiM_Hx0aIFcF_XxxQp3FLuEgoPOacZZxnLLB$)
* integration test datasets, including input datasets and expected outputs
* metadata required for execution (e.g. CWL files for FEM)

# Contributing a new tool

Contributions are expected through GitHub Pull Requests (PR). The recommended workflow is:

### 1. Fork this repository

### 2. Create a new tool directory

Copy `tool_template/` into `toolbox/`.

Example

```bash
cp -r tool_template toolbox/my_amazing_tool
```

### 3. Prepare your tool

Follow the instructions described in [tool_template/README.md](tool_template/README.md) In particular, you will need to provide

* task container information
* metadata for FEM execution
* integration test datasets
* expected outputs
* documentation

### 4. Commit changes

Push your modifications to your fork.

### 5. Open a Pull Request

Open a PR against this repository.

# Review process

EUCAIM platform operators will review the submission.

Validation includes:

* metadata completeness
* integration tests execution against provided test data
* compatibility with EUCAIM CDM
* compatibility with EUCAIM compute infrastructures

Possible outcomes are:

* Approved and merged
* Requested changes: direct communication with the provider for clarifications


# Questions

For questions regarding submissions or integration issues, please contact EUCAIM platform operators through GitHub Issues or PR discussions.

